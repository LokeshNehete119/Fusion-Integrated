from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LeaveBalance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(db_index=True, max_length=64)),
                ("year", models.PositiveIntegerField()),
                (
                    "leave_type",
                    models.CharField(
                        choices=[
                            ("CL", "Casual Leave"),
                            ("RH", "Restricted Holiday"),
                            ("SCL", "Special Casual Leave"),
                            ("EL", "Earned Leave"),
                            ("VL", "Vacation Leave"),
                            ("COL", "Commuted Leave"),
                        ],
                        max_length=10,
                    ),
                ),
                ("total_allocated", models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ("used_days", models.DecimalField(decimal_places=1, default=0, max_digits=5)),
            ],
            options={
                "db_table": "elm_leave_balance",
                "unique_together": {("employee_id", "year", "leave_type")},
            },
        ),
        migrations.CreateModel(
            name="LeaveApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("applicant_id", models.CharField(db_index=True, max_length=64)),
                (
                    "leave_type",
                    models.CharField(
                        choices=[
                            ("CL", "Casual Leave"),
                            ("RH", "Restricted Holiday"),
                            ("SCL", "Special Casual Leave"),
                            ("EL", "Earned Leave"),
                            ("VL", "Vacation Leave"),
                            ("COL", "Commuted Leave"),
                        ],
                        max_length=10,
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("total_days", models.DecimalField(decimal_places=1, max_digits=5)),
                ("is_half_day", models.BooleanField(default=False)),
                ("reason", models.TextField()),
                ("requires_station_leave", models.BooleanField(default=False)),
                ("station_leave_address", models.TextField(blank=True, default="")),
                ("substitute_id", models.CharField(blank=True, default="", max_length=64)),
                ("substitute_accepted", models.BooleanField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("SUBSTITUTE_ACCEPTED", "Substitute Accepted"),
                            ("RECOMMENDED", "Recommended by Unit Head"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=25,
                    ),
                ),
                ("reviewer_id", models.CharField(blank=True, default="", max_length=64)),
                ("review_remarks", models.TextField(blank=True, default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "elm_leave_application",
                "ordering": ["-created_at"],
            },
        ),
    ]
