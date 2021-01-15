"""Set the Environment Information Needed to Access Your Lab!

The provided sample code in this repository will reference this file to get the
information needed to connect to your lab backend.  You provide this info here
once and the scripts in this repository will access it as needed by the lab.


Copyright (c) 2018-2019 Cisco and/or its affiliates.

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

from crayons import blue, green, red
from inspect import currentframe

# User Input

# Please select the lab environment that you will be using today
#     sandbox - Cisco DevNet Always-On / Reserved Sandboxes
#     express - Cisco DevNet Express Lab Backend
#     custom  - Your Own "Custom" Lab Backend
ENVIRONMENT_IN_USE = "custom"

# End User Input


if ENVIRONMENT_IN_USE == "sandbox":
	# Values for the Reservable SMC Sandbox
	SMC = {
		"username": "admin",
		"password": "C1sco12345",
		"host": "10.10.20.60"
	}

elif ENVIRONMENT_IN_USE == "express":
	# SMC in the DevNet Express Security dCloud Pod
	SMC = {
		"username": "admin",
		"password": "C1sco12345",
		"host": "10.10.20.60"
	}


elif ENVIRONMENT_IN_USE == "custom":
	# Your SMC
	SMC = {
		"username": "admin",
		"password": "C1sco12345",
		"host": "10.10.20.60"
	}

		
"""Helper functions for the missions"""


def print_missing_mission_warn(lineerror) :
	print(blue(f"\nPlease replace this fucntion (print_missing_mission_warn(...)) with correct required mission statements!\n"))
	print(green(f"At hosted DNE Event; Please ask for help from procter or your neighbour attendee; if you are not making progress...\n"))
	print(red(f"Check and complete the #TODO at Line number --->  {lineerror}"))
	return exit()

def get_line():
	currentfram=currentframe()
	return currentfram.f_back.f_lineno