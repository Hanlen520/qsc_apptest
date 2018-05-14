# -*-coding:utf-8-*-
import sys
try:
    import ConfigParser
except ModuleNotFoundError:
    from configparser import ConfigParser

class Config(object):

    def __init__(self):
        configPath = 'config.ini'
        if sys.version_info >= (3,3):
            self.config = ConfigParser()
        else:
            self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        self.appConfig = self.App()
        self.adbConfig = self.ADB()
        self.logConfig = self.LOG()

    def APP(self):
        return dict(self.config.items("APP"))

    def ADB(self):
        return dict(self.config.items("ADB"))

    def LOG(self):
        return dict(self.config.items("LOG"))

if __name__ == '__main__':
    name = Config().appConfig['name']
    print(name)