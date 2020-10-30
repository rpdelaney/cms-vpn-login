# https://support.1password.com/command-line/
# https://docs.python.org/3.7/library/subprocess.html

import json
import os
import subprocess
import sys

import pexpect

from . import cli


def main() -> None:
    args = cli.parse_args()

    # Every record in 1password has a UUID. This one has my password and totp
    # for the CMS VPN. Your record's UUID will be different.
    #
    # Using the UUID to do the lookup saves us parsing a few layers of nested
    # JSON.  But to find it the first time, you may have to parse a few layers
    # of nested JSON manually using 1password-cli.
    OP_RECORD_UUID = {"CMS_VPN": "rsfq7iycufda7m5acghwyodapq"}

    OP_EMAIL = "ryan@truss.works"

    # log in to onepassword
    print("Signing in to onepassword...")
    child = pexpect.spawn("op signin")
    child.expect_exact(
        f"Enter the password for {OP_EMAIL} at truss.1password.com:"
    )

    print("We are logged in!")
    # get the 1pass item
    proc_get = subprocess.run(
        ["op", "get", "item", OP_RECORD_UUID["CMS_VPN"]],
        capture_output=True,
        text=True,
    )
    try:
        item = json.loads(proc_get.stdout)
    except json.decoder.JSONDecodeError:
        print(f"Could not decode json in: {proc_get.stdout}")
        print(f"stderr: {proc_get.stderr}")
        sys.exit(1)

    try:
        fields_by_name = {
            field.get("name"): field for field in item["details"]["fields"]
        }
    except UnboundLocalError:
        print(f"Could not do the business in: {fields_by_name}")

    username = fields_by_name["username"]["value"]
    password = fields_by_name["password"]["value"]

    # try to log in
    os.chdir(f"{args.path}")
    print("Spawning child process")
    child = pexpect.spawn("bash ./run-cms")

    print("waiting for username prompt...")
    child.expect_exact("Username:")
    print("sending username")
    child.sendline(username)

    print("waiting for password prompt...")
    child.expect_exact("Password:")
    print("sending password")
    child.sendline(password)

    print("waiting for totp prompt...")
    child.expect_exact("Password:")  # this second prompt is really the totp
    print("fetching totp")
    totp_get = subprocess.run(
        ["op", "get", "totp", OP_RECORD_UUID["CMS_VPN"]],
        capture_output=True,
        text=True,
    )
    print("sending totp")
    child.sendline(totp_get.stdout)

    print("finished, switching to interactive")
    child.interact()
