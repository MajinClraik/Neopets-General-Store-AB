import sys
import re
import random
import os
import time
from random import randint
from classes.neo import neo

class client:
    def __init__(self):
        self.neo = neo()
        self.username = None

    def doLogin(self, username, password, proxy):
        self.username = username
        if proxy != 'ip:port':
            self.neo.proxy(proxy)
        self.neo.get('login/')
        resp = self.neo.post('login.phtml', {'destination': '', 'username': username, 'password': password}, 'http://www.neopets.com/login/')
        if resp.text.find('id=\'npanchor\'') > 1:
            self.neo.log('Logged in as %s' % username)
            return True
        else:
            return False

    def generalStore(self):
        amount = int(input('How many times do you want to buy Blue Short Hair Brush?\n'))
        for _ in range(amount):
            resp = self.neo.get('generalstore.phtml')
            storeHash = self.neo.getBetween(resp.text, 'name=\'_ref_ck\' value="', '">')
            x, y = random.randint(0, 80), random.randint(0, 80)
            resp = self.neo.post('generalstore.phtml', {'buy_oii': '181', 'store_type': '', '_ref_ck': storeHash, 'buy_oii_click.x': x, 'buy_oii_click.y': y}, resp.url)
            if resp.text.find('purchased Blue Short Hair Brush') > 1:
                self.neo.log('Purchased x1 Blue Short Hair Brush')
            elif resp.text.find('purchased Blue Short Hair Brush') < 0:
                self.neo.log('Unable to buy Blue Short Hair Brush..')
            else:
                self.neo.log('Something went wrong..')
        self.neo.log('Finished buying from the general store, press enter to exit')
        input()

    def bot(self):
        accountData = self.loadAccounts()
        isLogged = self.doLogin(accountData[0], accountData[1], accountData[2])
        if isLogged:
            self.generalStore()
        else:
            self.neo.log('Unable to login')

    def loadAccounts(self):
        with open('accounts.txt', 'r') as f:
            accountData = f.readline().split(';')
            username, password, proxy = accountData[0].strip(), accountData[1].strip(), accountData[2].strip()
            return username, password, proxy

if __name__ == "__main__":
    a = client()
    a.bot()