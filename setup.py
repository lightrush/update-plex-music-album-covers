from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='update-plex-music-album-covers',
    keywords='update plex music album covers',
    version='0.1.2',
    author="Nicolay Doytchev",
    author_email="self@ndoytchev.com",
    description="Update Plex music album covers to the corresponding front covers embedded in your MP3 files",
    url="https://github.com/lightrush/update-plex-music-album-covers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['update_plex_music_album_covers'],
    install_requires=[
        'Click',
        'mutagen',
        'plexapi',
    ],
    entry_points='''
        [console_scripts]
        update-plex-music-album-covers=update_plex_music_album_covers:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)
