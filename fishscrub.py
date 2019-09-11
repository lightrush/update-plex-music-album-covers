#! /usr/bin/env python3

import click
from mutagen.id3 import ID3, APIC, PictureType, ID3NoHeaderError

APIC = "APIC"

@click.command()
@click.argument('file')
def scrub(file):
    """Scrub fish pics from MP3 file."""
    print("Scrubbing fish from: {file}".format(file=str(file)))
    
    try:
        tags = ID3(file)
        
        pics = tags.getall(APIC)
        pics_fishfree = list(filter(lambda pic: pic.type != PictureType.FISH, pics))
        if len(pics_fishfree) != len(pics):
            tags.setall(APIC, pics_fishfree)
            tags.save()
    
    except ID3NoHeaderError:
        print("No ID3 tags found.")
    
    except Exception as e:
        print("Error occured: {msg}".format(msg=str(e)))

if __name__ == '__main__':
    scrub()
