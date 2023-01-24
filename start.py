import os

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    print(path)
    os.system(f"cd /d {path} & cmd /k {path}\.venv\Scripts\python.exe {path}\main.py")
