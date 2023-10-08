import requests

class AccessToken:
    def __init__(self, redirect_uri, client_id, client_secret, token_url) -> None:
        self.__redirect_uri = redirect_uri
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__token_url = token_url
    
    def get_token(self, code):
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
    
        data = {
            "grant_type":"authorization_code", # TYPE
            "code": code, # AUTHORIZATION CODE
            "redirect_uri": self.__redirect_uri, # APP REDIRECT URI
            'client_id': self.__client_id, # SET SPOTIFY CLIENT ID HERE
            'client_secret': self.__client_secret # SET SPOTIFY CLIENT SECRET HERE
        }

        # return response with access_token
        return requests.post(url=self.__token_url, data=data, headers=headers)