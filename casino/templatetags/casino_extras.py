from django import template
import time, datetime

register = template.Library()

@register.filter(name='get_comp_users')
def get_comp_users(bets, username):
	l = len(bets)
	if l==0:
		return ''
	lst = [b.creator.user.username for b in bets if b.creator.user.username != username]
	if len(lst) == l:
		if l > 2:
			return '{0} and {1} others already placed a bet.'.format(lst[0], l-1)
		elif l == 2:
			return '{0} already placed a bet.'.format(' and '.join(lst))
		else:
			return 'Only {0} placed a bet.'.format(lst[0])
	else:
		if l > 2:
			return '{0} and {1} others already placed a bet.'.format('You', l-1)
		elif l == 2:
			return 'You and {0} already placed a bet.'.format(lst[0])
		else:
			return 'Only {0} placed a bet.'.format('You')


@register.filter(name='get_milli')
def get_milli(start):
	tt = start.timetuple()
	ts = time.mktime(tt)
	return ts*1000.0


@register.filter(name='load_buttons')
def load_buttons(bets, username):
	for b in bets:
		if b.creator.user.username == username:
			return b.res
	return '0'
