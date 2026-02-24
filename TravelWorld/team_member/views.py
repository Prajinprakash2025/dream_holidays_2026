# team_member/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from Travel.models import TeamMember
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from team_member.decorators import admin_required
from team_member.forms import TeamMemberForm
from team_member.permissions import AVAILABLE_PERMISSIONS, get_permissions_by_category


# ==========================================
# AUTHENTICATION VIEWS
# ==========================================

def login_view(request):
    """Login - Support both TeamMember and Django User (superuser)"""

    # ✅ FIXED: Proper redirect instead of HttpResponse
    if request.session.get('user_id'):
        messages.info(request, '✅ You are already logged in!')
        return redirect('team_member:dashboard')  # or just redirect('/')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username_or_email or not password:
            messages.error(request, '❌ Username/Email and password required')
            return render(request, 'login.html')

        # Try Team Member First
        try:
            user = TeamMember.objects.get(email=username_or_email, is_active=True)

            if user.check_password(password):
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                request.session['full_name'] = user.get_full_name()
                request.session['role'] = user.role
                request.session['user_type'] = 'team_member'

                user.last_login = now()
                user.save(update_fields=['last_login'])

                messages.success(request, f'✅ Welcome {user.get_full_name()}!')

                # ✅ Support redirect to previous page
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, '❌ Invalid password')
                return render(request, 'login.html')

        except TeamMember.DoesNotExist:
            pass

        # Try Django Superuser
        try:
            try:
                django_user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                django_user = User.objects.get(email=username_or_email)

            if django_user.check_password(password) and django_user.is_superuser:
                request.session['user_id'] = django_user.id
                request.session['email'] = django_user.email
                request.session['full_name'] = django_user.get_full_name() or django_user.username
                request.session['role'] = 'admin'
                request.session['user_type'] = 'superuser'

                messages.success(request, f'✅ Welcome Admin {django_user.username}!')

                # ✅ Support redirect to previous page
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, '❌ Invalid password or not superuser')
                return render(request, 'login.html')

        except User.DoesNotExist:
            pass

        messages.error(request, '❌ User not found')

    return render(request, 'login.html')


def logout_view(request):
    """Logout"""
    print("🔥 LOGOUT VIEW CALLED")
    print(f"Session before flush: {dict(request.session)}")

    name = request.session.get('full_name', 'User')
    request.session.flush()

    print("✅ Session flushed")

    messages.success(request, f'✅ Goodbye, {name}!')
    return redirect('team_member:login')


def dashboard_view(request):
    """Dashboard - Check if user is logged in"""
    if not request.session.get('user_id'):
        messages.warning(request, '⚠️ Please login first')
        return redirect('team_member:login')

    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_type == 'superuser':
        user = User.objects.get(id=user_id)
    else:
        user = TeamMember.objects.get(id=user_id)

    context = {
        'user': user,
        'full_name': request.session.get('full_name'),
        'role': request.session.get('role'),
        'user_type': user_type,
    }

    return render(request, 'dashboard.html', context)


# ==========================================
# PERMISSION MANAGEMENT VIEWS
# ==========================================

@admin_required
def manage_permissions(request):
    """Admin panel to manage user permissions"""

    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_type != 'superuser':
        current_user = TeamMember.objects.get(id=user_id)
        if current_user.role != 'admin':
            messages.error(request, '❌ You do not have permission to manage permissions')
            return redirect('team_member:dashboard')

    team_members = TeamMember.objects.filter(is_active=True).order_by('first_name')

    # Pre-process data
    team_data = []
    for member in team_members:
        member_info = {
            'member': member,
            'permissions_status': {}
        }

        for perm_key in AVAILABLE_PERMISSIONS.keys():
            # Check if permission exists in member.permissions dict
            member_info['permissions_status'][perm_key] = (
                member.permissions.get(perm_key, False) if member.permissions else False
            )

        team_data.append(member_info)

    context = {
        'team_data': team_data,
        'permissions_by_category': get_permissions_by_category(),
        'available_permissions': AVAILABLE_PERMISSIONS,
    }
    return render(request, 'manage_permissions.html', context)


@admin_required
@require_POST
def toggle_permission(request):
    """✅ AJAX endpoint to toggle permission"""
    try:
        user_id = request.POST.get('user_id')
        permission = request.POST.get('permission')
        action = request.POST.get('action')  # 'grant' or 'revoke'

        if not user_id or not permission or not action:
            return JsonResponse({
                'success': False,
                'message': 'Missing required parameters'
            }, status=400)

        member = get_object_or_404(TeamMember, id=user_id)

        # Get current permissions or initialize empty dict
        current_permissions = member.permissions if member.permissions else {}

        # Update permission
        if action == 'grant':
            current_permissions[permission] = True
            action_text = 'granted'
        else:
            current_permissions[permission] = False
            action_text = 'revoked'

        # Save back to model
        member.permissions = current_permissions
        member.save(update_fields=['permissions'])

        perm_label = AVAILABLE_PERMISSIONS.get(permission, {}).get('label', permission)

        return JsonResponse({
            'success': True,
            'message': f'✅ "{perm_label}" {action_text} for {member.get_full_name()}'
        })

    except TeamMember.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Team member not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


# ==========================================
# TEAM MEMBER MANAGEMENT VIEWS
# ==========================================

@admin_required
def team_member_list(request):
    """List all team members"""
    team_members = TeamMember.objects.all().order_by('-created_at')
    form = TeamMemberForm()

    context = {
        'team_members': team_members,
        'form': form,
    }
    return render(request, 'team_member_list.html', context)


@admin_required
@require_POST
def add_team_member(request):
    """Add new team member via modal form"""
    form = TeamMemberForm(request.POST)

    if form.is_valid():
        team_member = form.save(commit=False)

        password = form.cleaned_data.get('password')
        if password:
            team_member.set_password(password)
        else:
            if not team_member.id:
                messages.error(request, '❌ Password is required for new members')
                return redirect('team_member:team_member_list')

        team_member.save()
        messages.success(request, f'✅ Team Member "{team_member.get_full_name()}" added successfully!')
    else:
        messages.error(request, f'❌ Error: {form.errors.as_text()}')

    return redirect('team_member:team_member_list')


@admin_required
@require_POST
def edit_team_member(request, member_id):
    """Edit team member via modal form"""
    member = get_object_or_404(TeamMember, id=member_id)
    
    # Logic Fix: Manually handle is_active if it's missing from POST (unchecked)
    data = request.POST.copy()
    if 'is_active' not in data:
        data['is_active'] = False
    else:
        data['is_active'] = True

    form = TeamMemberForm(data, instance=member)

    if form.is_valid():
        team_member = form.save(commit=False)

        password = form.cleaned_data.get('password')
        if password:
            team_member.set_password(password)

        team_member.save()
        messages.success(request, f'✅ Team Member "{team_member.get_full_name()}" updated successfully!')
    else:
        # Better error reporting for debugging
        error_msg = ", ".join([f"{k}: {v[0]}" for k, v in form.errors.items()])
        messages.error(request, f'❌ Error: {error_msg}')

    return redirect('team_member:team_member_list')


@admin_required
@require_POST
def delete_team_member(request, member_id):
    """Delete team member"""
    member = get_object_or_404(TeamMember, id=member_id)

    if member.id == request.session.get('user_id'):
        messages.error(request, '❌ You cannot delete yourself')
        return redirect('team_member:team_member_list')

    name = member.get_full_name()
    member.delete()
    messages.success(request, f'✅ Team Member "{name}" deleted successfully!')
    return redirect('team_member:team_member_list')
