from rest_framework import serializers
from .models import *
import shutil
import os

class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 10000, allow_empty_file= False, use_url = False)
    )
    name = serializers.CharField(max_length=255, required=False)
    
    def save_files_to_temp(self, files, folder_path):
        """Temporarily save files to create zip"""
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
    
    def cleanup_temp_files(self, folder_path):
        """Remove temporary files after zip creation"""
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
    
    def create(self, validated_data):
        user = self.context.get('user')
        name = validated_data.get('name', 'Untitled Upload')
        folder = Folder.objects.create(user=user, name=name)
        files = validated_data.pop('files')
      
        temp_folder_path = f'public/static/{folder.uid}'
        zip_path = f'public/static/zip{folder.uid}'
        
        try:
            self.save_files_to_temp(files, temp_folder_path)
            shutil.make_archive(zip_path, 'zip', temp_folder_path)
            self.cleanup_temp_files(temp_folder_path)
            return {'folder': folder.uid}
        except Exception as e:
            self.cleanup_temp_files(temp_folder_path)
            if os.path.exists(f'{zip_path}.zip'):
                os.remove(f'{zip_path}.zip')
            folder.delete()
            raise e