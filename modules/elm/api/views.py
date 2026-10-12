from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fusion_auth.permissions import HasModuleGrant, HasPermission
from modules.elm.api.serializers import (
    LeaveApplicationCreateSerializer,
    LeaveApplicationSerializer,
    LeaveBalanceSerializer,
    LeaveReviewSerializer,
)
from modules.elm.models import LeaveApplication
from modules.elm.services import (
    cancel_leave_application,
    get_or_init_balances,
    review_leave_application,
    submit_leave_application,
)

MODULE_GRANT = HasModuleGrant("elm")


def _actor_id(request) -> str:
    principal = getattr(request, "principal", None)
    if principal and hasattr(principal, "username"):
        return str(principal.username)
    if request.user and request.user.is_authenticated:
        return str(request.user.username)
    return "anonymous"


class MyLeaveBalancesView(APIView):
    permission_classes = [MODULE_GRANT, HasPermission("elm.leave.view_self")]

    def get(self, request):
        actor_id = _actor_id(request)
        balances = get_or_init_balances(actor_id)
        return Response(LeaveBalanceSerializer(balances, many=True).data)


class MyLeaveApplicationsView(APIView):
    permission_classes = [MODULE_GRANT, HasPermission("elm.leave.view_self")]

    def get(self, request):
        actor_id = _actor_id(request)
        qs = LeaveApplication.objects.filter(applicant_id=actor_id)
        return Response(LeaveApplicationSerializer(qs, many=True).data)

    def post(self, request):
        serializer = LeaveApplicationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        actor_id = _actor_id(request)
        app = submit_leave_application(actor_id, serializer.validated_data)
        return Response(
            LeaveApplicationSerializer(app).data,
            status=status.HTTP_201_CREATED,
        )


class CancelLeaveApplicationView(APIView):
    permission_classes = [MODULE_GRANT, HasPermission("elm.leave.cancel")]

    def post(self, request, pk: int):
        actor_id = _actor_id(request)
        app = cancel_leave_application(pk, actor_id)
        return Response(LeaveApplicationSerializer(app).data)


class PendingApprovalsView(APIView):
    permission_classes = [MODULE_GRANT, HasPermission("elm.leave.review")]

    def get(self, request):
        qs = LeaveApplication.objects.all()
        return Response(LeaveApplicationSerializer(qs, many=True).data)


class ReviewLeaveApplicationView(APIView):
    permission_classes = [MODULE_GRANT, HasPermission("elm.leave.review")]

    def post(self, request, pk: int):
        serializer = LeaveReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reviewer_id = _actor_id(request)
        app = review_leave_application(
            pk,
            reviewer_id,
            serializer.validated_data["action"],
            serializer.validated_data.get("remarks", ""),
        )
        return Response(LeaveApplicationSerializer(app).data)
