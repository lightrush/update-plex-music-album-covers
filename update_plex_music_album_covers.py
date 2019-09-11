import click
import requests
from mutagen.id3 import ID3, PictureType, ID3NoHeaderError
from mutagen import MutagenError
from plexapi.compat import ElementTree
from plexapi.myplex import MyPlexAccount
import logging


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def get_plex(username, password, server):
    plex = None

    try:
        account = MyPlexAccount(username, password)
        logger.info("Logged into Plex.")
    except:
        logger.exception("Couldn't login to Plex. Are the credentials correct?")
        raise

    try:
        plex = account.resource(server).connect()
        logger.info("Connected to Plex server.")
    except:
        logger.exception("Couldn't connect to Plex server. Is the server correct and running?")
        raise

    return plex


def get_file_from_track(track):
    file_ = None

    if track.media:
        media = track.media[0]
        if media.parts:
            part = media.parts[0]
            file_ = part.file

    return file_


def get_front_cover_pic(file_):
    pic_front_cover = None

    try:
        tags = ID3(file_)
        pics = tags.getall("APIC")
        pics_front_cover = list(filter(lambda pic: pic.type == PictureType.COVER_FRONT, pics))
        if pics_front_cover:
            pic_front_cover = pics_front_cover[0].data

    except (ID3NoHeaderError, MutagenError):
        pass

    return pic_front_cover


@click.command()
@click.argument('username')
@click.option('--password', envvar='PLEX_PASSWORD', help='Plex account password')
@click.argument('server')
@click.argument('library')
def cli(username, password, server, library):
    """Set Plex music album covers to the corresponding front covers embedded in the contained MP3 files.

    USERNAME is the Plex account username to use.\n
    SERVER is the Plex server to connect to.\n
    LIBRARY is the Plex music library to work on.

    Password can be specified via the --password option or provided in the PLEX_PASSWORD environment variable.
    """

    try:
        plex = get_plex(username, password, server)

        music = None
        try:
            music = plex.library.section(library)
            logger.info("Retrieved Plex music library.")
        except:
            logger.exception("Couldn't get Plex music library. Is the specified music library correct?")
            raise

        try:
            albums = music.albums()
        except:
            logger.exception("Couldn't retrieve albums from library.")
            raise

        if not albums:
            logger.info("No albums found.")

        for album in albums:
            logger.info("Working on: {artist} - {album}".format(artist=album.parentTitle, album=album.title))

            posters_url = "{url}/posters".format(url=plex.url(album.key))
            container = None
            try:
                response = plex._session.get(posters_url, headers=plex._headers())
                response.raise_for_status()
                data = response.text.encode('utf8')
                container = ElementTree.fromstring(data) if data.strip() else None
            except:
                logger.exception("Couldn't fetch album convers from Plex.")
                raise

            if container and len(container) > 1:
                logger.info("Found multiple covers. Looking for embedded front cover...")

                # If we have different covers across multiple tracks in the same album
                # we have no good way to select one of them, therefore we'd choose a
                # one indiscriminately. If we are to choose a cover indiscriminately
                # we may as well pick the first one and avoid reading all files in the
                # album. So we do that.
                file_ = get_file_from_track(album.tracks()[0])
                front_cover_pic = get_front_cover_pic(file_)

                if front_cover_pic:
                    logger.info("Found an embedded cover. Updating album cover...")
                    try:
                        response = plex._session.post(posters_url, data=front_cover_pic, headers=plex._headers())
                        response.raise_for_status()
                        logger.info("Album cover updated successfully.")
                    except:
                        logger.exception("Couldn't update album cover in Plex.")
                        raise
                else:
                    logger.info("No embedded front covers found.")
            else:
                logger.info("Single or no cover found. Nothing to do.")

    except:
        exit(1)
