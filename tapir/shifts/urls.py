from django.urls import path

from tapir.shifts import views

app_name = "shifts"
urlpatterns = [
    path(
        "user/<int:user_pk>/set_user_attendance_mode_flying",
        views.set_user_attendance_mode_flying,
        name="set_user_attendance_mode_flying",
    ),
    path(
        "user/<int:user_pk>/set_user_attendance_mode_regular",
        views.set_user_attendance_mode_regular,
        name="set_user_attendance_mode_regular",
    ),
    # TODO(Leon Handreke): Can we somehow introduce a sub-namespace here?
    path("shift/<int:pk>/", views.ShiftDetailView.as_view(), name="shift_detail"),
    path(
        "shift/<int:pk>/printable",
        views.ShiftDetailView.as_view(
            template_name="shifts/shift_detail_printable.html"
        ),
        name="shift_detail_printable",
    ),
    path(
        "shift/<str:day>/day_printable",
        views.ShiftDayPrintableView.as_view(),
        name="shift_day_printable",
    ),
    path(
        "shift/create",
        views.CreateShiftView.as_view(),
        name="shift_create",
    ),
    path(
        "shiftslot/<int:pk>/register/<int:user_pk>",
        views.shiftslot_register_user,
        name="shiftslot_register_user",
    ),
    path(
        "shift/<int:pk>/edit",
        views.EditShiftView.as_view(),
        name="shift_edit",
    ),
    path(
        "shift_attendance/<int:pk>/<int:state>",
        views.UpdateShiftAttendanceStateView.as_view(),
        name="update_shift_attendance_state",
    ),
    path(
        "shift_attendance_form/<int:pk>/<int:state>",
        views.UpdateShiftAttendanceStateWithFormView.as_view(),
        name="update_shift_attendance_state_with_form",
    ),
    path(
        "shifttemplate/<int:pk>",
        views.ShiftTemplateDetail.as_view(),
        name="shift_template_detail",
    ),
    path(
        "shifttemplate/overview",
        views.ShiftTemplateOverview.as_view(),
        name="shift_template_overview",
    ),
    path(
        "slottemplate/<int:slot_template_pk>/register",
        views.SlotTemplateRegisterView.as_view(),
        name="slottemplate_register",
    ),
    path(
        "shiftslot/<int:slot_pk>/register/",
        views.SlotRegisterView.as_view(),
        name="slot_register",
    ),
    path(
        "shift_attendance_template/<int:pk>/delete",
        views.shift_attendance_template_delete,
        name="shift_attendance_template_delete",
    ),
    path(
        "calendar",
        views.ShiftCalendarFutureView.as_view(),
        name="calendar_future",
    ),
    path(
        "calendar_past",
        views.ShiftCalendarPastView.as_view(),
        name="calendar_past",
    ),
    path(
        "shift_user_data/<int:pk>",
        views.EditShiftUserDataView.as_view(),
        name="edit_shift_user_data",
    ),
    path(
        "group_calendar",
        views.ShiftTemplateGroupCalendar.as_view(),
        name="shift_template_group_calendar",
    ),
    path(
        "user_shift_account_log/<int:user_pk>",
        views.UserShiftAccountLog.as_view(),
        name="user_shift_account_log",
    ),
    path(
        "create_shift_account_entry/<int:user_pk>",
        views.CreateShiftAccountEntryView.as_view(),
        name="create_shift_account_entry",
    ),
    path(
        "create_shift_exemption/<int:shift_user_data_pk>",
        views.CreateShiftExemptionView.as_view(),
        name="create_shift_exemption",
    ),
    path(
        "edit_shift_exemption/<int:pk>",
        views.EditShiftExemptionView.as_view(),
        name="edit_shift_exemption",
    ),
    path(
        "shift_exemption_list",
        views.ShiftExemptionListView.as_view(),
        name="shift_exemption_list",
    ),
]
