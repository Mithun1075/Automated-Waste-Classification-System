from django.db import models
from django.contrib.auth.models import User


# -------------------------------
# Profile Model → Extends default Django User model
# -------------------------------
class Profile(models.Model):
    # One-to-one link with the built-in User model (each user has exactly one profile)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional details for the user
    dob = models.DateField(null=True, blank=True)  # Date of Birth (optional)
    state = models.CharField(max_length=100, null=True, blank=True)  # User's state (optional)

    # String representation in Django admin or shell
    def __str__(self):
        return f"{self.user.username} - {self.state}"


# -------------------------------
# WasteRecord Model → Stores uploaded waste images + predictions
# -------------------------------
class WasteRecord(models.Model):
    # Link to the user who uploaded the image
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Uploaded waste image file → saved under MEDIA_ROOT/waste_images/
    image = models.ImageField(upload_to='waste_images/')

    # Predicted waste type (Plastic, Paper, etc.)
    waste_type = models.CharField(max_length=50)

    # Auto-stores the date when the record was created
    created_at = models.DateField(auto_now_add=True)

    # String representation (example: "mithun - Plastic")
    def __str__(self):
        return f"{self.user.username} - {self.waste_type}"
