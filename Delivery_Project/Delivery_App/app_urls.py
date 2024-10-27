# from django.contrib import admin
from django.urls import path
from .views import (DeliveryView, example_view, Delivery_acceptace_view, Agent_details,Agent_action, active_tasks_view,
                    dashboard_map_view, dashboard_agent_view, tasks_list_view,task_list_by_daterange_view,
                    Task_Request_View, get_dpartner_notification_view, countrycodes_view, settings_view, create_team_view)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('delivery/', DeliveryView.as_view()),
    path('rpc/', example_view),
    path('delivery_response/',Delivery_acceptace_view.as_view()),
    path('dashboard_active_tasks/', active_tasks_view),
    path('dashboard_map/<str:merchant_id>/',dashboard_map_view),
    path('dashboard_agent_list/', dashboard_agent_view),
    path('agent_list/',Agent_details),
    path('agent_list/<str:phone>/',Agent_details),
    path('tasks_list/', tasks_list_view),
    path('tasklist_daterange/',task_list_by_daterange_view),
    path('task_request/', Task_Request_View.as_view()),
    path('agent_action/', Agent_action),
    path('dpartner_notification_response/',get_dpartner_notification_view),
    path('countrycodes/', countrycodes_view),
    path('settings/', settings_view),
    path('createteam/', create_team_view),

]
