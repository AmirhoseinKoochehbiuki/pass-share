from django.db import models
from user.models import User
from django_cryptography.fields import encrypt


class PassBox(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name='passwords')
    pass_code = encrypt(models.CharField(max_length=255, null=False))
    target = models.URLField(max_length=255, null=False)

    class Meta:
        unique_together = ['owner', 'target']

    def __str__(self) -> str:
        return f'{self.owner} -> {self.target}'


class ShareList(models.Model):
    pass_code = models.ForeignKey(
        PassBox, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = ['pass_code', 'user']

    def __str__(self) -> str:
        return f'{self.pass_code.id} shared with {self.user.first_name}'
