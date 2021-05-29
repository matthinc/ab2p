#!/usr/bin/env python3
"""Generates Podcast rss-feeds and a Caddyfile based on the content
(sub-directories and mp3 files) of the given 'BASEDIR'"""

import os
import sys
from natsort import natsorted
from jinja2 import Environment, FileSystemLoader

def get_sub_directories(directory):
    """Returns all not-hidden sub-dirs of directory"""

    entries = os.scandir(directory)
    # Remove all entries that are not directoryectories
    directorys = [directory for directory in entries
        if directory.is_dir() and not directory.name.startswith(".")]
    # Return the names of the sub directoryectories in natural order
    return natsorted([directory.name for directory in directorys])

def get_mp3_files(directory):
    """Returns all .mp3 files within directory"""

    entries = os.scandir(directory)
    # Remove all entries that are not directoryectories
    audio_files = [f for f in entries if f.is_file() and f.name.endswith(".mp3")]
    # Return filenames in natural order
    return natsorted([f.name for f in audio_files])

def end_with_slash(url):
    """Makes sure the given url or filename ends witn a slash"""

    if not url.endswith("/"):
        return url + "/"

    return url

def get_full_directory(base, directory):
    """Concatenates base and directory to a absolute path"""

    return end_with_slash(base) + directory

def scan_for_mp3(base, directory, files):
    """Scans the given directory for mp3 files recursively"""

    # Add mp3 files first...
    for file in get_mp3_files(get_full_directory(base, directory)):
        files.append({
            "path": directory + "/" + file,
            "file": file
        })

    # ...Then scan sub directoryectories
    for sub_directory in get_sub_directories(get_full_directory(base, directory)):
        scan_for_mp3(base, directory + "/" + sub_directory, files)

    return files

def feed_for_directory(hostname, base, directory):
    """Generate a podcast rss-feed containing all mp3 files in this directory"""

    feed = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    feed += "<rss version=\"2.0\" xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\">"
    feed += "<channel>"
    feed += "<title>" + directory + "</title>"
    feed += "<description>" + directory + "</description>"
    feed += "<itunes:type>episodic</itunes:type>"

    for file in scan_for_mp3(base, directory, []):
        feed += "<item>"
        feed += "<title>" + file["file"] + "</title>"
        feed += "<enclosure url=\""
        feed += end_with_slash(hostname) + file["path"] + "\" type=\"audio/mpeg\" />"
        feed += "</item>"

    feed += "</channel>"
    feed += "</rss>"

    # Write feed to xml file
    with open(get_full_directory(base, directory)+ ".xml", "w") as file:
        file.write(feed)

def import_directorys(hostname, base):
    """Generate rss feeds for all sub-directories in the given base path"""

    for entry in os.scandir(base):
        if entry.is_dir():
            feed_for_directory(hostname, base, entry.name)

def render_caddyfile(hostname, basedirectory):
    """Renders the j2 template to a Caddyfile"""

    jinja_env = Environment(loader=FileSystemLoader('.'))
    template = jinja_env.get_template(name = "./Caddyfile.j2")
    result = template.render(hostname = hostname, basedir = basedirectory)

    with open("Caddyfile", "w") as file:
        file.write(result)

def main():
    """Runs the import script"""

    hostname = os.getenv("HOSTNAME")
    basedirectory = os.getenv("BASEDIR")

    if (not hostname) or (not basedirectory):
        sys.exit("Please specify the 'HOSTNAME' and 'BASEDIR' environment variable.")

    import_directorys(hostname, basedirectory)
    render_caddyfile(hostname, basedirectory)

if __name__ == "__main__":
    main()
