from django.db import models
import uuid
import os
from django.contrib.auth.models import User

class Folder(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)


def get_uploade_path(instance, filename):
    return os.path.join(str(instance.folder.uid), filename) 

class Files(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateField(auto_now=True)
