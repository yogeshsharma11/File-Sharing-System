from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileListSerializer
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import logout
from .models import Folder, OTP
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.hashers import make_password

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'auth/login.html')

def signup_view(request):
    if request.method == 'POST':
        if 'verify_otp' in request.POST:
            email = request.POST.get('email')
            otp_entered = request.POST.get('otp')
            otp_obj = OTP.objects.filter(email=email, is_verified=False).last()
            
            if otp_obj and otp_obj.otp == otp_entered:
                username = request.POST.get('username')
                password = request.POST.get('password1')
                
                user = User.objects.create_user(username=username, email=email, password=password)
                otp_obj.is_verified = True
                otp_obj.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'auth/signup.html', {
                    'email': email,
                    'username': request.POST.get('username'),
                    'show_otp': True
                })
                
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'auth/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'auth/signup.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'auth/signup.html')

        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        OTP.objects.create(email=email, otp=otp)
        
        # Send OTP email
        send_mail(
            'Your OTP for File Share Registration',
            f'Your OTP is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return render(request, 'auth/signup.html', {
            'email': email,
            'username': username,
            'password1': password1,
            'show_otp': True
        })

    return render(request, 'auth/signup.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        
        if not user:
            messages.error(request, 'No account found with this email address')
            return render(request, 'auth/forgot_password.html')
            
        # Generate OTP
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        OTP.objects.create(email=email, otp=otp)
        
        # Send OTP email
        send_mail(
            'Password Reset OTP for File Share',
            f'Your OTP for password reset is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return render(request, 'auth/forgot_password.html', {
            'email': email,
            'show_otp': True
        })
        
    return render(request, 'auth/forgot_password.html')

def verify_reset_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_entered = request.POST.get('otp')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'auth/forgot_password.html', {
                'email': email,
                'show_otp': True
            })
            
        otp_obj = OTP.objects.filter(email=email, is_verified=False).last()
        
        if otp_obj and otp_obj.otp == otp_entered:
            user = User.objects.get(email=email)
            user.password = make_password(new_password1)
            user.save()
            
            otp_obj.is_verified = True
            otp_obj.save()
            
            messages.success(request, 'Password reset successful. Please login with your new password.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP')
            return render(request, 'auth/forgot_password.html', {
                'email': email,
                'show_otp': True
            })
            
    return redirect('forgot_password')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def download(request, uid):
    return render(request, 'download.html', context={'uid': uid})

@login_required(login_url='login')
def my_files(request):
    if request.method == 'POST' and request.POST.get('delete'):
        folder_uid = request.POST.get('delete')
        folder = Folder.objects.filter(uid=folder_uid, user=request.user).first()
        if folder:
            folder.delete()
            messages.success(request, 'File deleted successfully')
        return redirect('my_files')

    folders = Folder.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_files.html', {'folders': folders})

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            # Delete all user's files and folders
            Folder.objects.filter(user=user).delete()
            # Delete the user
            user.delete()
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid password. Account deletion failed.')
            return redirect('profile')
            
    return redirect('profile')

class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]
    
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({
                    'status': 403,
                    'message': 'Please log in to upload files'
                }, status=403)

            if not request.FILES:
                return Response({
                    'status': 400,
                    'message': 'No files were uploaded'
                }, status=400)

            serializer = FileListSerializer(data=request.data, context={'user': request.user})

            if serializer.is_valid():
                result = serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Files uploaded successfully',
                    'data': result
                })
            
            return Response({
                'status': 400,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=400)
            
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'An error occurred',
                'error': str(e)
            }, status=500)
