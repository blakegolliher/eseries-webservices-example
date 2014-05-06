#!/usr/bin/python

import json, sys, urllib, urllib2, base64

usage = """
Usage: ./eseries_io.py arrayname
e.g ./eseries_io.py eseries-001
 
"""

## change to your details
webserviceshost = 'webservices.host' 
name = 'yourname'
passwd = 'yourpass'

arrayname = sys.argv[1]

def sizeof_fmt(num):
    for x in ['Bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def nametouid(arrayname):
	request = urllib2.Request("https://" + webserviceshost + ":8443/devmgr/v1/storage-systems/")
	request.add_header('Accept', 'application/json')
	base64string = base64.encodestring('%s:%s' % (name,passwd)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)

	data = json.load(result)
	for array in data:
  		if array['name'] == arrayname:
			uid  = array['id']
			return uid

arrayid = nametouid(arrayname)

request = urllib2.Request("https://" + webserviceshost + ":8443/devmgr/v1/storage-systems/" + arrayid + "/volume-statistics/")

request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % (name,passwd)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data = json.load(result)

print 'Array Name : %s' % arrayname
print 'Array ID   : %s' % arrayid

for info in data:
	volid	   = info['volumeId']
	readbytes  = float(info['readBytes'])
	readops    = info['readOps']
	writebytes = float(info['writeBytes'])
	writeops   = info['writeOps']
	print "  %s : read bytes = %s read ops = %s write bytes = %s write ops = %s " % (volid, sizeof_fmt(readbytes), readops, sizeof_fmt(writebytes), writeops)
