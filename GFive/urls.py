from django.contrib import admin
from django.urls import path
from devices import views

app_name = 'devices'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('halls/', views.HallListView.as_view(), name='hall_list'),
    path('halls/<int:pk>/', views.HallDetailView.as_view(), name='hall_detail'),
    path('halls/create/', views.HallCreateView.as_view(), name='hall_create'),
    path('halls/<int:pk>/update/', views.HallUpdateView.as_view(), name='hall_update'),
    path('halls/<int:pk>/delete/', views.HallDeleteView.as_view(), name='hall_delete'),

    path('devices/', views.DeviceListView.as_view(), name='device_list'),
    path('devices/<int:pk>/', views.DeviceDetailView.as_view(), name='device_detail'),

    path('computers/', views.ComputerListView.as_view(), name='computer_list'),
    path('computers/<int:pk>/', views.ComputerDetailView.as_view(), name='computer_detail'),

    path('consoles/', views.ConsoleListView.as_view(), name='console_list'),
    path('consoles/<int:pk>/', views.ConsoleDetailView.as_view(), name='console_detail'),
]
