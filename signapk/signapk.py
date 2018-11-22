import subprocess


class Signer:

    def __init__(self):
        pass

    def start(self):
        pass

    def sign(self):
        p = subprocess.Popen('adb install -r ' + path, stdout=subprocess.PIPE)
        pass

