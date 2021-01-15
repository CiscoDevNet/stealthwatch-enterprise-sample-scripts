#!/usr/bin/env python

import json
import sys
import random
import datetime
import time

import requests
import webexteamssdk
from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import env_lab  # noqa
import env_user # noqa

try:
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except:
	pass


# Enter all authentication info
SMC_USER = env_lab.SMC.get("username")
SMC_PASSWORD = env_lab.SMC.get("password")
SMC_HOST = env_lab.SMC.get("host")


# Perform the request to login to the SMC
def login(sw_session, data):
	
	print("\n==> Logging in to the SMC")
	url = f'https://{SMC_HOST}/token/v2/authenticate'
	response = sw_session.request("POST", url, verify=False, data=data)

	# If the login was successful
	if(response.status_code == 200):
		print(green("Login SUCCESSFUL!"))
		return True
	
	print(red(f'An error has ocurred, while trying to login to SMC, with the following code {response.status_code}'))
	return False

# Get the list of tenants (domains) from the SMC
def get_tenants(sw_session):
	
	print("\n==> Finding all Tenants available")
	url = f'https://{SMC_HOST}/sw-reporting/v1/tenants/'
	response = api_session.request("GET", url, verify=False)

	if response.status_code == 200:
		return response.content

	print(red(f'An error has ocurred, while fetching tenants (domains), with the following code {response.status_code}'))
	return None

# Create a search query for all hosts with abnormal traffic
def get_security_events(time_window=60):
	# Set the URL for the query to POST the filter and initiate the search
	url = f'https://{SMC_HOST}/sw-reporting/v1/tenants/{SMC_TENANT_ID}/security-events/queries'

	# Set the timestamps for the filters, in the correct format, for last 'time_window' minutes
	end_datetime = datetime.datetime.utcnow()
	start_datetime = end_datetime - datetime.timedelta(minutes=time_window)
	end_timestamp = end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
	start_timestamp = start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

	# Set the filter with the request data. Remember: "timeRange" is the only mandatory field.
	request_data = {
		"timeRange": {
			"from": start_timestamp,
			"to": end_timestamp
		},
		"securityEventTypeIds": [16]
	}

	# Perform the query to initiate the search
	request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
	response = api_session.request("POST", url, verify=False, data=json.dumps(request_data), headers=request_headers)

	if response.status_code == 200:
		search = json.loads(response.content)["data"]["searchJob"]
		search_id = search["id"]

		return search_id

	print(red(f"An error has ocurred, while creating search query, with the following code {response.status_code}"))
	print(red(f"{response.json()}"))
	return None

# Terminate API session and terminate token validity
def terminate_session(sw_session):
	
	uri = f'https://{SMC_HOST}/token'
	response = api_session.delete(uri, timeout=30, verify=False)

# Add the new tag (host group) in the SMC
def create_new_tag(tag_data):

	print(f"\n==> Creating new TAG named: {tag_data[0]['name']}")

	url = f'https://{SMC_HOST}/smc-configuration/rest/v1/tenants/{SMC_TENANT_ID}/tags'
	request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
	response = api_session.request("POST", url, verify=False, data=json.dumps(tag_data), headers=request_headers)

	# If successfully able to add the tag (host group)
	if (response.status_code == 200):
		print(green(f"New tag (host group) successfully added"))
		print(json.dumps(response.json(), indent=4))
		return str(response.json()['data'][0]['id'])

	# If unable to add the new tag (host group)
	print(red(f"An error has ocurred, while adding tags (host groups), with the following code {response.status_code}"))
	return None

# Remove TAG from StealthWatch
def remove_tag(tag_id):
	
	print(f"\n==> Removing TAG {tag_id}")
	url = f'https://{SMC_HOST}/smc-configuration/rest/v1/tenants/{SMC_TENANT_ID}/tags/{tag_id}'
	response = api_session.request("DELETE", url, verify=False)

	# If successfully able to get list of tags (host groups)
	if (response.status_code == 200):
		print(green(f"Tag {tag_id} has been successfully removed"))
		return True

	print(red(f"An error has ocurred, while removing the tag, with the following code {response.status_code}"))
	return False

# Send message in the Webex Space
def send_webex_message(message):
	teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)
	teams.messages.create(
		roomId=env_user.WEBEX_TEAMS_ROOM_ID,
		markdown=message
	)

# Get my Webex Teams username (for logging purposes)
def get_webex_teams_username():

	teams = webexteamssdk.WebexTeamsAPI(env_user.WEBEX_TEAMS_ACCESS_TOKEN)
	data = teams.people.me()

	if data:
		return data.displayName
	
	return f"random-user-{random.randint(0,100)}"


# If this script is the "main" script, run...
if __name__ == "__main__":

	webex_username = get_webex_teams_username()

	# Initialize the Requests session
	api_session = requests.Session()

	# Login to the SMC
	login_request_data = {
		"username": SMC_USER,
		"password": SMC_PASSWORD
	}
	login_success = login(api_session, login_request_data)

	# If the login was successful
	if login_success:

		# Get all the tenants
		tenants_content = get_tenants(api_session)

		# If managed to get the list of tenants
		if tenants_content:

			# Store the tenants (domains) IDs as a variable to use later
			tenant_list = json.loads(tenants_content)["data"]
			print(green(f'Found all the following tenants: {tenant_list}'))
			SMC_TENANT_ID = tenant_list[0]['id']

			# Print the SMC Tenant ID selected
			print(f'Working on Tenant ID is: {SMC_TENANT_ID}')
			
			# Get all hosts with abnormally high traffic
			time_window = 60
			query_search_id = get_security_events(time_window)

			# If successfully created a search query 
			if query_search_id:

				print(f"\n==> Created query looking for all the hosts that generate high amount of traffic in the last {time_window} minutes.")
				print("Generating results. Please wait...")

				# Check status of query
				url = f'https://{SMC_HOST}/sw-reporting/v1/tenants/{SMC_TENANT_ID}/security-events/queries/{query_search_id}'

				# While search status is not complete, check the status every second
				percent_complete = 0.0
				while percent_complete != 100.0:
					response = api_session.request("GET", url, verify=False)
					percent_complete = json.loads(response.content)["data"]["percentComplete"]
					print(f"Search progress: {percent_complete}%")
					time.sleep(1)
				print(green(f"Search query completed!"))

				# Get the search results
				url = f'https://{SMC_HOST}/sw-reporting/v1/tenants/{SMC_TENANT_ID}/security-events/results/{query_search_id}'
				response = api_session.request("GET", url, verify=False)
				results = json.loads(response.content)["data"]["results"]
				
				# Loop through the results and add the first 10 source IP addresses to the list
				total_security_events = len(results)
				print(f'Total found events: {total_security_events}')
				ip_addresses = set()
				for result in results:
					source_address = result['source']['ipAddress']
					ip_addresses.add(source_address)

					if len(ip_addresses) == 10:
						break
				print(f"Collected the following first 10 IP addresses: {ip_addresses}")

				tag_name = f"[{webex_username}] - High Traffic Hosts"
				request_data = [
					{
						"name": tag_name,
						"location": "OUTSIDE",
						"description": "Hosts generating or receiving an unusually high amount of traffic.",
						"ranges": list(ip_addresses)
					}
				]
				id_tag = create_new_tag(request_data)

				if id_tag:

					print(f"\n==> Sending message to Webex Space bragging for a completed mission! :D")
					message = f"**StealthWatch Enterprise Mission completed!!! :D**\nI created the new TAG _{tag_name}_, containing {len(ip_addresses)} IP addresses of hosts generating an unusually high amount of traffic."

					# Finally, post a message to the Webex Teams Room to brag!!!
					send_webex_message(message)
					print(green(f"Message sent, StealthWatch Enterprise Mission Completed!!!"))

					# Clean-up the sandbox removing the TAG
					remove_tag(id_tag)


		# Terminate API session and terminate token validity
		terminate_session(api_session)
