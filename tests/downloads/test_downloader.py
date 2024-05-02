import os
import pytest
from unittest.mock import patch
from spotdl.download.downloader import Downloader, Song, DownloaderError

@pytest.fixture
def downloader():
    return Downloader()

@patch('spotdl.download.downloader.YouTube.search')
def test_search_no_results(mock_search, downloader):
    # Configure the mock to return None
    mock_search.return_value = None

    # Create a dummy Song object with all required arguments
    song = Song(
        name="Dummy Song",
        artists=["Dummy Artist"],
        artist="Dummy Artist",
        url="dummy_url",
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

    # Ensure the file does not exist before the download
    assert not os.path.exists("failedsonglog.txt")

    # Attempt to download the song (which should fail)
    try:
        downloader.search_and_download(song)
    except Exception as e:
        print(f"Exception occurred during download attempt: {e}")

    # Check if the file is created after the failed download
    file_exists = os.path.exists("failedsonglog.txt")
    print(f"File exists after download attempt: {file_exists}")

    # Check if the song is logged correctly in the file
    if file_exists:
        with open("failedsonglog.txt", "r") as file:
            content = file.read()
            print(f"Content of failedsonglog.txt: {content}")
            assert song.display_name in content

    # Assert that the file is created after the failed download
    assert file_exists
