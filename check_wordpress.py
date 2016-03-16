#!/usr/bin/env python
# Nagios plugin to check the heartbeat and version of a wordpress site
# Author: Christoph Hack <chack@mgit.at>
# (c) 2016 mgIT GmbH
import argparse
from requests import get
from datetime import datetime, timedelta
from sys import exit
import re
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

parser = argparse.ArgumentParser(description='Check the wordpress heartbeat.')
parser.add_argument('url', help='base URL of the wordpress blog')
parser.add_argument('--limit', default=5*60, type=int, help='accepted timedelta in seconds (default: 5m)')
parser.add_argument('--version', default=False, action='store_true', help='perform a version check instead')

args = parser.parse_args()

url = args.url
limit = timedelta(seconds=args.limit)
check_version = args.version

NAGIOS_OK = 0
NAGIOS_WARNING = 1
NAGIOS_CRITICAL = 2
NAGIOS_UNKNOWN = 3

WORDPRESS_API = 'http://api.wordpress.org/core/version-check/1.5/?version='

if check_version:
    try:
        re_version = re.compile(r'<meta\s+name="?generator"?\scontent="WordPress ([\d.]+)"\s*/>')
        r = get(url)
        m = re_version.search(r.text)
        if m is None:
            print('UNKNOWN - unable to detect WordPress version')
            exit(NAGIOS_UNKNOWN)
        version = m.group(1)
        r = get(WORDPRESS_API + version)
        status = r.text.split()[0]
        if status == 'upgrade':
            print('CRITICAL - upgrade required (current: %s)' % version)
            exit(NAGIOS_CRITICAL)
        if status == 'latest':
            print('OK - version %s is up to date' % version)
            exit(NAGIOS_OK)
        print('UNKNOWN - unknown status %s' % status)
        exit(NAGIOS_UNKNOWN)
    except Exception as e:
        print('UNKNOWN - %s' % e)
        exit(NAGIOS_UNKNOWN)

try:
    r = get(urljoin(url, '/wp-admin/admin-ajax.php?action=heartbeat'))
    if r.status_code != 200:
        print('CRITICAL - unexpected status code %d', r.status_code)
        exit(NAGIOS_CRITICAL)
    data = r.json()
    current = datetime.fromtimestamp(data['server_time'])
    now = datetime.now()
    delta = now - current if now > current else current - now
    if delta > limit:
        print('CRITICAL - timedelta %s too large' % delta)
        exit(NAGIOS_CRITICAL)
    print('OK - server time is %s' % current)
    exit(NAGIOS_OK)
except Exception as e:
    print('UNKNOWN - %s' % e)
    exit(NAGIOS_UNKNOWN)
