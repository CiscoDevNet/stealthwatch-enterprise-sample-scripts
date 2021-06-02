#!/usr/bin/env python

"""
This script will get all Cognitive Intelligence incidents in Stealthwatch using the REST API.

For more information on this API, please visit:
https://developer.cisco.com/docs/stealthwatch/

 -

Script Dependencies:
    requests
Depencency Installation:
    $ pip install requests

System Requirements:
    Stealthwatch Version: 7.1.0 or higher

Cognitive Intelligence Incidents API Configuration
    The Cognitive Intelligence Incidents REST API is disabled by default. To enable the API:
        * Enable Cognitive Analytics in External Services on your SMC and Flow Collector(s).
        * Locate /lancope/tomcat/webapps/cta-events-collector/WEB-INF/classes/app.properties file on your SMC system
        * Under #CTA_ENABLED section set the cta.api.enabled option to true
        * Restart web server on your SMC system: systemctl restart lc-tomcat
    (Note: The API returns CTA incidents for all domains and expects tenantId to be 0 in the API path parameter.
    Requesting data for any specific tenant will result in error.)


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

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Enter all authentication info
SMC_USER = ""
SMC_PASSWORD = ""
SMC_HOST = ""
MALICIOUS_IP = ""

# Stealthwatch Constants
XSRF_HEADER_NAME = 'X-XSRF-TOKEN'

# Set the URL for SMC login
url = "https://" + SMC_HOST + "/token/v2/authenticate"

# Let's create the login request data
login_request_data = {
    "username": SMC_USER,
    "password": SMC_PASSWORD
}

# Initialize the Requests session
api_session = requests.Session()

# Perform the POST request to login
response = api_session.request("POST", url, verify=False, data=login_request_data)

# If the login was successful
if (response.status_code == 200):

    # Set XSRF token for future requests
    for cookie in response.cookies:
        if cookie.name == 'XSRF-TOKEN':
            api_session.headers.update({XSRF_HEADER_NAME: cookie.value})
            break

    # Get the list of Cognitive Intelligence incidents from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v2/tenants/0/incidents?ipAddress=' + MALICIOUS_IP
    response = api_session.request("GET", url, verify=False)

    # If successfully able to get list of Cognitive Intelligence incidents
    if (response.status_code == 200):

        # Loop through the list and print Cognitive Intelligence incident
        incidents = json.loads(response.content)["data"]
        for incident in incidents:
            print(incident)

    # If unable to fetch list of Cognitive Intelligence incidents
    else:
        print(
            "An error has ocurred, while fetching Cognitive Intelligence incidents, with the following code {}".format(
                response.status_code))

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)
    api_session.headers.update({XSRF_HEADER_NAME: None})

# If the login was unsuccessful
else:
    print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))
