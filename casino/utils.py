import requests
from . import macros
# def send_mail():
# 	TODO


def api_call(suffix, **params):
	url = 'http://api.football-data.org/v1/' + suffix
	headers = { 
		'X-Auth-Token': 'd7034c57f4e44668b70e05f40765b961',
		'X-Response-Control': 'minified'
	}
	response = requests.get(url, headers=headers, params=params)
	return response
