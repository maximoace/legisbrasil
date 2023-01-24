from webscrapper.webscrapper import WebScrapper

import os
import threading

def get_path():
    return os.path.dirname(__file__)

def start_browser():
    os.system(f"cmd /c explorer http://localhost:5000")

def start_flask():
    os.system(f"cmd /k {get_path()}\.venv\Scripts\\flask.exe --app website/app.py run")

if __name__ == '__main__':
    ws = WebScrapper()
    ws.start()
    threading.Thread(target=start_browser())
    start_flask()