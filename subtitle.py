#!/usr/bin/env python
import os
import hashlib
import sys
import time
import subprocess

try:
    import urllib.request, urllib.parse
    pyVer = 3
except ImportError:
    import urllib2
    pyVer = 2

#this hash function receives the name of the file and returns the hash code
def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def sub_downloader(path):
    hash = get_hash(path)
    replace = [".avi",".mp4",".mkv",".mpg",".mpeg",".flv"]
    for content in replace:
        path = path.replace(content,"")
    if not os.path.exists(path+".srt"):
        headers = { 'User-Agent' : 'SubDB/1.0 (subtitle-downloader/1.0; http://github.com/manojmj92/subtitle-downloader)' }
        url = "http://api.thesubdb.com/?action=download&hash="+hash+"&language=en"
        if pyVer == 3:
            req = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(req).read()
        else:
            req = urllib2.Request(url, '', headers)
            response = urllib2.urlopen(req).read()
        with open (path+".srt","wb") as subtitle:
            subtitle.write(response)

path = sys.argv[1]
print "opening file "+path
try:
    sub_downloader(path)
    print "subtitles ready"
except:
    print "subtitles unavailable"	
time.sleep(1)
subprocess.call(["vlc",path])
