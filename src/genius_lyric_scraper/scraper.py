"""

CSV =

Album: Labirinto da ...
Data: 2024
Musica: Adeus adeus
letra: A vida permeava...

Labirinto da ...,2024,Adeus adeus,A vida permeava...
"""

from csv import DictWriter

import dateparser
from httpx import get
from parsel import Selector


url = 'https://genius.com/artists/Dead-fish/albums'

def get_lyrics(url: str) -> str:
    """
    Get the lyrics of a song.
    """
    response = get(url)
    s = Selector(response.text)
    return '\n'.join(s.css('[data-lyrics-container]::text').getall())

def get_tracks(url: str) -> list[tuple[str, str]]:
    """
    Get the tracks of an album.
    """
    response = get(url)
    s = Selector(response.text)
    tracks = s.css('div.chart_row-content')
    return [
        (track.css('h3::text').get().strip(), track.css('a').attrib['href'])
        for track in tracks
    ]

def get_albums(url: str) -> list[tuple[str | None, ...]]:
    """
    Get the albums of an artist.
    """
    response = get(url)
    s = Selector(response.text)
    albums = s.css('.ZvWhZ')
    result = []
    for album in albums:
        album_url = album.css('.kqeBAm').attrib['href']
        album_name = album.css('.gpuzaZ::text').get()
        album_year = album.css('.cedmJJ::text').get()
        result.append((album_url, album_name, album_year))
    return result

def scrap(url: str) -> list[dict[str, str]]:
    """
    Scrape the lyrics of an artist.
    """
    result = []
    for album in get_albums(url):
        for track in get_tracks(album[0]):
            result.append({
                    'album': album[1],
                    'data': album[2],
                    'musica': track[0],
                    'letra': get_lyrics(track[1])
            })
    return result

def save_csv() -> None:
    with open('deadfish.csv', 'w') as f:
        writer = DictWriter(f, ['album', 'data', 'musica', 'letra'])
        writer.writeheader()
        for disco in get_albums(url):
            for faixa in get_tracks(disco[0]):
                row = {
                    'album': disco[1],
                    'data': disco[2],
                    'musica': faixa[0],
                    'letra': get_lyrics(faixa[1])
                }
                print(row)
                writer.writerow(row)
