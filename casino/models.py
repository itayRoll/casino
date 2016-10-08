from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.

class Competition(models.Model):
	start_time = models.DateTimeField()
	home_team = models.CharField(blank=False, max_length=40)
	away_team = models.CharField(blank=False, max_length=40)

	def update_start_time(self, month, day, hour, minute):
		# admin permissions
		self.start_time.replace(month=month, day=day, hour=hour, minute=minute)
		self.save()


class Bet(models.Model):
	RESULTS = (
		('1', 'HOME-WIN'),
		('X', 'TIE'),
		('2', 'AWAY-WIN'),
	)
	creator = models.ForeignKey('auth.User')
	time_created = models.DateTimeField(editable=False) 	# maybe redubndant
	last_modified = models.DateTimeField()
	match = models.ForeignKey('Competition')
	res = models.CharField(max_length=1, choices=RESULTS, blank=False)

	def bet_validation(self):
		# placing a bet is only valid up to 5 minutes befote start time
		diff = self.match.start_time - timezone.now()
		minutes_diff = diff.seconds/60 + diff.days*24*60
		if not minutes_diff > 5:
			return False
		return True

	def place_bet(self):
		if self.bet_validation():
			self.save()
		else:
			# invalid bet - notify
			pass

	def save(self, *args, **kwargs):
		# on save, update last modeified field
		if not self.id:
			self.time_created = timezone.now()
		self.last_modified = timezone.now()
		return super(User, self).save(*args, **kwargs)
