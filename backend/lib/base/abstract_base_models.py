from django.db import models


class AuditableBaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=50, null=False)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    deleted_by = models.CharField(max_length=50, null=True, blank=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id!r}>'
