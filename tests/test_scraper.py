import unittest
import types
from genius_lyric_scraper import scraper

class TestScraper(unittest.TestCase):


    def test_scrap_returns_list_of_dicts(self):
        # Mock the dependencies to avoid real HTTP requests

        # Mock data
        fake_albums = [("album_url", "Fake Album", "2024")]
        fake_tracks = [("Fake Track", "track_url")]
        fake_lyrics = "Fake lyrics"

        # Patch functions
        scraper.get_albums = lambda url: fake_albums
        scraper.get_tracks = lambda url: fake_tracks
        scraper.get_lyrics = lambda url: fake_lyrics

        result = scraper.scrap("fake_url")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]['album'], "Fake Album")
        self.assertEqual(result[0]['data'], "2024")
        self.assertEqual(result[0]['musica'], "Fake Track")
        self.assertEqual(result[0]['letra'], "Fake lyrics")

if __name__ == "__main__":
    unittest.main()
