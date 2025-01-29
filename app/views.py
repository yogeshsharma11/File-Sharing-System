from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileListSerializer
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from django.shortcuts import render



def home(request):
    return render(request ,'home.html')

def download(request , uid):
    return render(request , 'download.html' , context = {'uid' : uid})



class HandleFileUploade(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request):
        try:
            data = request.data
            serializer = FileListSerializer(data=data)

            if serializer.is_valid():
                result = serializer.save()
                return Response({
                    'status': 200,
                    'message': 'File Uploaded Successfully',
                    'data': result
                })
            return Response({
                'status': 400,
                'message': 'File Upload Failed',
                'errors': serializer.errors
            })

        except Exception as e:
            return Response({
                'status': 500,
                'message': 'An error occurred',
                'error': str(e)
            })
