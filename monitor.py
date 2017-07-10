import argparse
import xml.etree.ElementTree as etree
from email.mime.text import MIMEText
from urllib import request
import smtplib
import time

parser = argparse.ArgumentParser()
parser.add_argument('domain', type=str)
parser.add_argument('username', type=str)
parser.add_argument('token', type=str)
parser.add_argument('salt', type=str)
parser.add_argument('recipient', type=str)
args = parser.parse_args()

while True:
    random = request.urlopen('http://{0}/rest/getRandomSongs?size=1&u={1}&t={2}&s={3}&v=1.13.0&c=monitor'.format(args.domain, args.username, args.token, args.salt)).read()
    random = etree.fromstring(random)
    random = random.find('.//{http://libresonic.org/restapi}song').attrib['id']

    song = request.urlopen('http://{0}/rest/download?id={1}&u={2}&t={3}&s={4}&v=1.13.0&c=monitor'.format(args.domain, random, args.username, args.token, args.salt))

    if song.getheader('Content-Type') != 'application/x-download':
        message = MIMEText('')
        message['Subject'] = 'Subsonic is down'
        message['From'] = ''
        message['To'] = args.recipient
        s = smtplib.SMTP('smtp', 25)
        s.send_message(message)
        s.quit()

    time.sleep(3600)

