# Stealthwatch Sample Scripts
This repository contains sample Python scripts and Postman collections related to Cisco Stealthwatch Enterprise. It is available for use by the Cisco DevNet community through Code Exchange.
<br/><br/>
This project is split into 2 sections: 
* [Python samples](./python-samples)
* [Postman samples](./postman-samples)

## Python samples
#### Installation
1. Ensure Python 3 is installed.
   * To download and install Python 3, please visit https://www.python.org.
2. Ensure the Python `requests` module is installed.
   * For more information on the Python `requests` module, please visit https://pypi.org/project/requests/.
3. Download the `.py` files located in the [python-samples](./python-samples) directory.

*Alternatively, advanced users can also use git to checkout / clone a copy of this project.*

#### Configuration
Open the desired `.py` file that you intend to run and enter the following values where specified:
* `SMC_USER = ""`
* `SMC_PASSWORD = ""`
* `SMC_HOST = ""`

(Note: additional fields may also be required)

#### Usage
<!--
Show users how to use the code. Be specific. Use appropriate formatting when showing code snippets or command line output. If a particular [DevNet Sandbox](https://developer.cisco.com/sandbox/) or [Learning Lab](https://developer.cisco.com/learning-labs/) can be used in to provide a network or other resources to be used with this code, call that out here.
-->
1. Identify the path to your Python 3 executible. 
    * Depending how Python 3 was installed, this might be as simple as just calling the command `python` or `python3`.
2. Run the Python script with the following command:
    * `$ <PYTHON-PATH> <PYTHON-SCRIPT-PATH>`
    * Example: `$ /usr/bin/python ./get_flows.py`

## Postman samples
#### Installation
1. Ensure Postman is installed.
   * To download and install Postman, please visit https://www.getpostman.com.
2. Download the Postman collections and environment files located in the [postman-samples](./postman-samples) directory.
3. After launching Postman, click the `import` button and import the previously downloaded Postman files.

#### Configuration
1. Ensure the Postman collections and environment have been imported.
2. Select the `Stealthwatch Enterprise - DevNet` environment from the dropdown in the top-right corner of Postman.
3. To the right of this dropdown (in the top-right corner of Postman), click the graphic of the gear to edit the Postman environment.
4. Please set the following fields appropriately:
    * `STEALTHWATCH-SMC`
    * `username`
    * `password`

#### Usage
<!--
Show users how to use the code. Be specific. Use appropriate formatting when showing code snippets or command line output. If a particular [DevNet Sandbox](https://developer.cisco.com/sandbox/) or [Learning Lab](https://developer.cisco.com/learning-labs/) can be used in to provide a network or other resources to be used with this code, call that out here.
-->
1. From the Collections list on the left side of Postman, select the desired collection as well as the desired request to run.
2. If necessary, modify any parameters in either the `params` section or the `body` section of the request.
3. When ready, press the `send` button to run the Postman request, and view the response below. 

*For more information on how to use Postman, please visit https://learning.getpostman.com.*

## Known issues
No known issues.

<!--
## Getting help
TODO: Instruct users how to get help with this code; this might include links to an issue tracker, wiki, mailing list, etc.
-->

## Getting involved
Contributions to this code are welcome and appreciated. See [CONTRIBUTING](./CONTRIBUTING.md) for details. Please adhere to our [Code of Conduct](./CODE_OF_CONDUCT.md) at all times.

## Licensing info
This code is licensed under the BSD 3-Clause License. See [LICENSE](./LICENSE) for details. 

