#!/usr/bin/env python

"""
This script will get a Host Snapshot in Stealthwatch using the SOAP API.

For more information on this API, please visit:
https://www.cisco.com/c/dam/en/us/td/docs/security/stealthwatch/api/SW_6_10_0_SMC_Web_Svs_Prog_DV_1_4.pdf

 -

Script Dependencies:
    requests
    xmltodict
Depencency Installation:
    $ pip install requests
    $ pip install xmltodict

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
import xmltodict
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


# Enter all authentication info
SMC_USER = ""
SMC_PASSWORD = ""
SMC_HOST = ""
SMC_DOMAIN_ID = ""
HOST_SNAPSHOT_IP = ""

# Set the URL to the 'hosts' endpoint for HostSnapshots
url = 'https://' + SMC_HOST + '/smc/swsService/hosts'

# Set the SOAP API request data
request_data = '<?xml version="1.0" encoding="UTF-8"?>'
request_data += '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body>'
request_data += '<getHostSnapshot>'
request_data += '<host-filter domain-id="' + SMC_DOMAIN_ID + '">'
request_data += '<host-selection><ip-address-selection value="' + HOST_SNAPSHOT_IP + '"/></host-selection>'
request_data += '</host-filter>'
request_data += '</getHostSnapshot>'
request_data += '</soapenv:Body>'
request_data += '</soapenv:Envelope>'

print(request_data)
# Use the Requests module to POST the request and return the results
# (Note: authentication is handled here and not beforehand like with the REST API)
response = requests.request("POST", url, auth=(SMC_USER, SMC_PASSWORD), verify=False, data=request_data)

# If the login was successful
if (response.status_code == 200):

    # Converts the XML into a dictionary object
    response_dict = xmltodict.parse(response.content, xml_attribs=True)
    # Prints the results
    print(json.dumps(response_dict, indent=4))

# If the login was unsuccessful
else:
    print("An error has ocurred with the following code {}".format(response.status_code))

