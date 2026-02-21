from django.urls import path
from . import views

app_name = 'team_member'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('register/', views.register_view, name='register'),
    # path('team/', views.team_list, name='team_list'),
    # path('team/<int:user_id>/toggle/', views.toggle_status, name='toggle_status'),
    # path('team/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('dashboard/', views.dashboard_view, name='dashboard'),  # ✅ NEW
    path('manage-permissions/', views.manage_permissions, name='manage_permissions'),  # ✅ ADD THIS
    
    path('team-members/', views.team_member_list, name='team_member_list'),
    path('team-members/add/', views.add_team_member, name='add_team_member'),
    path('toggle-permission/', views.toggle_permission, name='toggle_permission'),  # ✅ ADD THIS

    path('team-members/<int:member_id>/edit/', views.edit_team_member, name='edit_team_member'),
    path('team-members/<int:member_id>/delete/', views.delete_team_member, name='delete_team_member'),


]
