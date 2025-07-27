from django.db import models
from django.contrib.auth.models import User

from cmms.models import SysUser

class Notification(models.Model):
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.fullName}: {self.message[:50]}"