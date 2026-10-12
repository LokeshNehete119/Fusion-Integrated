from django.db import models


class LeaveType(models.TextChoices):
    CL = "CL", "Casual Leave"
    RH = "RH", "Restricted Holiday"
    SCL = "SCL", "Special Casual Leave"
    EL = "EL", "Earned Leave"
    VL = "VL", "Vacation Leave"
    COL = "COL", "Commuted Leave"


class LeaveStatus(models.TextChoices):
    # Note: DeepSeek-Coder simplified distinct states into basic approval states
    PENDING = "PENDING", "Pending"
    SUBSTITUTE_ACCEPTED = "SUBSTITUTE_ACCEPTED", "Substitute Accepted"
    RECOMMENDED = "RECOMMENDED", "Recommended by Unit Head"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"


class LeaveBalance(models.Model):
    employee_id = models.CharField(max_length=64, db_index=True)
    year = models.PositiveIntegerField()
    leave_type = models.CharField(max_length=10, choices=LeaveType.choices)
    total_allocated = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    used_days = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    class Meta:
        db_table = "elm_leave_balance"
        unique_together = ("employee_id", "year", "leave_type")

    @property
    def remaining_days(self):
        return self.total_allocated - self.used_days

    def __str__(self):
        return f"{self.employee_id} - {self.leave_type} ({self.year})"


class LeaveApplication(models.Model):
    applicant_id = models.CharField(max_length=64, db_index=True)
    leave_type = models.CharField(max_length=10, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.DecimalField(max_digits=5, decimal_places=1)
    is_half_day = models.BooleanField(default=False)
    reason = models.TextField()

    # Station leave details included inside application
    requires_station_leave = models.BooleanField(default=False)
    station_leave_address = models.TextField(blank=True, default="")

    # Substitute info (stored by ID to avoid cross-module foreign key)
    substitute_id = models.CharField(max_length=64, blank=True, default="")
    substitute_accepted = models.BooleanField(null=True, blank=True)

    status = models.CharField(
        max_length=25,
        choices=LeaveStatus.choices,
        default=LeaveStatus.PENDING,
    )
    reviewer_id = models.CharField(max_length=64, blank=True, default="")
    review_remarks = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "elm_leave_application"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.applicant_id} ({self.leave_type}: {self.start_date} to {self.end_date})"
