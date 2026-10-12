from django.urls import path
from modules.elm.api import views as v

urlpatterns = [
    path("balances", v.MyLeaveBalancesView.as_view(), name="elm-balances"),
    path("applications", v.MyLeaveApplicationsView.as_view(), name="elm-applications"),
    path("applications/<int:pk>/cancel", v.CancelLeaveApplicationView.as_view(), name="elm-application-cancel"),
    path("approvals", v.PendingApprovalsView.as_view(), name="elm-approvals"),
    path("approvals/<int:pk>/review", v.ReviewLeaveApplicationView.as_view(), name="elm-application-review"),
]
