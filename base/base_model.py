import uuid
from django.db import models

"""
This BaseModel is used for all models in the project.
"""
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuidv4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

