from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Bet)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(ActivationKey)
admin.site.register(Gambler)

class BetInline(admin.TabularInline):
	model = Competition.bets.through

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
	inlines = (BetInline,)
	exclude = ('bets',)