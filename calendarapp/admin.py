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
# @admin.register(models.RezervasyonMember)
# class EventMemberAdmin(admin.ModelAdmin):
#     model = models.RezervasyonMember
#     list_display = ["id", "event", "user", "created_at", "updated_at"]
#     list_filter = ["event"]
from calendarapp.models.concrete.rezervasyon import RezervasyonModel
from calendarapp.models.member.rezervasyon_member import RezervasyonMember

admin.site.register(RezervasyonModel)
admin.site.register(RezervasyonMember)
