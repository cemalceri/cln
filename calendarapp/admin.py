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
from calendarapp.models.concrete.etkinlik import EtkinlikModel
from calendarapp.models.concrete.musteri import MusteriModel
from calendarapp.models.member.etkinlik_member import EtkinlikMember

admin.site.register(EtkinlikModel)
admin.site.register(EtkinlikMember)
admin.site.register(MusteriModel)
