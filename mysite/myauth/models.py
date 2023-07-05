from django.contrib.auth.models import User
from django.db import models


def avatar_directory_path(instance, filename: str) -> str:
    return "user-details/avatar/{instance}/{filename}".format(
        filename=filename,
        instance=instance,
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_directory_path)
    agreement_accepted = models.BooleanField(default=False)


# class ProfileAvatar(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="avatar")
#     avatar = models.ImageField(upload_to=)

