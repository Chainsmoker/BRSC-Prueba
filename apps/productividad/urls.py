from django.urls import path
from . import views

app_name = 'productivity'

urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('api/events/', views.EventsApiView.as_view(), name='events_api'),
    path('activity/add/', views.ActivityCreateView.as_view(), name='activity_add'),
    path('activity/<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='activity_edit'),
    path('activity/<int:pk>/score/', views.ScoreActivityView.as_view(), name='activity_score'),
    path('reports/user/<int:user_id>/', views.UserReportView.as_view(), name='user_report'),
    path('activity/form-ajax/', views.ActivityFormAjaxView.as_view(), name='activity_form_ajax'),

    path('activity/<int:pk>/edit-ajax/', views.ActivityEditAjaxView.as_view(), name='activity_edit_ajax'),
]