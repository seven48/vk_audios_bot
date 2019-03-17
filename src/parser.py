import sys
import urllib

from bs4 import BeautifulSoup
from requests import Session, exceptions

from src.utils import logger


class Parser:
    def __init__(self, username, password):
        self.session = Session()

        self.username = username
        self.password = password

        self._auth()

    def search(self, query):
        url = {
            'q': query,
            'tab': 'global'
        }
        link = 'https://m.vk.com/audio?{}'.format(urllib.parse.urlencode(url))

        try:
            response = self.session.get(link)
        except exceptions.SSLError:
            response = self.session.get(link, verify=False)

        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            'query': query,
            'type': 'Search',
            'artists': {},
            'playlists': {},
            'tracks': {}
        }

        # Artists
        if soup.find('div', {'class': 'AudioShowcase__block AudioShowcase__block_custom_image_small'}):  # noqa: E501
            data['artists'] = {
                'full': '',
                'list': []
            }

            get_all = soup.find('a', {'class': 'Pad__corner al_empty'})
            data['artists']['full'] = get_all['href'] if get_all else ''

            for link in soup.find_all('a', {'class': 'OwnerRow__content'}):
                data['artists']['list'].append({
                    'name': link.text,
                    'link': link['href']
                })

        # Playlists
        if soup.find('div', {'class': 'AudioBlock AudioBlock_playlists Pad'}):
            data['playlists'] = {
                'full': '',
                'list': []
            }

            get_all = soup.find('a', {'class': 'Pad__corner al_empty'})
            data['playlists']['full'] = get_all['href'] if get_all else ''

            for playlist in soup.find_all('div', {'class': 'audioPlaylists__item'}):  # noqa: E501
                link = playlist.find('a', {'class': 'audioPlaylists__itemLink al_playlist'})  # noqa: E501
                title = playlist.find('span', {'class': 'audioPlaylists__itemTitle'})  # noqa: E501
                subtitle = playlist.find('div', {'class': 'audioPlaylists__itemSubtitle'})  # noqa: E501

                data['playlists']['list'].append({
                    'link': link['href'],
                    'title': title.text if title else '',
                    'subtitle': subtitle.text if subtitle else ''
                })

        # Tracks
        if soup.find('div', {'class': 'AudioShowcase__block AudioShowcase__block_audios'}):  # noqa: E501
            data['tracks'] = {
                'full': '',
                'list': []
            }

            get_all = soup.find('a', {'class': 'Pad__corner al_empty'})
            data['tracks']['full'] = get_all['href'] if get_all else ''

            for track in soup.find_all('div', {'class': 'audio_item'}):
                data_id = track['data-id']
                title = track.find('span', {'class': 'ai_title'})
                artist = track.find('span', {'class': 'ai_artist'})

                data['tracks']['list'].append({
                    'data-id': data_id,
                    'title': title.text if title else '',
                    'artist': artist.text if artist else ''
                })

        return data

    def _auth(self):
        landing = self.session.get(
            'https://m.vk.com'
        )
        soup = BeautifulSoup(landing.text, 'html.parser')
        form_link = soup.find('form')['action']
        data = {
            'email': self.username,
            'pass': self.password
        }
        result = self.session.post(
            form_link,
            data=data
        )
        if result.url != 'https://m.vk.com/':
            sys.exit('Username or password are incorrect')
        else:
            logger.info('VK Authorized')
