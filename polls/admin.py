from django.contrib import admin

from .models import RatingSubject, RatingRecord


class RatingSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'credits', 'enabled')
    list_filter = ['subject']
    search_fields = ['subject']


class RatingRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'rating')
    list_filter = ['user']
    search_fields = ['user']


admin.site.register(RatingSubject, RatingSubjectAdmin)
admin.site.register(RatingRecord, RatingRecordAdmin)
admin.site.site_header = "Rating Admin"
