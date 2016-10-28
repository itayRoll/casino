from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from . import utils, macros


class Gambler(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	favourite_team = models.ForeignKey('Team', null=True, on_delete=models.CASCADE)
	date_joined = models.DateTimeField(default=timezone.now(), editable=False)

	def __str__(self):
		return '{0}'.format(self.user.username)


class League(models.Model):
	name = models.CharField(max_length=28, blank=False, default='-')
	api_id = models.IntegerField()
	curr_matchday = models.IntegerField(default=0)


	def init_teams(self):
		r = utils.api_call(suffix='competitions/{0}/teams'.format(self.api_id))
		teams = r.json()['teams']
		for dct in teams:
			try:
				Team.objects.get(api_id=int(dct['id']))
			except:
				t = Team(api_id= int(dct['id']), name=dct['name'].replace(' FC', ''), img_url=dct['crestUrl'])
				t.save()


	def update_fixtures(self):
		"""
		First, fetch fixtures for current match day using external API call
		Then, create DB entries or update existing ones according to returned data
		"""
		# self.update_matchday()
		r = utils.api_call(suffix='competitions/{0}/fixtures'.format(self.api_id), matchday=self.curr_matchday)
		data = r.json()
		if data['count'] > 20:
			return False
		fixtures = data['fixtures']
		for d in fixtures:
			home = Team.objects.get(api_id=int(d['homeTeamId']))
			away = Team.objects.get(api_id=int(d['awayTeamId']))
			match_start = d['date']
			dt = datetime.strptime(match_start, '%Y-%m-%dT%H:%M:%SZ')
			comp = Competition.objects.filter(league__api_id=self.api_id, home_team__api_id=home.api_id, away_team__api_id=away.api_id)
			if comp:
				comp = comp[0]
				comp.start_time = dt
			else:
				comp = Competition(start_time=dt, home_team=home, away_team=away, league=self)
			comp.save()
		return True


	def update_teams_md_fixtures(self):
		r = utils.api_call(suffix='competitions/{0}/leagueTable'.format(self.api_id))
		data = r.json()
		self.curr_matchday = int(data['matchday'])
		self.save()
		x = self.update_fixtures()
		for dct in data['standing']:
			team = Team.objects.get(api_id=int(dct['teamId']))
			team.rank = int(dct['rank'])
			team.played_games = int(dct['playedGames'])
			team.points = int(dct['points'])
			team.goals = int(dct['goals'])
			team.goals_against = int(dct['goalsAgainst'])
			team.save()
			# team.init_form()
		self.save()


	def __str__(self):
		return self.name


# class Group(models.Model):
# 	name = models.CharField(max_length=30, blank=True)
# 	bets = models.ManyToManyField('Bet')
# 	num_gamblers = models.IntegerField(default=0)
# 	admins = models.ManyToManyField('Gambler')


class Competition(models.Model):
	start_time = models.DateTimeField()
	home_team = models.ForeignKey('Team', null=True, related_name='home_team', on_delete=models.CASCADE)
	away_team = models.ForeignKey('Team', null=True, related_name='away_team', on_delete=models.CASCADE)
	league = models.ForeignKey('League', null=True)
	bets = models.ManyToManyField('Bet')


	def __str__(self):
		return '{0} vs. {1}'.format(self.home_team, self.away_team)


	def get_match_distribution(self):
		bets = Bet.objects.filter(match__pk=self.pk)
		total_cnt = len(bets)*1.0
		d = {}
		d['1'] = d['X'] = d['2'] = 0
		for bet in bets:
			d[bet.res] += 1
		try:
			return str(100*d['1']/total_cnt), str(100*d['X']/total_cnt), str(100*d['2']/total_cnt)
		except:
			return 'no bets'


class Bet(models.Model):
	def limit_competitions_choices():
		return {'start_time__gt': timezone.now()}
	RESULTS = (
		('1', 'HOME WIN'),
		('X', 'DRAW'),
		('2', 'AWAY WIN'),
	)
	creator = models.ForeignKey('Gambler', null=True, on_delete=models.CASCADE)
	# match = models.ForeignKey('Competition', limit_choices_to=limit_competitions_choices)
	match = models.ForeignKey('Competition', on_delete=models.CASCADE)
	res = models.CharField(max_length=1, choices=RESULTS, blank=False)
	last_modified = models.DateTimeField(default=timezone.now())
	creation_time = models.DateTimeField(default=timezone.now(), editable=False)

	def validation(self):
		# placing a bet is only valid up to 5 minutes befote start time
		diff = self.match.start_time - timezone.now()
		minutes_diff = diff.seconds/60 + diff.days*24*60
		if not minutes_diff > 5:
			return False
		return True

	def save(self, *args, **kwargs):
		if not self.pk:
			self.creation_time = timezone.now()
		self.last_modified = timezone.now()
		return super(Bet, self).save(*args, **kwargs)

	def hidden_res(self):
		return '{0} , {1}-{2}-{3} starting at {4}:{5}'.format(self.match,
				self.match.start_time.year, self.match.start_time.month, self.match.start_time.day,
				self.match.start_time.hour, self.match.start_time.minute)

	def shown_res(self):
		return '{0} | {1}'.format(self.hidden_res(), self.res)

	def __str__(self):
		return '{0}'.format(self.pk)


class Team(models.Model):
	api_id = models.IntegerField()
	name = models.CharField(max_length=40, blank=False)
	img_url = models.URLField(max_length=200)
	rank = models.IntegerField(default=0)
	played_games = models.IntegerField(default=0)
	points = models.IntegerField(default=0)
	goals = models.IntegerField(default=0)
	goals_against = models.IntegerField(default=0)
	form = models.CharField(max_length=5, blank=True)

	def __str__(self):
		return ('%s' % self.name).encode('ascii', 'replace')

	def init_form(self):
		r = utils.api_call(suffix='teams/{0}/fixtures'.format(self.api_id), season=2016)
		data = r.json()
		try:
			md = Competition.objects.filter(home_team__api_id=self.api_id)[0].league.curr_matchday
		except:
			md = Competition.objects.filter(away_team__api_id=self.api_id)[0].league.curr_matchday
		form = []
		num_iter = min(md, macros.TEAM_FORM_HISTORY_NUM)
		for i in range(num_iter):
			try:
				dct = data['fixtures'][md + i - num_iter - 1]
			except:
				dct = data['fixtures'][md + i - num_iter]
			if dct['status'] == 'FINISHED':
				home_goals = dct['result']['goalsHomeTeam']
				away_goals = dct['result']['goalsAwayTeam']
				is_home = dct['homeTeamName'] == self.name
				if home_goals > away_goals:
					if is_home:
						form.append('W')
					else:
						form.append('L')
				elif home_goals == away_goals:
					form.append('D')
				else:
					if is_home:
						form.append('L')
					else:
						form.append('W')
			else:
				break
		if len(form) > macros.TEAM_FORM_HISTORY_NUM:
			self.form = ''.join(form[1:])
		else:
			self.form = ''.join(form)
		self.save()


class ActivationKey(models.Model):
	creation_time = models.DateTimeField(default=timezone.now(), editable=False)
	key = models.CharField(max_length=macros.ACTIVATION_KEY_LENGTH, blank=True)
	username = models.CharField(max_length=40, blank=True)
	email = models.EmailField(max_length=70, blank=True)
	password = models.CharField(max_length=30, blank=True)

	def activate_user(self):
		user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
		g = Gambler(user=user)
		g.save()
		un = self.username
		p = self.password
		self.delete()
		return un, p