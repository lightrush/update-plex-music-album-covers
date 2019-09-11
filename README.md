# update-plex-music-album-covers

Is your Plex showing waveforms or label covers instead of the posters (covers) you worked or paid for?

Update Plex music album covers to the corresponding front covers embedded in your MP3 files.

## Rationale

This utility was written as a solution to a problem with Plex Media Server and music album covers.
Some MP3 files such as the ones purchased from Beatport come with the usual cover one would expect
as well as an additional waveform image. They often include a label cover too.
When scanning files for covers Plex Media Server sees all of these and selects one seemingly
at random. This utility scans your music library for albums with multiple covers, attempts
to extract the embedded front covers from the MP3 files themselves and updates the album
covers with the those. The MP3 files are not modified in this process.

## Running

Install via PIP on the same machine where you Plex server is running:
```bash
pip3 install --user update-plex-music-album-covers
```

Run:
```bash
update-plex-music-album-covers USERNAME --password PASSWORD SERVER LIBRARY
```

If you want to conceal your password you can pass it via environment variable like so:
```bash
read -p "Enter your password: " -s PLEX_PASSWORD && export PLEX_PASSWORD
update-plex-music-album-covers USERNAME SERVER LIBRARY
```
