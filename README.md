# Cisco Secure Network Analytics API Sample Scripts
This repository contains sample Python scripts related to Cisco Secure Network Analytics (formerly Stealthwatch Enterprise) APIs. It is available for use by the Cisco DevNet community through Code Exchange.
For more information on the Secure Network Analytics REST API, please see the following link: https://developer.cisco.com/docs/stealthwatch/enterprise

## Compatibility
The minimum supported version of Secure Network Analytics (formerly Stealthwatch) that is required to use each respective API capability:
   * v6.5.0 (Host Snapshot)
   * v6.10.0 (Domains / Tenants, Top Reports, Security Events)
   * v7.0.0 (Flows, Host Groups / Tags)
   * v7.1.0 (Cognitive Intelligence Incidents)

## Installation
1. Ensure Python 3 is installed.
   * To download and install Python 3, please visit https://www.python.org.
2. Ensure the Python `requests` module is installed.
   * For more information on the Python `requests` module, please visit https://pypi.org/project/requests/.
3. Download the `.py` files located in the [python](python) directory.

*Alternatively, advanced users can also use git to checkout / clone this project.*

## Configuration
Open the desired `.py` file that you intend to run and enter the following values where specified:
* `SMC_USER = ""`
* `SMC_PASSWORD = ""`
* `SMC_HOST = ""`

*(Note: if a new user is created for making API calls that userid MUST go through the password reset process before making any api calls)

*(Note: additional fields may also be required)*

#### **Cognitive Intelligence Incidents API Configuration**
The Cognitive Intelligence Incidents REST API is disabled by default. To enable the API:

* Enable Cognitive Analytics in External Services on your Manager (formerly Stealthwatch Management Console or SMC) and Flow Collector(s).
* Locate `/lancope/tomcat/webapps/cta-events-collector/WEB-INF/classes/app.properties` file on your Manager
* Under `#CTA_ENABLED` section set the `cta.api.enabled` option to `true`
* Restart web server on your SMC system: `systemctl restart lc-tomcat`

*(Note: The API returns CTA incidents for all domains and expects tenantId to be 0 in the API path parameter. Requesting data for any specific tenant will result in error.)*

## Usage
<!--
Show users how to use the code. Be specific. Use appropriate formatting when showing code snippets or command line output. If a particular [DevNet Sandbox](https://developer.cisco.com/sandbox/) or [Learning Lab](https://developer.cisco.com/learning-labs/) can be used in to provide a network or other resources to be used with this code, call that out here.
-->
1. Identify the path to your Python 3 executible. 
    * Depending how Python 3 was installed, this might be as simple as just calling the command `python` or `python3`.
2. Run the Python script with the following command:
    * `$ <PYTHON-PATH> <PYTHON-SCRIPT-PATH>`
    * Example: `$ /usr/bin/python ./get_flows.py`

## Known issues
No known issues.

## Getting help
Use this project at your own risk (support not provided). *If you need technical support with Cisco Secure Network Analytics APIs, do one of the following:*

#### Browse the Forum
Check out our [forum](https://community.cisco.com/t5/custom/page/page-id/customFilteredByMultiLabel?board=j-disc-dev-security&labels=stealthwatch) to pose a question or to see if any questions have already been answered by our community. We monitor these forums on a best effort basis and will periodically post answers. 


## Getting involved
Contributions to this code are welcome and appreciated. See [CONTRIBUTING](CONTRIBUTING.md) for details. Please adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) at all times.

## Licensing info
This code is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE) for details. 

