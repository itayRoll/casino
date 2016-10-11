from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from . import utils


class League(models.Model):
	api_id = models.IntegerField()
	curr_matchday = models.IntegerField()


	def update_matchday(self):
		r = utils.api_call(suffix='competitions/{0}/'.format(self.api_id))
		data = r.json()
		matchday = int(data['currentMatchday'])
		if matchday != self.curr_matchday:
			self.curr_matchday = matchday
			self.save()


	def update_fixtures(self):
		"""
		First, fetch fixtures for current match day using external API call
		Then, create DB entries or update existing ones according to returned data
		"""
		self.update_matchday()
		r = utils.api_call(suffix='competitions/{0}/fixtures', params={'matchDay': self.curr_matchday})
		data = r.json()
		fixtures = data['fixtures']
		for k, d in fixtures.iteritems():
			match_start = d['date']
			dt = datetime.strptime(match_start, '%Y-%m-%dT%H:%M:%SZ')
			comp = Competition.objects.filter(league__api_id=self.api_id, home_team=self.home_team, away_team=self.away_team)
			if comp:
				comp = comp[0]
				comp.start_time = dt
			else:
				comp = Competition(start_time=dt, home_team=d['homeTeamName'], away_team=d['awayTeamName'], league=self)
			comp.save()



class Competition(models.Model):
	start_time = models.DateTimeField()
	home_team = models.CharField(blank=False, max_length=40)
	away_team = models.CharField(blank=False, max_length=40)
	league = models.ForeignKey('League', null=True)

	def update_start_time(self, month, day, hour, minute):
		# admin permissions
		self.start_time.replace(month=month, day=day, hour=hour, minute=minute)
		self.save()

	def __str__(self):
		return '{0} vs. {1}'.format(self.home_team, self.away_team)


class Bet(models.Model):

	def limit_competitions_choices():
		return {'start_time__gt': timezone.now()}

	RESULTS = (
		('1', 'HOME-WIN'),
		('X', 'TIE'),
		('2', 'AWAY-WIN'),
	)
	creator = models.ForeignKey(User)
	time_created = models.DateTimeField(editable=False, default=timezone.now()) 	# maybe redubndant
	last_modified = models.DateTimeField(default=timezone.now())
	match = models.ForeignKey('Competition', limit_choices_to=limit_competitions_choices)
	res = models.CharField(max_length=1, choices=RESULTS, blank=False)

	def validation(self):
		# placing a bet is only valid up to 5 minutes befote start time
		diff = self.match.start_time - timezone.now()
		minutes_diff = diff.seconds/60 + diff.days*24*60
		if not minutes_diff > 5:
			return False
		return True

	def save(self, *args, **kwargs):
		if not self.id:
			self.time_created = timezone.now()
		self.last_modified = timezone.now()
		return super(Bet, self).save(*args, **kwargs)

	def hidden_res(self):
		return '{0} , {1}-{2}-{3} starting at {4}:{5}'.format(self.match,
				self.match.start_time.year, self.match.start_time.month, self.match.start_time.day,
				self.match.start_time.hour, self.match.start_time.minute)

	def shown_res(self):
		return '{0} | {1}'.format(self.hidden_res(), self.res)
