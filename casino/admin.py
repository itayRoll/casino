from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Bet)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(ActivationKey)
admin.site.register(Group)
admin.site.register(Gambler)

class GroupInline(admin.TabularInline):
	model = Competition.groups.through

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
	inlines = (GroupInline,)
	exclude = ('groups',)