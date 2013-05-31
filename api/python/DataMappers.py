class BasicDataMapper: 
    def __init__(self):
        pass
    
    def makeStringValue (self, value):
        pass
        
    def writeParameterFile (self, datadir):
        pass
        

class StringMapper(BasicDataMapper):
    def __init__(self, datadir, parameterNumber, value = ""):
        self.parameterNumber = parameterNumber
        self.datadir = value
        self.value = value
    
    def writeParameterFile(self):
        pass