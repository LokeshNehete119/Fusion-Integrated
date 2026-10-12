from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from core.api.exceptions import BadRequestError, NotFoundError
from modules.elm.models import LeaveApplication, LeaveBalance, LeaveStatus, LeaveType

DEFAULT_ENTITLEMENTS = {
    LeaveType.CL: Decimal("8.0"),
    LeaveType.RH: Decimal("2.0"),
    LeaveType.SCL: Decimal("15.0"),
    LeaveType.EL: Decimal("30.0"),
    LeaveType.VL: Decimal("60.0"),
    LeaveType.COL: Decimal("20.0"),
}


def get_or_init_balances(employee_id: str, year: int | None = None):
    if year is None:
        year = timezone.now().year
    balances = list(LeaveBalance.objects.filter(employee_id=employee_id, year=year))
    existing_types = {b.leave_type for b in balances}
    for ltype, default_days in DEFAULT_ENTITLEMENTS.items():
        if ltype not in existing_types:
            b = LeaveBalance.objects.create(
                employee_id=employee_id,
                year=year,
                leave_type=ltype,
                total_allocated=default_days,
                used_days=Decimal("0.0"),
            )
            balances.append(b)
    return balances


@transaction.atomic
def submit_leave_application(applicant_id: str, data: dict) -> LeaveApplication:
    start_date = data["start_date"]
    end_date = data["end_date"]
    leave_type = data["leave_type"]
    is_half_day = data.get("is_half_day", False)

    if end_date < start_date:
        raise BadRequestError("End date cannot be earlier than start date.")

    if is_half_day and leave_type != LeaveType.CL:
        raise BadRequestError("Half-day option is only allowed for Casual Leave (CL).")

    # Check overlapping active leave requests
    overlap = LeaveApplication.objects.filter(
        applicant_id=applicant_id,
        start_date__lte=end_date,
        end_date__gte=start_date,
    ).exclude(status__in=[LeaveStatus.REJECTED, LeaveStatus.CANCELLED]).exists()

    if overlap:
        raise BadRequestError("Leave dates overlap with an existing leave application.")

    if is_half_day:
        total_days = Decimal("0.5")
    else:
        total_days = Decimal((end_date - start_date).days + 1)

    year = start_date.year
    get_or_init_balances(applicant_id, year)
    balance = LeaveBalance.objects.select_for_update().get(
        employee_id=applicant_id, year=year, leave_type=leave_type
    )

    if balance.remaining_days < total_days:
        raise BadRequestError(f"Insufficient {leave_type} balance.")

    application = LeaveApplication.objects.create(
        applicant_id=applicant_id,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        total_days=total_days,
        is_half_day=is_half_day,
        reason=data.get("reason", ""),
        requires_station_leave=data.get("requires_station_leave", False),
        station_leave_address=data.get("station_leave_address", ""),
        substitute_id=data.get("substitute_id", ""),
        status=LeaveStatus.PENDING,
    )
    return application


@transaction.atomic
def review_leave_application(application_id: int, reviewer_id: str, action: str, remarks: str = "") -> LeaveApplication:
    try:
        app = LeaveApplication.objects.select_for_update().get(pk=application_id)
    except LeaveApplication.DoesNotExist:
        raise NotFoundError("Leave application not found.")

    if action == "approve":
        if app.status == LeaveStatus.APPROVED:
            raise BadRequestError("Leave is already approved.")
        balance = LeaveBalance.objects.select_for_update().get(
            employee_id=app.applicant_id,
            year=app.start_date.year,
            leave_type=app.leave_type,
        )
        if balance.remaining_days < app.total_days:
            raise BadRequestError("Insufficient leave balance to approve request.")
        balance.used_days += app.total_days
        balance.save(update_fields=["used_days"])
        app.status = LeaveStatus.APPROVED
    elif action == "recommend":
        app.status = LeaveStatus.RECOMMENDED
    elif action == "reject":
        app.status = LeaveStatus.REJECTED
    else:
        raise BadRequestError("Invalid review action.")

    app.reviewer_id = reviewer_id
    app.review_remarks = remarks
    app.save()
    return app


@transaction.atomic
def cancel_leave_application(application_id: int, actor_id: str) -> LeaveApplication:
    try:
        app = LeaveApplication.objects.select_for_update().get(pk=application_id, applicant_id=actor_id)
    except LeaveApplication.DoesNotExist:
        raise NotFoundError("Leave application not found.")

    if app.status == LeaveStatus.APPROVED:
        balance = LeaveBalance.objects.select_for_update().get(
            employee_id=app.applicant_id,
            year=app.start_date.year,
            leave_type=app.leave_type,
        )
        balance.used_days = max(Decimal("0.0"), balance.used_days - app.total_days)
        balance.save(update_fields=["used_days"])

    app.status = LeaveStatus.CANCELLED
    app.save(update_fields=["status", "updated_at"])
    return app
