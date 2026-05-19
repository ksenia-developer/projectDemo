from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.rooms_list, name='rooms'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinet/', views.dashboard, name='dashboard'),
    path('application/new/', views.application_create, name='application_create'),
    path('review/<int:pk>/', views.review_create, name='review_create'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/<int:pk>/status/', views.admin_change_status, name='admin_change_status'),
]
