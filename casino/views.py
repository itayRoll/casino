from django.shortcuts import render, get_object_or_404
from .models import Bet, Competition, League
from django.utils import timezone
from .forms import BetForm
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import macros
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
	return render(request, 'casino/login.html', {})

def login_page(request):
	# allow access only if user is not logged in already
	if request.user.is_authenticated():
		return HttpResponseRedirect('/bet/')
	return render(request, 'casino/login.html', {})


def login_user(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		next_page = request.POST['next']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if next_page != '':
					return HttpResponseRedirect(next_page)
				return HttpResponseRedirect('/bet/')
	return render(request, 'casino/login.html', {'err_msg': macros.WRONG_LOGIN})


@login_required(login_url='/login/')
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')


def fetch_games(request):
	"""
	Performs a daily check on competitions
	Saves new comps, modifies exisiting ones
	"""
	leagues = League.objects.all()
	for league in leagues:
		league.update_fixtures()
	return HttpResponse('success!')


@login_required(login_url='/login/')
def bet_list(request):
	bets = Bet.objects.all().order_by('-last_modified')
	return render(request, 'casino/bet_list.html', {'bets': bets})


@login_required(login_url='/login/')
def bet_details(request, pk):
	bet = get_object_or_404(Bet, pk=pk)
	return render(request, 'casino/bet_details.html', {'bet': bet})


@login_required(login_url='/login/')
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
			# bet is invalid - TODO: redirect to designated page
			return redirect('bet_list')
	else:
		form = BetForm()
	return render(request, 'casino/bet_edit.html', {'form': form})


@login_required(login_url='/login/')
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