
from requests import get
from json import load
from re import compile, match
from cryptography.fernet import Fernet


class Client():
    def __init__(self, name):
        self.name = name
        
        with open('asset/config.json') as file:
            self.config = load(file)
            self.url = self.config['URL']
        
        try:
            responce = get(self.url+'/get/'+self.name)
            data = responce.json()
            if 'error' in data:
                self.connected = False
            else:
                self.connected = True
            
        except Exception as error:
            print(error)
            self.connected = False
        
        self.regex = compile(self.config['REGEX'])
        self.username = None
        self.password = None
    
    @property
    def logged(self):
        return self.username is not None and self.password is not None
    
    def isValidName(self, string):
        return bool(match(self.regex, string))
    
    def login(self, username, password):
        if self.isValidName(username):
            if self.isValidName(password):
                self.username = username
                self.password = password
            else:
                return {'error': 'invalid password'}
        else:
            return {'error': 'invalid username'}
    
    def logout(self):
        self.username = None
        self.password = None
    
    def sendScore(self, score):
        if self.connected and self.unsername and self.password:
            responce = get(
                self.url+'/edit/'+self.name+'?player='+self.username+'&score='+str(score)+'&password='+self.password+
                '&key='+Fernet(b'b8eo6lOvOFWpk8JjYlGEK_dw2MULYsXhdsHrF3C5sY4=').decrypt(self.config['ACCESS_KEY']).decode()
                )
            data = responce.json()
            if 'error' in data:
                return data['error']
    
    def request(self, param=''):
        if self.connected:
            responce = get(self.url+'/get/'+self.name+'?'+param)
            return responce.json()
