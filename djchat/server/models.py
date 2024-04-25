from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from .validators import validate_icon_extension, validate_icon_size
import os

# Create your models here.


def category_icon_upload_path(instance, filename):
    return 'category/{0}/icons/{1}'.format(instance.id, filename)


def channel_icon_upload_path(instance, filename):
    return 'Channel/{0}/icons/{1}'.format(instance.id, filename)


def channel_banner_upload_path(instance, filename):
    return 'channel/{0}/banner/{1}'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.FileField(
        null=True,
        blank=True,
        upload_to=category_icon_upload_path,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # Check if the instance already exists in the database
        if self.pk:
            try:
                # Retrieve the existing instance from the database
                existing_instance = get_object_or_404(Category, pk=self.pk)
                # Compare the existing icon with the new icon
                if existing_instance.icon and existing_instance.icon != self.icon:
                    # Delete the old icon file
                    existing_instance.icon.delete(save=False)

            except Category.DoesNotExist:
                pass
        super().save(*args, **kwargs)  # Call the real save() method

    def delete(self, *args, **kwargs):
        # Delete the icon file when the Category instance is deleted
        if self.icon:
            if os.path.exists(self.icon.path):
                os.remove(self.icon.path)
        super().delete(*args, **kwargs)


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='servers_owner')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='servers_category')
    description = models.CharField(max_length=250, null=True, blank=True)
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="server_member")

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='channel_server')
    topic = models.CharField(max_length=150)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='channels_owner',)
    icon = models.ImageField(null=True,
                             blank=True,
                             upload_to=channel_icon_upload_path,
                             validators=[validate_icon_extension,
                                         validate_icon_size]
                             )
    banner = models.ImageField(
        null=True,
        blank=True,
        upload_to=channel_banner_upload_path,
        validators=[validate_icon_extension,]
    )

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        # Check if the instance already exists in the database
        if self.pk:
            try:
                # Retrieve the existing instance from the database
                existing_instance = get_object_or_404(Channel, pk=self.pk)
                # Compare the existing icon with the new icon
                if existing_instance.icon and existing_instance.icon != self.icon:
                    # Delete the old icon file
                    existing_instance.icon.delete(save=False)
                if existing_instance.banner and existing_instance.banner != self.banner:
                    # Delete the old banner file
                    existing_instance.banner.delete(save=False)

            except Category.DoesNotExist:
                pass
        super().save(*args, **kwargs)  # Call the real save() method

        # super(Channel, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        # Delete the icon file when the Channel instance is deleted
        if self.icon:
            if os.path.exists(self.icon.path):
                os.remove(self.icon.path)
        if self.banner:
            if os.path.exists(self.banner.path):
                os.remove(self.banner.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
