# Module registration and permissions for Employee Leave Management (ELM)

MODULE = {
    "code": "elm",
    "label": "Employee Leave Management",
    "icon": "CalendarBlank",
    "base_path": "/elm",
    "nav_section": "HR & Leave",
    "sort_order": 20,
    "status": "active",
}

NAV_ITEMS = [
    {
        "code": "elm.dashboard",
        "label": "My Leaves & Balances",
        "icon": "ClipboardText",
        "to": "/elm/dashboard",
        "required_permission": "elm.leave.view_self",
        "sort_order": 10,
    },
    {
        "code": "elm.apply",
        "label": "Apply Leave",
        "icon": "PlusCircle",
        "to": "/elm/apply",
        "required_permission": "elm.leave.apply",
        "sort_order": 20,
    },
    {
        "code": "elm.approvals",
        "label": "Leave Approvals",
        "icon": "Checks",
        "to": "/elm/approvals",
        "required_permission": "elm.leave.review",
        "sort_order": 30,
    },
]

PERMISSIONS = [
    ("elm.leave.view_self", "View own leave applications and balances"),
    ("elm.leave.apply", "Submit a new leave application"),
    ("elm.leave.cancel", "Withdraw or cancel own leave request"),
    ("elm.substitute.respond", "Accept or decline substitute assignment"),
    ("elm.leave.review", "Review and recommend or approve leave requests"),
    ("elm.admin.manage", "Manage leave balances and holiday calendar"),
]

_EMPLOYEE = [
    "elm.leave.view_self",
    "elm.leave.apply",
    "elm.leave.cancel",
    "elm.substitute.respond",
]

_UNIT_HEAD = _EMPLOYEE + [
    "elm.leave.review",
]

_HR_ADMIN = _UNIT_HEAD + [
    "elm.admin.manage",
]

ROLE_GRANTS = {
    "faculty": _EMPLOYEE,
    "staff": _EMPLOYEE,
    "hod": _UNIT_HEAD,
    "unit_head": _UNIT_HEAD,
    "dean": _UNIT_HEAD,
    "establishment_admin": _HR_ADMIN,
}
