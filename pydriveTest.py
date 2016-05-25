#!/usr/bin/python
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

#load authorization file and drive API
oauthfile = 'lever-arena-01-d2618fc356b1.json'
scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(oauthfile,scope)

#connect to drive with the credentials
gauth = GoogleAuth()
gauth.credentials = credentials
gauth.Authorize()
drive = GoogleDrive(gauth)

#TEST
#Create a file in folder lever-arena-01
testFile = drive.CreateFile({'parents' : [{'id' : '0B8LTj-6zmvAPQTZZS2tSaXR4UTA'}],'title': 'test.txt'})
testFile.SetContentString('Test')
testFile.Upload()

# Paginate file lists by specifying number of max results
for file_list in drive.ListFile({'q': "'0B8LTj-6zmvAPQTZZS2tSaXR4UTA' in parents and trashed=false"}):
    print 'Received %s files from Files.list()' % len(file_list) # <= 10
    for file1 in file_list:
        print 'title: %s, id: %s' % (file1['title'], file1['id'])
