from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_size(image):
    if image:
        with Image.open(image) as img:
            width, height = img.size
            if width > 70 or height > 70:
                raise ValidationError(
                    f"The maximum dimensions allowed for the image  are 70x70 - size of image you uploaded is{img.size}")

# Validate icon file extension


def validate_icon_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    if ext.lower() not in valid_extensions:
        raise ValidationError(('Invalid file extension. Only JPG, JPEG, PNG, and GIF files are allowed.'),
                              code='invalid_extension'
                              )
