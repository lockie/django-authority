from django import forms
from django.utils.translation import gettext_lazy as _

from authority.forms import UserPermissionForm


class SpecialUserPermissionForm(UserPermissionForm):
    user = forms.CharField(label=_("Special user"), widget=forms.Textarea())
