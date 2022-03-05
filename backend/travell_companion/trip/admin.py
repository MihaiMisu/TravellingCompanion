from django.contrib.admin import site, ModelAdmin

from .models import Trip, User, TripCompanion


class UserAdmin(ModelAdmin):
    list_display = ('user_name', 'email')
    readonly_fields = ('user_id', 'created_at', 'updated_at')

    def user_name(self, obj):
        return obj.name
    user_name.short_description = 'User name'


class TripAdmin(ModelAdmin):
    list_display = ('name', 'starting_time', 'duration', 'cost_estimation')
    readonly_fields = ('created_at', 'updated_at')


class TripCompanionAdmin(ModelAdmin):
    list_display = ('trip_name', 'user_name')
    readonly_fields = ('created_at', 'updated_at')

    def trip_name(self, obj):
        return obj.trip_id
    trip_name.short_description = 'Trip name'

    def user_name(self, obj):
        return obj.user_id
    user_name.short_description = 'User name'


site.register(User, UserAdmin)
site.register(Trip, TripAdmin)
site.register(TripCompanion, TripCompanionAdmin)
