from django.shortcuts import render
from .models import Bet
from django.utils import timezone

def bet_list(request):
	# bets = Bet.objects.filter(match__start_time__gte=timezone.now()).order_by('match__start_time')
	bets = Bet.objects.all()
	return render(request, 'casino/bet_list.html', {'bets': bets})