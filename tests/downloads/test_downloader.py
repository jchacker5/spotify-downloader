import os
import pytest
from unittest.mock import patch
from spotdl.download.downloader import Downloader, Song, DownloaderError, NoSearchResultsException

@pytest.fixture
def downloader():
    return Downloader()

@patch('spotdl.download.downloader.Downloader.search_and_download')
def test_search_no_results(mock_search_and_download, downloader):
    # Configure the mock to raise NoSearchResultsException
    mock_search_and_download.side_effect = NoSearchResultsException("No search results found.")

    song = Song(
        name="Dummy Song",
        artists=["Dummy Artist"],
        artist="Dummy Artist",
        url="http://valid.url",  # Use a valid URL format to avoid URL validation issues
        genres=[],
        disc_number=1,
        disc_count=1,
        album_name="Dummy Album",
        album_artist=["Dummy Album Artist"],
        duration=0,
        year=2024,
        date=None,
        track_number=1,
        tracks_count=1,
        song_id=None,
        explicit=False,
        publisher=None,
        isrc=None,
        cover_url=None,
        copyright_text=None
    )

    # Expect the NoSearchResultsException to be raised
    with pytest.raises(NoSearchResultsException):
        downloader.search_and_download(song)

    # Check if the method was called once
    mock_search_and_download.assert_called_once_with(song)
