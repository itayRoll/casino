from django.shortcuts import render, get_object_or_404
from .models import Bet
from django.utils import timezone
from .forms import BetForm
from django.shortcuts import redirect
# import requests, json
# from django.http import HttpResponse

# ONLY_FUTURE_GAMES = False
# SOCCER_BASE_LINK = 'http://api.football-data.org/v1/teams/66'
# API_TOKEN = 'd7034c57f4e44668b70e05f40765b961'

# def fetch_games(request):
# 	headers = { 
# 		'X-Auth-Token': API_TOKEN,
# 		'X-Response-Control': 'minified'
# 	}
# 	r = requests.get(SOCCER_BASE_LINK, headers=headers)
# 	data = r.json()
# 	return HttpResponse(data['squadMarketValue'])


def bet_list(request):
	# if ONLY_FUTURE_GAMES:
	# 	bets = Bet.objects.filter(match__start_time__gte=timezone.now()).order_by('-last_modified')
	# else:
	# 	bets = Bet.objects.all().order_by('-last_modified')
	bets = Bet.objects.all().order_by('-last_modified')
	return render(request, 'casino/bet_list.html', {'bets': bets})

def bet_details(request, pk):
	bet = get_object_or_404(Bet, pk=pk)
	return render(request, 'casino/bet_details.html', {'bet': bet})

def bet_new(request):
	if not request.user.is_authenticated():
		return redirect('bet_list') # temp! redirect to custom page "you must be logged in to place a bet"
	if request.method == 'POST':
		form = BetForm(request.POST)
		if form.is_valid():
			bet = form.save(commit=False)
			bet.creator = request.user
			t = timezone.now()
			bet.creation_time = t
			bet.last_modified = t
			bet.save()
			return redirect('bet_details', pk=bet.pk)
	else:
		form = BetForm()
	return render(request, 'casino/bet_edit.html', {'form': form})

def bet_edit(request, pk):
    bet = get_object_or_404(Bet, pk=pk)
    if request.method == "POST":
        form = BetForm(request.POST, instance=bet)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.creator = request.user
            t = timezone.now()
            bet.last_modified = t
            bet.creation_time = t
            bet.save()
            return redirect('bet_details', pk=bet.pk)
    else:
        form = BetForm(instance=bet)
    return render(request, 'casino/bet_edit.html', {'form': form})