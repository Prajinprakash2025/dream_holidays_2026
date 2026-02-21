# team_member/decorators.py

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def custom_login_required(view_func):
    """Check if user is logged in via session"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.warning(request, '⚠️ Please login to continue')
            return redirect('team_member:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Check if user is admin (TeamMember or Django superuser)"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        role = request.session.get('role')
        user_type = request.session.get('user_type')
        
        if not user_id:
            messages.warning(request, '⚠️ Please login to continue')
            return redirect('team_member:login')
        
        # ✅ Allow if role is admin OR user type is superuser
        if role == 'admin' or user_type == 'superuser':
            return view_func(request, *args, **kwargs)
        
        messages.error(request, '❌ Admin access required')
        return redirect('/')
    
    return wrapper
