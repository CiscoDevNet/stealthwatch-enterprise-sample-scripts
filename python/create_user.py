#!/usr/bin/env python

"""
This script will get all tags (host groups) in Stealthwatch using the REST API.

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
SMC_USER = "admin"
SMC_PASSWORD = "C1sco12345"
SMC_HOST = "10.10.20.60"
SMC_TENANT_ID = "132"

# Stealthwatch Constants
XSRF_HEADER_NAME = 'X-XSRF-TOKEN'

# This is the new user you want to create.
# Edit the fields as you like.
newUser = {
    'username': 'newusername',
    'fullname': 'My Full Name',
    'email'   : 'user@example.com',
    'password': 'my_password',
    'datarole': 0     # Use 0 or 1, which are the two pre-defined data roles
}

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

    try:

        # Create the request data with the mandatory data for creating a new user
        username = newUser['username']
        request_data = {
            "userName": username,
            "fullName": newUser['fullname'],
            "emailAddress": newUser['email'],
            "authenticationServiceName": "local",
            "dataRoleId": newUser['datarole'],
            "functionRoleIds": [0],
            "webFunctionRoleIds": [1],
            "password": newUser['password'],
            "isAdmin": False
        }

        # Get the list of users from the SMC
        url = 'https://' + SMC_HOST + '/smc-users/rest/v1/user'
        request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'} 
        response = api_session.request("POST", url, verify=False, data=json.dumps(request_data), headers=request_headers)

        # Check if the request was successful
        if (response.status_code != 200):
            raise RuntimeError("An error has occurred, while fetching users, with the following code: {}".format(response.status_code))

        # Loop through the list of users and print the relevant information.
        data = json.loads(response.content)["data"]
        print(f'\nNew user ({username}) successfully created.\n')

    except RuntimeError as err:
        print(err.args[0])

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)
    api_session.headers.update({XSRF_HEADER_NAME: None})

# If the login was unsuccessful
else:
    print("An error has occurred, while logging in, with the following code {}".format(response.status_code))


