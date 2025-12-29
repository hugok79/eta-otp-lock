#!/usr/bin/env python3
import os
import pwd
import grp
import traceback
import pyotp
import json

"""
{
    "etapadmin" : "JBSWY3DPEHPK3PXP"
}
"""

## Pam config (common-auth)
## before pam_unix:
# auth sufficient pam_python.so /usr/libexec/pam_otp.py


def pam_sm_authenticate(pamh, flags, argv):
    # fetch username
    try:
        user = pamh.get_user(None)
    except Exception as e:
        return pamh.PAM_AUTH_ERR

    # fetch otp
    conv = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Password: "))
    passwd = conv.resp

    # read config
    config = {}
    if not os.path.isfile("/etc/etap-otp"):
        return pamh.PAM_AUTH_ERR
    with open("/etc/etap-otp", "r") as f:
        config = json.load(f)

    # check otp
    if user in config:
        otp = pyotp.TOTP(config[user])
        if otp.now() == passwd:
            return pamh.PAM_SUCCESS

    # set auth token if not totp
    pamh.authtok = passwd
    return pamh.PAM_AUTH_ERR

def pam_sm_setcred(pamh, flags, argv):
    return pamh.PAM_SUCCESS
