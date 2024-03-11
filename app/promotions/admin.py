from import_export.admin import ExportMixin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin

from import_export import resources, fields

from app.promotions.models import Promotion, PromotionCode


@admin.register(Promotion)
class PromotionAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'mask', 'start_date', 'end_date', 'is_active')
    date_hierarchy = 'start_date'  # Add date hierarchy for start_date

    fieldsets = (
        (_("Основная информация"), {
            'fields': ('name', 'description', 'is_active', "mask", "conditions"),
        }),
        (_("Даты проведения"), {
            'fields': ('start_date', 'end_date'),
        }
         )
    )


class PromotionCodeResource(resources.ModelResource):
    user_phone = fields.Field(column_name='Телефон номер', attribute='user__phone/')
    user_name = fields.Field(column_name='ФИО', attribute='user__fullname/')
    promotion_name = fields.Field(column_name='Название акции', attribute='promotion__name/')

    class Meta:
        model = PromotionCode
        fields = ('code', 'user_phone', 'promotion_name', 'created_at')

    def dehydrate_user_phone(self, code):
        return code.user.phone

    def dehydrate_user_name(self, code):
        return code.user.fullname

    def dehydrate_promotion_name(self, code):
        return code.promotion.name


@admin.register(PromotionCode)
class PromotionCodeAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PromotionCodeResource
    list_display = ['code', 'user', 'promotion', 'created_at']
    date_hierarchy = 'created_at'
    list_filter = ['promotion']
    search_fields = ("code",)

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_delete_permission(self, request, obj=...):
    #     return False
    #
    # def has_change_permission(self, request, obj=...):
    #     return False
