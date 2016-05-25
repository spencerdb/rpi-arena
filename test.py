#!/usr/bin/python
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

oauthfile = 'lever-arena-01-d2618fc356b1.json'
scope = ['https://spreadsheets.google.com/feeds']
json_key = json.load(open(oauthfile))
credentials = ServiceAccountCredentials.from_json_keyfile_name(oauthfile,scope)

gc = gspread.authorize(credentials)


sh = gc.open("testSheet").sheet1
sh.update_acell('A1', "test")


