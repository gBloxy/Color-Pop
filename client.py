
import threading
import requests
from pickle import dumps, loads
from re import compile, match
from cryptography.fernet import Fernet


key = b'DfOaFLRVToUyjSRRo0ZqeVAu3Bksp_z9bp-uFpgvfsU='


def writeFile(data, file):
    data = dumps(data)
    cipher = Fernet(key)
    data = cipher.encrypt(data)
    with open(file, 'wb') as file:
        file.write(data)


def readFile(file):
    with open(file, 'rb') as file:
        data = file.read()
    cipher = Fernet(key)
    data = cipher.decrypt(data)
    data = loads(data)
    return data


class Client():
    def __init__(self, game):
        self.game = game
        
        # load config
        
        self.config = readFile('asset/config.dat')
        self.url = self.config['URL']
        self.regex = compile(self.config['REGEX'])
        
        # server connection test
        try:
            response = requests.get(self.url+'/get/'+self.game)
            
            if not response.ok or 'error' in response.json():
                self.connected = False
            else:
                self.connected = True
        
        except Exception as error:
            print(error)
            self.connected = False
        
        # load player data / check if registred
        
        data = readFile('asset/data.dat')
        self.uuid = data['uuid']
        self.username = data['username']
        if self.uuid is None or not self.isValidName(self.username):
            self.username = None
            self.registred = False
        else:
            self.registred = True
    
    def thread(self, func, args=tuple()):
        thread = threading.Thread(target=func, args=args)
        thread.start()
    
    def isValidName(self, string):
        return bool(match(self.regex, string))
    
    def save(self):
        data = {'uuid': self.uuid, 'username': self.username}
        writeFile(data, 'asset/data.dat')
    
    def register(self, username, registred=False):
        if self.connected:
            if self.isValidName(username):
                response = requests.post(
                    url  = self.config['URL_ROOT'] + '/register',
                    json = {'username': username, 'uuid': self.uuid if registred else None, 'key': self.config['ACCESS_KEY']}
                )
                data = response.json()
                if 'error' in data:
                    return data
                else:
                    if not registred:
                        self.uuid = data['uuid']
                        self.registred = True
                    self.username = username
                    self.save()
                    return {}
            else:
                return {'error': 'invalid username'}
        else:
            return {'error': 'not connected to server'}
    
    def setUsername(self, username):
        if username != self.username:
            return self.register(username, registred=True)
        return {}
    
    def getMinScore(self):
        if self.connected:
            payload = 'mode=high:'+self.username if self.registred else 'mode=high'
            response = requests.get(self.url+'/get/'+self.game+'?'+payload)
            return int(response.text)
    
    def sendScore(self, score):
        if self.connected and self.registred and type(score) == int:
            data = {'uuid': self.uuid, 'score': score, 'key': self.config['ACCESS_KEY']}
            response = requests.post(self.url+'/edit/'+self.game, json=data)
            data = response.json()
            if 'error' in data:
                return data['error']
