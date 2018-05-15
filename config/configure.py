# -*- coding:utf-8 -*-
import sys,os
try:
    import ConfigParser
except ModuleNotFoundError:
    from configparser import ConfigParser

class Configure(object):

    def __init__(self):
        self.configPath = (os.path.dirname(sys.path[0])) + '/config/config.ini'
        if sys.version_info >= (3,3):
            self.config = ConfigParser()
        else:
            self.config = ConfigParser.ConfigParser()
        self.config.read(self.configPath)

    @property
    def configure(self):
        config = {}
        sections = self.config.sections()
        for i in sections:
            config = dict(config,**dict(self.config.items(i)))
        return config

    @configure.setter
    def configure(self, *value):
        self.config.set(section = list(*value)[0],option = list(*value)[1],value = list(*value)[2])
        with open(self.configPath,"w+") as f:
            self.config.write(f)

    def getConfigure(self):
        return self.configure

    def setConfigure(self,section,key,value):
        self.configure = (section,key,value)

class Config(Configure):

    def __init__(self):
        super(Config,self).__init__()
        for k,v in self.getConfig.items():
            setattr(self,k,v)

    @property
    def getConfig(self):
        return self.getConfigure()

    def setConfig(self,section,key,value):
        self.setConfigure(section,key,value)



if __name__ == '__main__':
    # b = Configure()
    # b.setConfigure(section = "APP",key = "name",value = "zyzy")
    a = Config()
    print(a.getConfig)
