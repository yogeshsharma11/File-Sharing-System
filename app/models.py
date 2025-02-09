from django.db import models
import uuid
import os
from django.contrib.auth.models import User
import string
import random

def generate_short_uid():
    """Generate a short 8-character unique ID"""
    chars = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    while True:
        uid = ''.join(random.choices(chars, k=8))  # 8 characters long
        if not Folder.objects.filter(uid=uid).exists():
            return uid

class Folder(models.Model):
    uid = models.CharField(max_length=8, primary_key=True, default=generate_short_uid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)

    def get_download_url(self):
        return f"/download/{self.uid}/"

    def get_zip_path(self):
        return f"public/static/zip{self.uid}.zip"

    def delete(self, *args, **kwargs):
        # Delete associated zip file
        zip_path = self.get_zip_path()
        if os.path.exists(f"{zip_path}.zip"):
            os.remove(f"{zip_path}.zip")
        super().delete(*args, **kwargs)

def get_uploade_path(instance, filename):
    return os.path.join(str(instance.folder.uid), filename) 

class Files(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateField(auto_now=True)
