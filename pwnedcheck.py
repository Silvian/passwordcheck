import sys
import hashlib
import requests


def hashpasswd(password):
    h = hashlib.sha1()
    password = password.encode('utf-8')
    h.update(password)
    return h.hexdigest().upper()


def pwncheck(password):
    sha1_hash = hashpasswd(password)
    # first 5 characters is to be used as the key
    key = sha1_hash[:5]
    # remaining characters to be used as the lookup hash
    hash = sha1_hash[5:]

    url = "https://api.pwnedpasswords.com/range/{}".format(key)
    response = requests.get(url)
    results = list(response.text.split("\r\n"))

    compromised = False
    for result in results:
        parts = list(result.split(":"))
        match = parts[0] # the remaining hash to be matched
        count = parts[1] # the occurance of this match
        if hash == match:
            compromised = True
            print("Your password has been compromised!")
            print("It has been found {} times.".format(count))
            print("Do not use this password anymore")
    if not compromised:
        print("Your password has not been found yet.")


def main():
    try:
        args = sys.argv[1]
        pwncheck(args)
    except IndexError as e:
        print("Please provide a password to check")


if __name__ == '__main__':
    main()
