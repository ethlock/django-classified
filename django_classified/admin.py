# -*- coding:utf-8 -*-
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from django.utils.translation import get_language, ugettext_lazy as _
from ordered_model.admin import OrderedModelAdmin

from .models import Section, Group, Item, Image, Area, Profile
from .l10n.models import Country, AdminArea, AdminSubarea, Currency


class ImageInline(AdminImageMixin, admin.StackedInline):
    model = Image
    extra = 5


class ItemAdmin(OrderedModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'group', 'area', 'user', 'is_active', 'posted', 'updated', 'order', 'move_up_down_links')
    list_filter = ('area', 'group', 'is_active', 'posted',)
    search_fields = ('title', 'description', 'user__email')
    inlines = [ImageInline]
    ordering = ['order',]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group":
            kwargs["queryset"] = Group.objects.all().order_by('section__order', 'order')
        return super().formfield_for_choice_field(db_field, request, **kwargs)


class GroupAdmin(OrderedModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    list_display = ('title', 'slug', 'section', 'count', 'order', 'move_up_down_links')
    list_filter = ('section',)
    search_fields = ('title', 'section__title')
    ordering = ['order',]


class SectionAdmin(OrderedModelAdmin):
    list_display = ('title', 'order', 'move_up_down_links')
    ordering = ['order',]


class AreaAdmin(admin.ModelAdmin):

    def make_active(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            message_bit = _("1 area was")
        else:
            message_bit = _("%s areas were" % rows_updated)
        self.message_user(request, _("%s successfully marked as active") % message_bit)
    make_active.short_description = _("Mark selected areas as active")
    
    def make_inactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            message_bit = _("1 area was")
        else:
            message_bit = _("%s areas were" % rows_updated)
        self.message_user(request, _("%s successfully marked as inactive") % message_bit)
    make_inactive.short_description = _("Mark selected areas as inactive")

    list_display = (
        'title', 'admin_area', 'active',
    )
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('admin_area', 'active')
    search_fields = ('title', 'admin_area')
    actions = ('make_active', 'make_inactive')

    

# l10n admin
class AdminArea_Inline(admin.TabularInline):
    model = AdminArea
    extra = 1

class Currency_Inline(admin.TabularInline):
    model = Currency
    extra = 1

class CountryOptions(admin.ModelAdmin):
    
    def make_active(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            message_bit = _("1 country was")
        else:
            message_bit = _("%s countries were" % rows_updated)
        self.message_user(request, _("%s successfully marked as active") % message_bit)
    make_active.short_description = _("Mark selected countries as active")
    
    def make_inactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            message_bit = _("1 country was")
        else:
            message_bit = _("%s countries were" % rows_updated)
        self.message_user(request, _("%s successfully marked as inactive") % message_bit)
    make_inactive.short_description = _("Mark selected countries as inactive")
    
    list_display = ('printable_name', 'iso2_code','active')
    list_filter = ('continent', 'active')
    search_fields = ('name', 'iso2_code', 'iso3_code')
    actions = ('make_active', 'make_inactive')
    inlines = [AdminArea_Inline, Currency_Inline]

class AdminSubarea_Inline(admin.TabularInline):
    model = AdminSubarea
    extra = 1

class AdminAreaOptions(admin.ModelAdmin):
    
    def make_active(self, request, queryset):
        rows_updated = queryset.update(active=True)
        if rows_updated == 1:
            message_bit = _("1 administrative area was")
        else:
            message_bit = _("%s administrative areas were" % rows_updated)
        self.message_user(request, _("%s successfully marked as active") % message_bit)
    make_active.short_description = _("Mark selected admininstrative areas as active")
    
    def make_inactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            message_bit = _("1 administrative area was")
        else:
            message_bit = _("%s administrative areas were" % rows_updated)
        self.message_user(request, _("%s successfully marked as inactive") % message_bit)
    make_inactive.short_description = _("Mark selected administrative areas as inactive")
    
    list_display = ('name', 'country', 'active')
    list_filter = ('country', 'active')
    search_fields = ('name', 'abbrev')
    actions = ('make_active', 'make_inactive')
    inlines = [AdminSubarea_Inline]

# Profile admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'receive_news')
    
admin.site.register(Area, AreaAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Item, ItemAdmin)

admin.site.register(Country, CountryOptions)
admin.site.register(AdminArea, AdminAreaOptions)

admin.site.register(Profile, ProfileAdmin)
