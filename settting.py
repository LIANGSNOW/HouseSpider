import os

ROOT = os.path.abspath(os.path.dirname('setting.py'))

APP_DATA= os.path.join(ROOT,'data')

if __name__ == '__main__':
    print(APP_DATA)