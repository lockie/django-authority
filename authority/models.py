from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from authority.managers import PermissionManager

USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class Permission(models.Model):
    """
    A granular permission model, per-object permission in other words.
    This kind of permission is associated with a user/group and an object
    of any content type.
    """

    codename = models.CharField(_("codename"), max_length=100)
    content_type = models.ForeignKey(
        ContentType, related_name="row_permissions", on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey(
        USER_MODEL,
        null=True,
        blank=True,
        related_name="granted_permissions",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(
        USER_MODEL,
        null=True,
        blank=True,
        related_name="created_permissions",
        on_delete=models.CASCADE,
    )

    approved = models.BooleanField(
        _("approved"),
        default=False,
        help_text=_(
            "Designates whether the permission has been approved and treated as active. "
            "Unselect this instead of deleting permissions."
        ),
    )

    date_requested = models.DateTimeField(_("date requested"), default=datetime.now)
    date_approved = models.DateTimeField(_("date approved"), blank=True, null=True)

    objects = PermissionManager()

    def __unicode__(self):
        return self.codename

    class Meta:
        unique_together = ("codename", "object_id", "content_type", "user", "group")
        verbose_name = _("permission")
        verbose_name_plural = _("permissions")
        permissions = (
            ("change_foreign_permissions", "Can change foreign permissions"),
            ("delete_foreign_permissions", "Can delete foreign permissions"),
            ("approve_permission_requests", "Can approve permission requests"),
        )

    def save(self, *args, **kwargs):
        # Make sure the approval date is always set
        if self.approved and not self.date_approved:
            self.date_approved = datetime.now()
        super(Permission, self).save(*args, **kwargs)

    def approve(self, creator):
        """
        Approve granular permission request setting a Permission entry as
        approved=True for a specific action from an user on an object instance.
        """
        self.approved = True
        self.creator = creator
        self.save()
