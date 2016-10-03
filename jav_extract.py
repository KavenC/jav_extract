from __future__ import print_function
import time
import threading
import pyperclip
import re
import urllib

def is_valid_url(input_txt):
    if re.match(r'http://jav123.com/\d+', input_txt) is not None:
        return True
    return False

def find_video_path(jav_url):
    page = urllib.urlopen(jav_url).read()
    mo = re.search(r'http://sixav.com/video.php\?videoid=\w+', page)
    if mo is None:
        print('Error on opening video page')
        return
    
    embed_url = mo.group(0)
    embed_page = urllib.urlopen(embed_url).read()
    mo_embed = re.search(r'http://[^"]+', embed_page)
    if mo_embed is None:
        print('Error on opening embed page')
        return
    pyperclip.copy(mo_embed.group(0))
    print('Copy Video Path Successfully.')    


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
    
