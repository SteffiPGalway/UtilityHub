import os
import time

def cleanup(directory, days):
    now = time.time()
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        if os.stat(filepath).st_mtime < now - days * 86400:
            os.remove(filepath)
