# team_member/context_processors.py

from Travel.models import TeamMember
from django.contrib.auth.models import User


def user_context(request):
    """Add current user to all templates"""
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')  # ✅ GET USER TYPE
    
    if user_id and user_type:
        try:
            # ✅ CHECK USER TYPE BEFORE QUERYING
            if user_type == 'superuser':
                # Handle Django superuser
                user = User.objects.get(id=user_id, is_superuser=True)
                return {
                    'current_user': user,
                    'is_admin': True,  # Superusers are always admin
                    'is_manager': True,
                    'is_authenticated': True,
                    'user_type': 'superuser',
                }
            
            elif user_type == 'team_member':
                # Handle TeamMember
                user = TeamMember.objects.get(id=user_id, is_active=True)
                return {
                    'current_user': user,
                    'is_admin': user.role == 'admin',
                    'is_manager': user.role in ['admin', 'manager'],
                    'is_authenticated': True,
                    'user_type': 'team_member',
                }
        
        except (TeamMember.DoesNotExist, User.DoesNotExist):
            # ✅ Only flush if user truly doesn't exist
            request.session.flush()
            return {'is_authenticated': False}
    
    return {'is_authenticated': False}
