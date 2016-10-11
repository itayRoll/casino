from django import forms
from .models import Bet, Competition

class BetForm(forms.ModelForm):
	
	class Meta:
		model = Bet
		fields = ('match', 'res')

	def is_valid(self):
		if not super(BetForm, self).is_valid():
			return False
		if not self.instance.validation():
			return False
		return True