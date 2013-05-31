import tempfile
import subprocess
import os
import __main__

import DataMappers

class DoorsServer:
    def executeDatalet(dataletName, *pars, **kwargs):
        print "Executing datalet %s" % dataletName
    
    def startupServer(self):
        print "Starting up Server ..."
        runnerExecutable = os.path.abspath(os.path.join(os.path.basename(__file__), "..", "..", "..", "runner", "runServer.bat"))
        self.serverProcess = subprocess.Popen([runnerExecutable, "server1"])
        print runnerExecutable 
            
    def sendServer (self, data):
        if self.socket != None: 
            self.socket.send(data);
        else:
            print "Cannot send: " + data 
    
    def __init__ (self):
        self.socket = None
        self.serverProcess = None
        
        self.startupServer()
        
    
    def shutdownServer(self):
        self.sendServer("\n// TERMINATE_SERVER\n");
        
    def __del__ (self): 
        self.shutdownServer()        
        # if self.serverProcess != None: self.serverProcess.kill();


if __name__ == '__main__':
    d = DoorsServer();
    
    for i in range(1):
        d.executeDatalet('HelloWorld', baseItem = "/")
