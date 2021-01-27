#!/usr/bin/env python

import json

import requests
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
def get_all_security_events():
	# Set the URL 
	url = f'https://{SMC_HOST}/smc-configuration/rest/v1/tenants/{SMC_TENANT_ID}/policy/system/events'

	# Perform the query to initiate the search
	response = api_session.request("GET", url, verify=False)

	if response.status_code == 200:
		return json.loads(response.content)["data"]

	print(red(f"An error has ocurred, while getting all security events, with the following code {response.status_code}"))
	print(red(f"{response.json()}"))
	return None

# Update security event parameters
def update_security_event(security_event_data):
	# Set the URL 
	url = f'https://{SMC_HOST}/smc-configuration/rest/v1/tenants/{SMC_TENANT_ID}/policy/system/events'

	# Perform the query to initiate the search
	request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
	response = api_session.request("PUT", url, verify=False, data=json.dumps(security_event_data), headers=request_headers)

	if response.status_code == 200:
		print(green(f'Security Events updated successfully!'))
		return json.loads(response.content)["data"]

	print(red(f"An error has ocurred, while updating the security events data, with the following code {response.status_code}"))
	print(red(f"{response.json()}"))
	return None

# Terminate API session and terminate token validity
def terminate_session(sw_session):
	
	uri = f'https://{SMC_HOST}/token'
	response = api_session.delete(uri, timeout=30, verify=False)


# If this script is the "main" script, run...
if __name__ == "__main__":

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
			# TODO: Print all the tenants IDs returned and find the one you need.
			print(green(f'Found the following tenants: {tenant_list}'))
			SMC_TENANT_ID = tenant_list[0]['id']

			# Print the SMC Tenant ID selected
			print(f'Working on Tenant ID is: {SMC_TENANT_ID}')
			
			# Updating the Security Event 16 (Total High Traffic) to meet our needs for the DNE
			print(f'\n==> Updating the Security Event 16 (Total High Traffic) to meet our needs for the DNE')
			new_security_event_details = [{
				"id": 16,
				"policyId": 1,
				"eventSettings": {
					"eventStatus": {
						"sourceStatus": "ENABLED",
						"targetStatus": "ENABLED"
					},
					"alarmSettings": [
						{
							"key": "tolerance",
							"value": "70"
						},
						{
							"key": "min",
							"value": "100000"	# Do not trigger alarms for less than 100KB of total traffic
						},
						{
							"key": "max",
							"value": "500000"	# Always trigger alarms for more than 500KB of total traffic
						}
					]
				}
			}]

			updated = update_security_event(new_security_event_details)

		# Terminate API session and terminate token validity
		terminate_session(api_session)
