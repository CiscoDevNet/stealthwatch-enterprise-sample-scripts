#!/usr/bin/env python

"""
This script will get the details for a specific tag (host group) in Stealthwatch using the REST API.

For more information on this API, please visit:
https://developer.cisco.com/docs/stealthwatch/

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
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


# Enter all authentication info
SMC_USER = ""
SMC_PASSWORD = ""
SMC_HOST = ""
SMC_TENANT_ID = ""
SMC_MALICIOUS_TAG_ID = ""
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
if(response.status_code == 200):

    # Set XSRF token for future requests
    for cookie in response.cookies:
        if cookie.name == 'XSRF-TOKEN':
            api_session.headers.update({XSRF_HEADER_NAME: cookie.value})
            break

    # Get the details of a given tag (host group) from the SMC
    url = 'https://' + SMC_HOST + '/smc-configuration/rest/v1/tenants/' + SMC_TENANT_ID + '/tags/' + SMC_MALICIOUS_TAG_ID
    response = api_session.request("GET", url, verify=False)

    # If successfully able to get list of tags (host groups)
    if (response.status_code == 200):

        # Grab the tag details and check if the malicious IP is associated with this tag
        tag_details = json.loads(response.content)["data"]
        if MALICIOUS_IP in tag_details["ranges"]:
            print("This IP is already associated with this tag (host group)")
        else:
            print("This IP is not associated with this tag (host group)")



    # If unable to fetch details of a given tag (host group)
    else:
        print("An error has ocurred, while fetching tags (host groups), with the following code {}".format(response.status_code))

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)
    api_session.headers.update({XSRF_HEADER_NAME: None})

# If the login was unsuccessful
else:
        print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))


