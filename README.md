# MyLyric

Add live display of lyrics to music files downloaded from NetEase Cloud Music (`163 key` included in metadata) that are being played in DeaDBeeF (or Foobar2000)

## How it works

See "Acknowledgments" below, I've sorted them according to the process, you should get a rough idea. In fact, the way it is implemented is quite funny, but it can work

## How to use

### Windows

### GNOME (Wayland or X)

## Acknowledgments

In building this project, we would like to acknowledge the contributions of the following references:

- Highly customizable music player: [DeaDBeeF-Player/deadbeef](https://github.com/DeaDBeeF-Player/deadbeef)
  - [wiki/Title-formatting-2.0](https://github.com/DeaDBeeF-Player/deadbeef/wiki/Title-formatting-2.0)
- Get title of windows on Windows: [Kalmat/PyWinCtl](https://github.com/Kalmat/PyWinCtl)
- Get title of windows on GNOME (Wayland or X): [jieran233/gnome-get-all-titles](https://github.com/jieran233/gnome-get-all-titles) (forked from [lucaswerkmeister/activate-window-by-title](https://github.com/lucaswerkmeister/activate-window-by-title))
- Read metadata of music file: [quodlibet/mutagen](https://github.com/quodlibet/mutagen)
- Decrypt AES in ECB mode: [Legrandin/pycryptodome](https://github.com/Legrandin/pycryptodome)
- NetEase Cloud Music API: [2061360308/NeteaseCloudMusic_PythonSDK](https://github.com/2061360308/NeteaseCloudMusic_PythonSDK)
  - [tree/main/docs#获取歌词](https://github.com/2061360308/NeteaseCloudMusic_PythonSDK/tree/main/docs#%E8%8E%B7%E5%8F%96%E6%AD%8C%E8%AF%8D)
  - [Binaryify/NeteaseCloudMusicApi](https://web.archive.org/web/20231226220526/https://github.com/Binaryify/NeteaseCloudMusicApi)
- Web server: [pallets/flask](https://github.com/pallets/flask)
- WebSocket: [Flask-SocketIO](https://github.com/miguelgrinberg/Flask-SocketIO)

`163 key` decrypting reference:

- [https://stageguard.top/2019/10/27/analyze-163-music-key/](https://web.archive.org/web/20230131233424/https://stageguard.top/2019/10/27/analyze-163-music-key/)

Lyric parsing references:

- [Steve-xmh/LibLyric](https://github.com/Steve-xmh/LibLyric)
  - [blob/main/src/index.ts](https://github.com/Steve-xmh/LibLyric/blob/main/src/index.ts)
- [jitwxs/163MusicLyrics](https://github.com/jitwxs/163MusicLyrics)
  - [blob/master/MusicLyricApp/Bean/NetEaseMusicBean.cs](https://github.com/jitwxs/163MusicLyrics/blob/master/MusicLyricApp/Bean/NetEaseMusicBean.cs)
