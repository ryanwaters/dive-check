import requests
import sys
import os
from datetime import datetime

def get_report(spot_id):
	api_key = os.environ.get('MSW_API_KEY')
	base_url = 'http://magicseaweed.com/api/' + api_key + '/forecast/?spot_id=' + str(spot_id)
	fields = '&units=us&fields=localTimestamp,swell.*,condition.*,wind.*,charts.*'

	try:
		res = requests.get(base_url + fields)
		if res.status_code == 200:
			return res.json()
	except:
		print 'Unexpected error: ', sys.exc_info()[0]

def get_current(spot_id):
	forecast = get_report(spot_id)
	current_day = datetime.utcnow().strftime('%d')
	current_reports = []
	for report in forecast:
		forecast_day = datetime.fromtimestamp(report['localTimestamp']).strftime('%d')
		if current_day == forecast_day:
			current_reports.append(report)

	return current_reports


