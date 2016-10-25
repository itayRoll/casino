from django.shortcuts import render, get_object_or_404
from .models import Bet, Competition, League, Team, ActivationKey, Gambler
from django.utils import timezone
from .forms import BetForm
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import macros
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django_tables2 import RequestConfig
from .tables import CompetitionTable
import json
# from django.views.decorators.csrf import csrf_exempt



def index(request):
	# allow access only if user is not logged in already
	if request.user.is_authenticated():
		return HttpResponseRedirect('/feed/')
	return render(request, 'casino/login.html', {})


def clean_db(request):
	bets = Bet.objects.all()
	for b in bets:
		b.delete()
	leagues = League.objects.all()
	for l in leagues:
		l.delete()
	comps = Competition.objects.all()
	for c in comps:
		c.delete()
	teams = Team.objects.all()
	for t in teams:
		t.delete()
	return HttpResponse('ss')


def login_page(request):
	# allow access only if user is not logged in already
	if request.user.is_authenticated():
		return HttpResponseRedirect('/bet/')
	return render(request, 'casino/login.html', {})


def init_teams(request):
	for league in League.objects.all():
		league.init_teams()
	return HttpResponse('success')


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


def signup_page(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/bet/')
	return render(request, 'casino/signup.html', {})


def register_user(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/bet/')
	if request.POST:
		username=request.POST['username']
		password=request.POST['password']
		email=request.POST['email']
		if User.objects.filter(email=email):
			# error - email already exists
			return HttpResponse('shit')
		key = get_random_string(length=macros.ACTIVATION_KEY_LENGTH)
		ak = ActivationKey(username=username, password=password, email=email, key=key)
		ak.save()
		# TODO: async send confirmation mail
		return HttpResponse('Login to your email address to confirm registration.')
	return render(request, 'casino/login.html', {})


def clean_activation_keys(request):
	"""
	Deletes old activation keys
	"""
	keys = ActivationKey.objects.all()
	now = timezone.now()
	for key in keys:
		d2 = key.creation_time
		monday1 = (now - timedelta(days=now.weekday()))
		monday2 = (d2 - timedelta(days=d2.weekday()))
		if (monday2 - monday1).days / macros.ACTIVATION_KEY_LIFE_EXPECTENCY != 0:
			key.delete()
	return HttpResponse('success!')


def fetch_games(request):
	"""
	Performs a daily check on competitions
	Saves new, modifies exisiting ones
	"""
	leagues = League.objects.all()
	for league in leagues:
		league.update_teams_md_fixtures()
	return HttpResponse('success')
	# err_lst = [league for league in leagues if not league.update_fixtures()]
	# if not err_lst:
	# 	return HttpResponse('success!')
	# return HttpResponse('Failed fetching games for the following:<br>{0}'.format(', '.join(err_lst)))


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


@login_required(login_url='/login/')
def populate_user_feed(request):
	user_bets = Bet.objects.filter(creator__user__username=request.user.username)
	user_comps = [b.match for b in user_bets]
	all_comps = Competition.objects.all()
	# all_comps = Competition.objects.filter(start_time__gt=timezone.now())
	# feed_comps = [c for c in all_comps if c not in user_comps]
	feed_comps = all_comps
	# feed_comps.sort(key=lambda c: c.start_time)
	# feed_comps now contains all competitions that the user hasn't placed a bet on
	return render(request, 'casino/feed.html', {'comps': feed_comps})


@login_required(login_url='/login/')
def user_page(request):
	return render(request, 'casino/userpage.html', {})


@login_required(login_url='/login/')
def ext_user_page(request, pk):
	user = get_object_or_404(User, pk=pk)
	return render(request, 'casino/extuserpage.html', {})


@login_required(login_url='/login/')
def team_page(request, pk):
	team = Team.objects.get(pk=pk)
	return render(request, 'casino/teampage.html', {'team': team})


def init_form(request):
	teams = Team.objects.all()
	for team in teams:
		team.init_form()
	return HttpResponse('success')


def activate_user(request, activation_key):
	try:
		key = ActivationKey.objects.get(key=activation_key)
	except:
		# wrong activation key - return error
		return HttpResponse('Wrong activation key. Go fuck yourself.')
	un, p = key.activate_user()
	user = authenticate(username=un, password=p)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect('/feed/')
	return render(request, 'casino/login.html', {'err_msg': macros.WRONG_ACTIVATION_KEY})

# @csrf_exempt
@login_required(login_url='/login/')
def place_bet(request):
	r = request.POST['bet']
	try:
		c = Competition.objects.get(pk=int(request.POST['match_pk']))
		g = Gambler.objects.get(user__username=request.user.username)
	except:
		return HttpResponse('Failure')
	try:
		similar_bet = Bet.objects.get(creator__user__username=g.user.username, match__pk=c.pk)
		if similar_bet.res != r:
			similar_bet.res = r
			similar_bet.save()
	except:
		b = Bet(creator=g, match=c, res=r)
		b.save()
	return HttpResponse('success')


@login_required(login_url='/login/')
def match_distribution(request):
	match_pk = int(request.POST['match_pk'])
	try:
		comp = Competition.objects.get(pk=match_pk)
	except:
		return HttpResponse('failure')
	dist = comp.get_match_distribution()
	data = {'x': ', '.join(dist)}
	return HttpResponse(json.dumps(data), content_type='application/json')