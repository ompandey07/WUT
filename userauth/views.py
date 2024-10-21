from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser , Post , Task
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.core.serializers.json import DjangoJSONEncoder



#############################################################
#*** This View Handles Registration Of Users ***
#############################################################
@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        profile_picture = request.FILES.get('profile_picture')
        
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Account with this email already exists'})

        try:
            user = CustomUser.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            
            if profile_picture:
                user.profile_picture = profile_picture
            
            user.save()
            login(request, user)
            
            # Refresh CSRF token
            new_csrf_token = get_token(request)
            return JsonResponse({
                'status': 'success', 
                'message': 'Registration successful!',
                'csrfToken': new_csrf_token
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # For GET requests, render the template
    return render(request, 'Reg & Logins/Register.html')
#############################################################
# View Ends Here
#############################################################




#############################################################
#*** This View Handles Login Of Users ***
#############################################################
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect': '/dashboard_view/'})  
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    return render(request, 'Reg & Logins/Login.html')
#############################################################
# This View Ends Here 
#############################################################




#############################################################
# This View Handles Logout Of Users 
#############################################################
def logout_view(request):
    logout(request)
    return redirect('login_view')
#############################################################
# This View Ends Here 
#############################################################







############################################################################################################################################################################
                                                                    #  !  All Other Addtional Views 
############################################################################################################################################################################                                                                       




#############################################################
#**** This View Handles Dashboards Of Users ***#
#############################################################
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Post):
            return {
                'id': obj.id,
                'content': obj.content,
                'user_name': obj.user.get_full_name() or obj.user.username,
                'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
                'created_at': obj.created_at.isoformat(),
                'views': obj.views
            }
        return super().default(obj)

@login_required
def dashboard_view(request):
    user = request.user
    print(f"Current user: {user.username}, ID: {user.id}")  
    
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            post = Post.objects.create(user=user, content=content)
            return JsonResponse({
                'status': 'success',
                'post': CustomJSONEncoder().default(post)
            })
        return JsonResponse({'status': 'error', 'message': 'Content is required'})

    posts = Post.objects.all().select_related('user').order_by('-created_at')
    posts_json = json.dumps(list(posts), cls=CustomJSONEncoder)

    # Fetch recent tasks
    recent_tasks = Task.objects.filter(user=user).order_by('-created_at')[:10]

    context = {
        'user': user,
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
        'posts_json': posts_json,
        'recent_tasks': recent_tasks  # Add recent tasks to the context
    }
    return render(request, "Pages/Dashboard.html", context)
#############################################################
# This View Ends Here 
#############################################################






#############################################################
# **** This View Handles Profiles Of Users ***
#############################################################
@login_required
def user_profile_view(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    
    posts_json = json.dumps(list(posts), cls=CustomJSONEncoder)

    context = {
        'user': user,
        'posts_json': posts_json,
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
        'cover_photo': 'https://wallpapercave.com/wp/wp9258170.jpg',  
        'joined_date': user.registration_date.strftime('%B %d, %Y')
    }
    return render(request, 'Pages/UserProfile.html', context)
#############################################################
# This View Ends Here 
#############################################################





#############################################################
# **** This View Handles Works Of Users ***
#############################################################
@login_required
@require_http_methods(["GET", "POST"])
def work_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get('action')
        task_id = data.get('task_id')
        content = data.get('content')

        if action == 'add':
            task = Task.objects.create(user=request.user, content=content)
            return JsonResponse({
                'status': 'success',
                'task': {
                    'id': task.id,
                    'content': task.content,
                    'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        elif action == 'update' and task_id:
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                task.content = content
                task.save()
                return JsonResponse({'status': 'success'})
            except Task.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Task not found'})
        elif action == 'delete' and task_id:
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                task.delete()
                return JsonResponse({'status': 'success'})
            except Task.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Task not found'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'Pages/Works.html', {'user': request.user, 'tasks': tasks})
#############################################################
# This View Ends Here 
#############################################################