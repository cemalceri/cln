from django.contrib import admin


#
# @admin.register(models.RezervasyonModel)
# class EventAdmin(admin.ModelAdmin):
#     model = models.RezervasyonModel
#     list_display = [
#         "id",
#         "title",
#         "user",
#         "is_active",
#         "is_deleted",
#         "created_at",
#         "updated_at",
#     ]
#     list_filter = ["is_active", "is_deleted"]
#     search_fields = ["title"]
#
#
# @admin.register(models.EtkinlikMember)
# class EventMemberAdmin(admin.ModelAdmin):
#     model = models.EtkinlikMember
#     list_display = ["id", "event", "user", "created_at", "updated_at"]
#     list_filter = ["event"]
from calendarapp.models.Enums import SaatlerModel, GunlerModel
from calendarapp.models.concrete.abonelik import PaketModel, UyeAbonelikModel, UyePaketModel
from calendarapp.models.concrete.commons import OkulModel
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.kort import KortModel
from calendarapp.models.concrete.uye import UyeModel, UyeGrupModel, GrupModel

admin.site.register(EtkinlikModel)
admin.site.register(UyeModel)
admin.site.register(UyeGrupModel)
admin.site.register(KortModel)
admin.site.register(GunlerModel)
admin.site.register(SaatlerModel)
admin.site.register(GrupModel)
admin.site.register(PaketModel)
admin.site.register(UyeAbonelikModel)
admin.site.register(OkulModel)
admin.site.register(UyePaketModel)
