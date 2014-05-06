#!/usr/bin/python
##
# Simple example to list all known arrays
# in the web services API.  Should just work.
#
# by Blake Golliher blakegolliher@gmail.com
##

import json, sys, urllib2, base64, getpass

usage = """
Usage: ./eseries_get_all.py webservices.host
e.g ./eseries_io_wwn_name_map.py webserver001

eseries-array-1 : 52418bfb-520e-82d9-a5b7-49f363825dc4
eseries-array-2 : 52481bfb-530e-42d0-a7b5-46g363825dc9
eseries-array-3 : 53447bab-920e-02d7-u0b5-76f363825dc4

"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

webserviceshost = sys.argv[1]

name = 'ro' # change this to match your env.
passwd = getpass.getpass()

request = urllib2.Request("https://" + webserviceshost + ":8443/devmgr/v1/storage-systems/")
request.add_header('Accept', 'application/json')
base64string = base64.encodestring('%s:%s' % (name,passwd)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)

data = json.load(result)

for info in data:
    print "%s : %s " % (info['name'], info['id'])
