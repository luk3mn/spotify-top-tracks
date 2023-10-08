import json
import requests

class Playlist:
    """Playlist allow to create news playlist on spotify account"""
    def __init__(self, headers: object, user_id: str) -> None:
        """
        :param user_id (str): Spotify username
        :param headers (object): Spotify header API request
        """
        self.headers = headers
        self.user_id = user_id
        self.endpoint = 'https://api.spotify.com/v1/'
    
    def create_playlist(self, name: str, description: str, public: bool = False):
        """Create a new Spotify playlist

        :param name (str): Spotify playlist name
        :param description (str): Spotify playlist description
        :param public (object): Spotify playlist visibility
        :return response (object): json file with playlist proprieties 
        """
        endpoint_url = f'{self.endpoint}users/{self.user_id}/playlists'

        request_body = json.dumps({
            'name': name,
            'description': description,
            'public': public
        })

        response = requests.post(url=endpoint_url, data=request_body, headers=self.headers)
        return response.json()
    
    def populate_playlist(self, uris: list, playlist_id: str) -> None:
        """Populate a Spotify playlist with tracks
        
        :param playlist_id (str): playlist id of playlist to populate
        :param uri (str): uri list Spotify tracks
        """
        endpoint_url = f'{self.endpoint}playlists/{playlist_id}/tracks'

        request_body = json.dumps({
            "uris": uris
        })

        response = requests.post(url=endpoint_url, data=request_body, headers=self.headers)
        print(response.status_code)
