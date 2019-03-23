#!/usr/bin/env python

"""
This script will get the flows for a specific IP in Stealthwatch using the REST API.

For more information on this API, please visit:
https://www.cisco.com/web/fw/stealthwatch/Online-Help/Content/Online-Help/enterprise-rest-api.htm

 -

Script Dependencies:
    requests
Depencency Installation:
    $ pip install requests

System Requirements:
    Stealthwatch Version: 7.0.0 or higher

Copyright (c) 2019, Cisco Systems, Inc. All rights reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
import json
import datetime, time
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


# Enter all authentication info
SMC_USER = "admin"
SMC_PASSWORD = "lan7cope"
SMC_HOST = "10.208.102.170"
SMC_TENANT_ID = "122"
MALICIOUS_IP = "10.10.101.24"

# Set the URL for SMC login
url = "https://" + SMC_HOST + "/token/v2/authenticate"

# Let's create the loginrequest data
login_request_data = {
    "username": SMC_USER,
    "password": SMC_PASSWORD
}

# Initialize the Requests session
api_session = requests.Session()

# Perform the POST request to login
response = api_session.request("POST", url, verify=False, data=login_request_data)

# If the login was successful
if(response.status_code == 200):

    # Set the URL for the query to POST the filter and initiate the search
    url = 'https://' + SMC_HOST + '/sw-reporting/v2/tenants/' + SMC_TENANT_ID + '/flows/queries'

    # Set the timestamps for the filters, in the correct format, for last 60 minutes
    end_datetime = datetime.datetime.utcnow()
    start_datetime = end_datetime - datetime.timedelta(minutes=60)
    end_timestamp = end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    start_timestamp = start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Set the filter with the request data
    request_data = {
        "startDateTime": start_timestamp,
        "endDateTime": end_timestamp,
        "recordLimit": 50
    }
    print(request_data)

    # Perform the query to initiate the search
    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("POST", url, verify=False, data=json.dumps(request_data), headers=request_headers)

    # If successfully able to initiate flows search, grab the search details
    if (response.status_code == 201):
        print("Generating results. Please wait...\n")
        search = json.loads(response.content)["data"]["query"]

        # Set the URL to check the search status
        url = 'https://' + SMC_HOST + '/sw-reporting/v2/tenants/' + SMC_TENANT_ID + '/flows/queries/' + search["id"]

        # While search status is not complete, check the status every second
        while search["percentComplete"] != 100.0:
            response = api_session.request("GET", url, verify=False)
            search = json.loads(response.content)["data"]["query"]
            time.sleep(1)

        # Set the URL to check the search results and get them
        url = 'https://' + SMC_HOST + '/sw-reporting/v2/tenants/' + SMC_TENANT_ID + '/flows/queries/' + search["id"] + "/results"
        response = api_session.request("GET", url, verify=False)
        results = json.loads(response.content)["data"]["flows"]

        # Loop through the results and print each flow in a new line
        for flow in results:
            print(flow)

    # If unable to update the IPs for a given tag (host group)
    else:
        print("An error has ocurred, while getting flows, with the following code {}".format(response.status_code))

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)

# If the login was unsuccessful
else:
        print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))


