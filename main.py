import json

from NeteaseCloudMusic import NeteaseCloudMusicApi

import lrc
from os_de import *
from music163key import get_decrypted_music163key
import lang
import fonts

from flask import Flask, render_template
from flask_socketio import SocketIO


# Get the system platform
current_os_de = get_os_de()

# Import library for getting titles corresponding to the system platform
if current_os_de == os_de['windows']:
    import title_win as title
elif current_os_de == os_de['linux_gnome']:
    import title_gnome as title

# Initialize the Netease Cloud Music API
netease_cloud_music_api = NeteaseCloudMusicApi()

# Constants for lyrics html generation
innerhtml_placeholder = '{lyric}'
lang_class_placeholder = '{lang}'
paired_tag = 'p'
all_lrc_class = 'lrc-all'

# List of all lrc types
all_lrc_types = ['lrc', 'klyric', 'tlyric', 'romalrc']

# Generate html for all lrc type (e.g. 'lrc': '<p class="lrc-all lrc {lang}">{lyric}</p>')
all_lrc_types_html = {lrc_type: (f'<{paired_tag} class="{all_lrc_class} {lrc_type} {lang_class_placeholder}">'
                                 f'{innerhtml_placeholder}</{paired_tag}>')
                      for lrc_type in all_lrc_types}

# Download fonts
fonts.download_fonts()

# Time offset for lyrics (in seconds)
offset = 0.5

# Variables to track the last path and last lyrics line
last_path = last_lyrics_line = None
# Variables to store lrc related data
lrc_list = lrc_parsed = valid_lrc_types = None


def time_to_seconds(time_str: str):
    """
    Convert time string in format 'hh:mm:ss', 'mm:ss', or 'ss' to seconds.
    """
    components = time_str.split(':')
    if len(components) == 1:
        return float(components[0])
    elif len(components) == 2:
        minutes = int(components[0])
        seconds = float(components[1])
        return minutes * 60 + seconds
    elif len(components) == 3:
        hours = int(components[0])
        minutes = int(components[1])
        seconds = float(components[2])
        return hours * 3600 + minutes * 60 + seconds
    else:
        return None


def changedTitleCB(_title: str):
    """
    Callback function for title change.
    """
    global last_path, last_lyrics_line, lrc_list, lrc_parsed, valid_lrc_types

    # Parse title information
    title_info = json.loads(_title.lstrip(title.title_left).rstrip(title.title_right))
    path = title_info['path']
    time = time_to_seconds(title_info['time'].split('/')[0])
    print(title_info)

    # read music163key, retrieve lyric
    if path != last_path:
        last_path = path

        # Retrieve music163key
        music163key = json.loads(get_decrypted_music163key(path))
        music_id = music163key['musicId']
        print(music163key)
        # === '/lyric' api ===
        # https://github.com/2061360308/NeteaseCloudMusic_PythonSDK/tree/main/docs#%E8%8E%B7%E5%8F%96%E6%AD%8C%E8%AF%8D
        # - lrc: lrc
        # - klyric: ???
        # - tlyric: translated lrc
        # - romalrc: romaji lrc
        # all are standard lrc format

        # Retrieve lyrics data from Netease Cloud Music API
        lyric_response_data = netease_cloud_music_api.request('/lyric', {'id': music_id})['data']
        lrc_list = {}
        lrc_parsed = {}
        valid_lrc_types = []

        # Parse and store lyrics data for each lrc type
        for lrc_type in all_lrc_types:
            if lrc_type in lyric_response_data and lyric_response_data[lrc_type]['lyric'] != '':
                valid_lrc_types.append(lrc_type)
                lrc_list[lrc_type] = lyric_response_data[lrc_type]['lyric'].splitlines()
                lrc_parsed[lrc_type] = lrc.parse_lrc(lyric_response_data[lrc_type]['lyric'])

        print(lyric_response_data)

    # Extract lyrics lines based on current time
    now_lyrics_line = {}
    for lrc_type in valid_lrc_types:
        if lrc_parsed[lrc_type] != {}:
            line = lrc.get_lyric_at_time(lrc_parsed[lrc_type], float(time + offset))[0]
            content = lrc_list[lrc_type][line].split(']', 1)[1].strip()
            now_lyrics_line[lrc_type] = {'line': line, 'content': content}

    # Update UI only if lyrics have changed
    if now_lyrics_line != last_lyrics_line:
        last_lyrics_line = now_lyrics_line
        print(now_lyrics_line)
        data = ''
        for lrc_type in valid_lrc_types:
            if now_lyrics_line:
                # Replace placeholders
                _lrc = now_lyrics_line[lrc_type]['content']
                lyric_html = (all_lrc_types_html[lrc_type]
                              .replace(innerhtml_placeholder, _lrc)
                              .replace(lang_class_placeholder, lang.identify_language(_lrc)))
                data += lyric_html
        data = data.rstrip('<br/>')
        socketio.emit('update', {'data': data})


if __name__ == '__main__':
    # Initialize Flask app and SocketIO
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    # Flag to track whether background task is running
    run_background_task = False


    @app.route('/')
    def index():
        """
        Render index.html template.
        """
        return render_template('index.html',
                               fonts=fonts.fonts, font_family=fonts.font_family, languages=lang.languages)


    def background_thread():
        """
        Background task to monitor title changes.
        """
        title.set_title_change_polling(callback=changedTitleCB)


    @socketio.on('connect')
    def connect():
        """
        Event handler for client connection.
        """
        global run_background_task
        if not run_background_task:
            print('Client connected')
            socketio.start_background_task(target=background_thread)
            run_background_task = True


    # Run the Flask app with SocketIO
    # socketio.run(app, allow_unsafe_werkzeug=True)
    socketio.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0')
