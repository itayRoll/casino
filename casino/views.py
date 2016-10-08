from django.shortcuts import render, get_object_or_404
from .models import Bet
from django.utils import timezone

def bet_list(request):
	# bets = Bet.objects.filter(match__start_time__gte=timezone.now()).order_by('match__start_time')
	bets = Bet.objects.all()
	return render(request, 'casino/bet_list.html', {'bets': bets})

def bet_details(request, pk):
	bet = get_object_or_404(Bet, pk=pk)
	return render(request, 'casino/bet_details.html', {'bet': bet})