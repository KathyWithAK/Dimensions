#
# This sets up how models are displayed
# in the web admin interface.
#
from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from world.space.models import SpaceDB as Space
from world.space.models import SpaceContactDB as SpaceContact

#from . import utils as adminutils

# see: evennia\evennia\web\admin\objects.py
# see: https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
# 2024.06.08 - This is not yet working

class SpaceCreateForm(forms.ModelForm):
    """
    This form details the look of the fields.

    """
    class Meta(object):
        model = Space
        fields = "__all__"

    db_key = forms.CharField(
        label="Key",
        widget=forms.TextInput(attrs={"size": "78"}),
        help_text="",
    )
    db_category = forms.CharField(
        label="Category",
        widget=forms.TextInput(attrs={"size": "78"}),
        help_text="",
    )
    db_name= forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={"size": "78"}),
        help_text="",
    )

    def __init__(self, *args, **kwargs):
        """
        Tweak some fields dynamically.

        """
        super().__init__(*args, **kwargs)    

class SpaceEditForm(SpaceCreateForm):
    """
    Form used for editing. Extends the create one with more fields

    """

    class Meta:
        model = Space
        fields = "__all__"

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    """
    Describes the admin page for Space Objects.

    """
    list_display = (
        "id",
        "db_key",
        "db_category",
    )
    list_display_links = ("id", "db_key")
    ordering = ["-id"]
    raw_id_fields = ("db_transmat", "db_dock_room", "db_item_id")
    readonly_fields = ()

    save_as = False
    save_on_top = False
    list_select_related = False
    view_on_site = False
    list_filter = ("db_category",)

    # editing fields setup

    form = SpaceEditForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("db_key", "db_category"),
                    ("db_name"),
                )
            },
        ),
    )

    add_form = SpaceCreateForm
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    ("db_key", "db_category"),
                    ("db_name"),
                )
            },
        ),
    )

    def serialized_string(self, obj):
        """
        Get the serialized version of the object.

        """
        from evennia.utils import dbserialize

        return str(dbserialize.pack_dbobj(obj))

    serialized_string.help_text = (
        "Copy & paste this string into an Attribute's `value` field to store this object there."
    )

    def get_fieldsets(self, request, obj=None):
        """
        Return fieldsets.

        Args:
            request (Request): Incoming request.
            obj (Object, optional): Database object.
        """
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during creation.

        Args:
            request (Request): Incoming request.
            obj (Object, optional): Database object.

        """
        help_texts = kwargs.get("help_texts", {})
        help_texts["serialized_string"] = self.serialized_string.help_text
        kwargs["help_texts"] = help_texts

        defaults = {}
        if obj is None:
            defaults.update(
                {"form": self.add_form, "fields": flatten_fieldsets(self.add_fieldsets)}
            )
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "account-object-link/<int:pk>",
                self.admin_site.admin_view(self.link_object_to_account),
                name="object-account-link",
            )
        ]
        return custom_urls + urls

    def save_model(self, request, obj, form, change):
        """
        Model-save hook.

        Args:
            request (Request): Incoming request.
            obj (Object): Database object.
            form (Form): Form instance.
            change (bool): If this is a change or a new object.

        """
        if not change:
            # adding a new object
            # have to call init with typeclass passed to it
            obj.set_class_from_typeclass(typeclass_path=obj.db_typeclass_path)
            obj.save()
            obj.basetype_setup()
            obj.basetype_posthook_setup()
            obj.at_object_creation()
        else:
            obj.save()
            obj.at_init()

    def response_add(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        return HttpResponseRedirect(reverse("admin:objects_objectdb_change", args=[obj.id]))
