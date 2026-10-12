from rest_framework import serializers
from modules.elm.models import LeaveApplication, LeaveBalance


class LeaveBalanceSerializer(serializers.ModelSerializer):
    remaining_days = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)

    class Meta:
        model = LeaveBalance
        fields = [
            "id",
            "employee_id",
            "year",
            "leave_type",
            "total_allocated",
            "used_days",
            "remaining_days",
        ]


class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = [
            "id",
            "applicant_id",
            "leave_type",
            "start_date",
            "end_date",
            "total_days",
            "is_half_day",
            "reason",
            "requires_station_leave",
            "station_leave_address",
            "substitute_id",
            "substitute_accepted",
            "status",
            "reviewer_id",
            "review_remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "applicant_id",
            "total_days",
            "status",
            "reviewer_id",
            "review_remarks",
            "created_at",
            "updated_at",
        ]


class LeaveApplicationCreateSerializer(serializers.Serializer):
    leave_type = serializers.ChoiceField(choices=["CL", "RH", "SCL", "EL", "VL", "COL"])
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    is_half_day = serializers.BooleanField(default=False)
    reason = serializers.CharField()
    requires_station_leave = serializers.BooleanField(default=False)
    station_leave_address = serializers.CharField(required=False, allow_blank=True, default="")
    substitute_id = serializers.CharField(required=False, allow_blank=True, default="")


class LeaveReviewSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["approve", "recommend", "reject"])
    remarks = serializers.CharField(required=False, allow_blank=True, default="")
