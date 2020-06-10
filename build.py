import subprocess
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def build():
    os.chdir(os.path.join(BASE_PATH, 'frontend', 'static_src'))
    subprocess.run(["npm", "install"])
    subprocess.run(["npm", "run", "build"])
    os.chdir(BASE_PATH)
    subprocess.run(["poetry", "build"])


'''
Custom build script to bundle assets before build.
Should be obsolete once poetry 1.1 is released
https://github.com/python-poetry/poetry/issues/1856
https://github.com/python-poetry/poetry/issues/537
https://github.com/python-poetry/poetry/issues/1992
'''
if __name__ == '__main__':
    build()
