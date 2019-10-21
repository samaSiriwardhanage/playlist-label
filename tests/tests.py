import datetime
import json
import os
from unittest.mock import MagicMock, patch

from peewee import SqliteDatabase

from app.main import Message, PlaylistLabel


def file_to_string_strip_new_lines(filename):
    """
    Read file and return as string with new line characters stripped
    :param filename: a filename relative to the current working directory.
    e.g. 'xml_files/example.xml' or 'example.xml'
    :return: a string representation of the contents of filename, with new line characters removed
    """
    # get current working directory
    cwd = os.path.dirname(__file__)
    file_as_string = ""

    # open filename assuming filename is relative to current working directory
    with open(os.path.join(cwd, filename), 'r') as file_obj:
        # strip new line characters
        file_as_string = file_obj.read().replace('\n', '')
    # return string
    return file_as_string


def mocked_requests_get(*args, **kwargs):
    """
    Thanks to https://stackoverflow.com/questions/15753390/how-can-i-mock-requests-and-the-response
    """
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.content = json.loads(json_data)
            self.status_code = status_code

        def json(self):
            return self.content

        def raise_for_status(self):
            return None

    if args[0].startswith('https://museumos-prod.acmi.net.au/api/playlists/'):
        return MockResponse(file_to_string_strip_new_lines('data/playlist.json'), 200)

    return MockResponse(None, 404)


def test_message():
    """
    Test the Message class initialises.
    """

    DB = SqliteDatabase('message.db')
    DB.create_tables([Message])
    timestamp = datetime.datetime.now().timestamp()

    message = Message.create(
        datetime=timestamp,
        playlist_id=1,
        media_player_id=1,
        label_id=1,
        playback_position=0,
        audio_buffer=0,
        video_buffer=0,
    )
    assert message
    assert message.datetime is timestamp


@patch('requests.get', side_effect=mocked_requests_get)
def test_download_playlist_label(mocked_requests_get):
    """
    Test that downloading the playlist from XOS
    successfully saves it to the filesystem.
    """

    playlistlabel = PlaylistLabel()
    playlistlabel.download_playlist_label()
    file_exists = os.path.isfile('playlist_1.json')
    playlist = json.loads(file_to_string_strip_new_lines('../playlist_1.json'))['playlist_labels']

    assert file_exists is True
    assert len(playlist) == 3
    assert playlist[0]['label']['title'] == 'Dracula'


def test_process_media():
    """
    Test the process_media function creates a valid Message.
    """

    message_broker_json = json.loads(file_to_string_strip_new_lines('data/message.json'))
    playlistlabel = PlaylistLabel()
    mock = MagicMock()
    playlistlabel.process_media(message_broker_json, mock)
    saved_message = Message.get(Message.datetime == message_broker_json['datetime'])

    mock.ack.assert_called_once()
    assert message_broker_json['label_id'] == saved_message.label_id
