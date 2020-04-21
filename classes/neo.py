import requests
import os
import time
import random
import json

class neo:
    def __init__(self):
        self.s = requests.session()
        self.base = 'http://www.neopets.com/'
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        self.minDelay = 0.0
        self.maxDelay = 0.0
        self.getSettings()
        self.setHeaders()

    def log(self, msg):
        print(time.strftime('%A') + ' ' + '%s%s' % (time.strftime('%H:%M:%S => '), msg.encode('utf-8').decode('utf-8')))

    def proxy(self, prox):
        self.s.proxies.update({'http': 'http://%s' % prox, 'https': 'https://%s' % prox})

    def getBetween(self, data, first, last):
        return data.split(first)[1].split(last)[0]

    def url(self, path):
        return '%s%s' % (self.base, path)

    def setHeaders(self):
        self.s.headers.update({'User-Agent': self.useragent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'})

    def get(self, path, referer = None, params = None):
        try:
            time.sleep(random.uniform(self.minDelay, self.maxDelay))
            url = self.url(path)
            if referer:
                self.s.headers.update({'Referer': referer})
            if params:
                r = self.s.get(url, params=params)
            else:
                r = self.s.get(url)
            if 'Referer' in self.s.headers:
                del self.s.headers['Referer']
            return r
        except:
            self.get(path, referer)

    def post(self, path, data = None, referer = None):
        try:
            time.sleep(random.uniform(self.minDelay, self.maxDelay))
            if referer:
                self.s.headers.update({'Referer': referer})
            url = self.url(path)
            if data:
                r = self.s.post(url, data=data)
            else:
                r = self.s.post(url)
            if 'Referer' in self.s.headers:
                del self.s.headers['Referer']
            return r
        except:
            self.post(path, data, referer)

    def getSettings(self):
        with open('settings/settings.ini', 'r') as f:
            settings = f.read().strip()
        bot = self.getBetween(settings, '[bot settings]', '[/bot settings]')
        bot = bot.split('\n')[1:-1]
        self.useragent = bot[0].split(':', 1)[1]
        self.minDelay = float(bot[1].split(':', 1)[1])
        self.maxDelay = float(bot[2].split(':', 1)[1])