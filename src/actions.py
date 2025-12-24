import pyotp
import sys
import os
import json

config_file = "/etc/etap-otp"
config = {}
try:
    with open(config_file, "r") as f:
        config = json.load(f)
except:
    pass

def find_user(uid):
    with open("/etc/passwd", "r") as f:
        for line in f.read().split("\n"):
            cur = line.split(":")[2]
            if str(uid) == cur:
                return line.split(":")[0]
    return None

def save(user, secret="JBSWY3DPEHPK3PXP"):
    config[user] = secret
    with open(config_file, "w") as f:
        json.dump(config, f)

def load(user):
    if user in config:
        return config[user]
    return None

def check(user, pin):
    secret = config[user]
    totp = pyotp.TOTP(secret)
    return str(pin) == str(totp.now())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "PKEXEC_UID" in os.environ:
            user = find_user(os.environ["PKEXEC_UID"])
        else:
            user = input()
        if sys.argv[1] == "save":
            save(user, sys.argv[2])
        elif sys.argv[1] == "load":
            print(load(user))
        elif sys.argv[1] == "check":
            if check(user, sys.argv[2]):
                print("true")
                sys.exit(0)
            else:
                print("false")
                sys.exit(1)

