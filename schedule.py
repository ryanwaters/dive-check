import sys
import os
import moment
from app import User
from msw.get_conditions import get_report
from twilio.rest import Client


ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTHTOKEN = os.environ.get('AUTHTOKEN')
TWILIO_PHONE_NUM = os.environ.get('TWILIO_PHONE_NUM')

client = Client(ACCOUNT_SID, AUTHTOKEN)

def send_message(number, timestamp, location):
	text = 'Looks like a great day to dive in %s on ' % location
	date = moment.unix(timestamp, utc=True).format('dddd, MMMM D')

	try:
		message = client.messages.create(
			to    = number,
			from_ = TWILIO_PHONE_NUM,
			body  = text + date
		)
	except Exception as e:
		print "Unknown Exception: ", e.msg


def get_user_data():
	users = User.query.all()
	user_data = []
	for user in users:
		user_data.append([user.phone, user.max_wave_height])
	return user_data

def validate_reports(sonoma, mendo):
	user_data = get_user_data()
	sonoma_alerts = []
	mendo_alerts = []
	for report in sonoma:
		forecast_max = report['swell']['components']['primary']['height']
		for user in user_data:
			user_max = user[1]
			user_phone = user[0]
			if user_max <= forecast_max:
				sonoma_alerts.append([user_phone, report['localTimestamp']])

	for report in mendo:
		forecast_max = report['swell']['components']['primary']['height']
		for user in user_data:
			user_max = user[1]
			user_phone = user[0]
			if user_max <= forecast_max:
				mendo_alerts.append([user_phone, report['localTimestamp']])

	return sonoma_alerts, mendo_alerts

if __name__ == '__main__':
	# Get forecast reports from MSW
	sonoma = [get_report(305)[2], get_report(305)[10], get_report(305)[18], get_report(305)[26], get_report(305)[34]]
	mendo = [get_report(303)[2], get_report(303)[10], get_report(303)[18], get_report(303)[26], get_report(303)[34]]

	# Check user swell preference against forecasted swell
	sonoma_alerts, mendo_alerts = validate_reports(sonoma, mendo)
	
	# Loop through all alerts and send using Twilio
	if sonoma_alerts:
		for user in sonoma_alerts:
			send_message(user[0], user[1], 'Sonoma')
	if mendo_alerts:
		for user in mendo_alerts:
			send_message(user[0], user[1], 'Mendocino')

