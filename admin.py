from familytree.models import *
from django.contrib import admin
class PersonAdmin(admin.ModelAdmin):
	list_display = (('firstname', 'surname', 'DOB'))
	fieldsets = (('Creation Info', {'fields': ('author', 'created_date')}),
		('Names', {'fields': (('firstname', 'surname', 'maidenname'), ('middlename1','middlename2'))}),
		('No clue what to call this', {'fields': (('sex', 'DOB', 'DOD'))}),
		('Relations', {'fields': (('parents', 'siblings'),('partners','children'))}),
		('Advanced options', {'classes': ('collapse',),'fields': ('notes', 'familypictures')}),
	)

admin.site.register(Note)
admin.site.register(Familypicture)
admin.site.register(Person, PersonAdmin)

