import requests


class AccessToken:
    """To be able get a permission to access private data"""
    def __init__(self, redirect_uri: str, client_id: str, client_secret: str, token_url: str) -> None:
        """
        :param redirect_uri (str): to redirect to after the user grants or denies permission
        :param client_id (str): Spotify client id
        :param client_secret (str): Spotify client secret
        :param token_url (str): Spotify base url access token
        """
        self.__redirect_uri = redirect_uri
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__token_url = token_url

    def get_token(self, code: str) -> object:
        """Get access token
        
        :param code (int): authorization code from flask application
        :return response (json): json response
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.__redirect_uri,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }

        return requests.post(url=self.__token_url, data=data, headers=headers)
