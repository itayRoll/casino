from django import forms
from .models import Bet, Competition

class BetForm(forms.ModelForm):
	
	class Meta:
		model = Bet
		fields = ('res', 'match')
