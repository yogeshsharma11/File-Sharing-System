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

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('home')

    return render(request, 'auth/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def download(request, uid):
    return render(request, 'download.html', context={'uid': uid})

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

            data = request.data
            serializer = FileListSerializer(data=data, context={'user': request.user})

            if serializer.is_valid():
                result = serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Files uploaded successfully',
                    'data': result
                })
            
            return Response({
                'status': 400,
                'message': 'Invalid file upload',
                'errors': serializer.errors
            }, status=400)

        except Exception as e:
            print(f"Upload error: {str(e)}")  # For debugging
            return Response({
                'status': 500,
                'message': f'An error occurred: {str(e)}',
            }, status=500)
