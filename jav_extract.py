from __future__ import print_function
import time
import threading
import pyperclip
import re
import urllib


DEBUG = True
PATTERN_EMBED_PAGE = [
    re.compile(r'//(avcdn1\.xyz|sixav\.com)[^"]+'),
    re.compile(r'http://sixav\.com/video\.php\?[^"]+'),
]

PATTERN_VIDEO_PATH= [
     re.compile(r'(https://redirector[^"]+)'),
     re.compile(r'(http://[^"]+)'),
]

def debug_print(string):
    if DEBUG:
        print(string)

def is_valid_url(input_txt):
    if re.match(r'http://jav123.com/zh/\d+', input_txt) is not None:
        return True
    return False

def find_video_path(jav_url):
    page = urllib.urlopen(jav_url).read()
    
    debug_print("Matching embed page urls:")
    for pattern in PATTERN_EMBED_PAGE:
        debug_print("= Pattern = {}".format(pattern.pattern))
        mo = pattern.search(page)
        debug_print("== result = {}".format(mo is not None))
        
        if mo is not None:
            break
    else:
        print('Error on searching in video page')
        return
    
    if not mo.group(0).startswith('http'):
        embed_url = 'http:' + mo.group(0)
    else:
        embed_url = mo.group(0)
    debug_print("Embed url = {}".format(embed_url))
    
    embed_page = urllib.urlopen(embed_url).read()
    debug_print("Matching video paths:")
    for pattern in PATTERN_VIDEO_PATH:
        debug_print("= Pattern = {}".format(pattern.pattern))
        mo_embed = pattern.search(embed_page)
        debug_print("== result = {}".format(mo_embed is not None))
        if mo_embed is not None:
            break
    else:
        print('Error on searching in embed page')
        return
    pyperclip.copy(mo_embed.group(0))
    print('Copy Video Path Successfully.')
    debug_print("Video path = {}".format(mo_embed.group(0)))


class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):
        print("Monitoring Clipboard...")
        last_value = None
        while not self._stopping:
            current_value = pyperclip.paste()
            if current_value != last_value:
                last_value = current_value
                if self._predicate(current_value):
                    self._callback(current_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True

if __name__ == '__main__':
    watcher = ClipboardWatcher(is_valid_url, find_video_path, 0.5)
    watcher.start()
    
