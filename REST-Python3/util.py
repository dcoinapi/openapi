#!/usr/bin/env python

import urllib
import requests
import hashlib

TIMEOUT = 20
HTTP_URL = "https://openapi.dcoinpro.com" # for china user
# HTTP_URL = "https://openapi.dcoin.com"

APP_KEY = "lcj7bjmtbiai3ihrj1crcdtqz1hcfdx5"
SECRET_KEY = "sx0id8yclrnqc71rvpp3m6vj2uclt0o4"


def http_get_request(url, params):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    data = urllib.parse.urlencode(params or {})
    try:
        response = requests.get(url, data, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {"code": -1, "msg": "response status:%s" % response.status_code}
    except Exception as e:
        print("httpGet failed, detail is:%s" % e)
        return {"code": -1, "msg": e}


def http_post_request(url, params):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    data = urllib.parse.urlencode(params or {})
    try:
        response = requests.post(url, data, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return {"code": -1, "msg": "response status:%s" % response.status_code}
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"code": -1, "msg": e}


def api_key_get(url, params):
    if not params:
        params = {}
    params["api_key"] = APP_KEY
    params["sign"] = create_sign(params, SECRET_KEY)
    return http_get_request(url, params)


def api_key_post(url, params):
    if not params:
        params = {}
    params["api_key"] = APP_KEY
    params["sign"] = create_sign(params, SECRET_KEY)
    return http_post_request(url, params)


def create_sign(params, secret_key):
    sorted_params = sorted(params.items(), key=lambda d: d[0], reverse=False)
    s = "".join(map(lambda x: str(x[0]) + str(x[1] or ""), sorted_params)) + secret_key
    h = hashlib.md5(s.encode("utf-8"))
    return h.hexdigest()
