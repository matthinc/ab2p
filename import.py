#!/usr/bin/env python3
import os
from natsort import natsorted

def get_sub_directories(dir):
    entries = os.scandir(dir)
    # Remove all entries that are not directories
    dirs = [dir for dir in entries if dir.is_dir() and not dir.name.startswith(".")]
    # Return the names of the sub directories in natural order
    return natsorted([dir.name for dir in dirs])

def get_mp3_files(dir):
    entries = os.scandir(dir)
    # Remove all entries that are not directories
    audioFiles = [f for f in entries if f.is_file() and f.name.endswith(".mp3")]
    # Return filenames in natural order
    return natsorted([f.name for f in audioFiles])

def get_jpeg_files(dir):
    entries = os.scandir(dir)
    # Remove all entries that are not directories
    jpegFiles = [f for f in entries if f.is_file() and f.name.endswith(".jpg")]
    # Return filenames in natural order
    return natsorted([f.name for f in jpegFiles])

# /a/b/c -> /a/b/c/
def end_with_slash(url):
    if not url.endswith("/"):
        return url + "/"
    else:
        return url

def get_full_dir(base, dir):
    return end_with_slash(base) + dir

def scan_for_mp3(base, dir, files):
    # Add mp3 files first...
    for file in get_mp3_files(get_full_dir(base, dir)):
        files.append({
            "path": dir + "/" + file,
            "file": file
        })

    # ...Then scan sub directories
    for sub_dir in get_sub_directories(get_full_dir(base, dir)):
        scan_for_mp3(base, dir + "/" + sub_dir, files)

    return files

def feed_for_dir(hostname, base, dir):
    feed = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    feed += "<rss version=\"2.0\" xmlns:itunes=\"http://www.itunes.com/dtds/podcast-1.0.dtd\" xmlns:atom=\"http://www.w3.org/2005/Atom\">"
    feed += "<channel>"
    feed += "<title>" + dir + "</title>"
    feed += "<description>" + dir + "</description>"
    feed += "<itunes:type>episodic</itunes:type>"

    for file in scan_for_mp3(base, dir, []):
        feed += "<item>"
        feed += "<title>" + file["file"] + "</title>"
        feed += "<enclosure url=\"" + end_with_slash(hostname) + file["path"] + "\" type=\"audio/mpeg\" />"
        feed += "</item>"
    
    feed += "</channel>"
    feed += "</rss>"

    # Write feed to xml file
    with open(get_full_dir(base, dir)+ ".xml", "w") as f:
        f.write(feed)

def import_dirs(hostname, base):
    for entry in os.scandir(base):
        if entry.is_dir():
            feed_for_dir(hostname, base, entry.name)

import_dirs(os.getenv("HOSTNAME"), os.getenv("BASEDIR"))