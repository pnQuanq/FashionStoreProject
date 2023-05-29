from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
    is_email_vertified = models.BooleanField(default=False, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

