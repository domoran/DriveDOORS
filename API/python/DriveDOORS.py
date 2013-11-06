import time
import tempfile
import subprocess
from subprocess import PIPE
import os
import __main__
import socket 
import DataMappers

def getDriveDOORSRoot(): 
    sPath = os.path.dirname(__file__)
    while not os.path.exists(os.path.join(sPath, "README.md")):
        sPath = os.path.dirname(sPath)
    return sPath

class DoorsServer:
    DISCONNECTED = 1 # no connection to the server
    CONNECTED    = 2 # connect has been performed
    READY        = 3 # handshake has been performed
    
    def startupServer(self, configuration):
        print ("Starting up Server ...")
        root = getDriveDOORSRoot()
        libdir = os.path.join(root, "lib", "dxl")
        dxlserver = os.path.join(root, "runner", "DxlServer.dxl")
        runnerExecutable = os.path.abspath(os.path.join(root, "runner", "runDoors.bat"))
        
        cmdlist = [runnerExecutable, configuration, "-a",  libdir, "-b",  dxlserver]
        print ("Running:", cmdlist) 
        self.serverProcess = subprocess.Popen(cmdlist, stdout=PIPE)
        
    def connectToServer (self):
        try:
            self.socket = socket.socket()
            self.socket.connect( ("localhost", 2030) )
            self.socket.settimeout(1)
            self.state = self.CONNECTED
        except ConnectionRefusedError:
            self.socket = None
            self.state = self.DISCONNECTED
            
    def ensureConnectionReady(self):
        if self.state == self.DISCONNECTED:
            self.connectToServer()
        
        # perform handshake
        if self.state == self.CONNECTED:
            self.sendServer(b"DXLURDY?")

            try:
                response = self.socket.recv(8)
            except socket.timeout:
                response = b"TIMEOUT"

            if response == b"TIMEOUT": 
                self.disconnect()
                raise RuntimeError("Timeout while waiting for handshake!")
            
            if response != b"YAMERDY!":
                self.disconnect()
                raise RuntimeError("Invalid handshake response: %s" % response.decode("utf-8"))
        
            self.state = self.READY
    
    def executeDatalet(self, dataletName, *pars, **kwargs):
        self.ensureConnectionReady()
        
        if self.state != self.READY: raise RuntimeError("Socket not open! Use connectToServer before starting programs!")
        print ("Executing datalet %s" % dataletName)
        self.sendServer(b'print "Hallo" //END_OF_PROGRAM\n')

    def disconnect (self):
        if self.socket:
            self.socket.shutdown(self.SHUT_RDWR)
            self.socket.close()
            self.socket = None
            self.state = "disconnected"

    def sendServer (self, data):
        if self.socket != None: 
            self.socket.send(data);
        else:
            print ("Cannot send: ", data) 
    
    def __init__ (self, configuration = "server1"):
        self.port = 2030; 
        self.serverProcess = None
        self.socket = None
        self.state  = "disconnected"
        self.SHUT_RDWR = socket.SHUT_RDWR

        # startup a server if necessary ...        
        if not self.connectToServer():
            self.startupServer(configuration)
        
            retries = 0
            while retries < 5 and not self.state != self.DISCONNECTED: 
                self.connectToServer()
                time.sleep(0.5)
                retries += 1
    
    def shutdownServer(self):
        if not self.socket: raise RuntimeError("Socket not open! Use connectToServer before starting programs!")
        self.sendServer(b"\n// TERMINATE_SERVER\n");
        
        if self.serverProcess: 
            self.serverProcess.wait(5)
            if self.serverProcess.poll() != None: self.serverProcess.terminate()
        
    def __del__(self):
        self.disconnect()

if __name__ == '__main__':
    d = DoorsServer();
    
    for i in range(10):
        d.executeDatalet('HelloWorld', baseItem = "/")
        
    d.shutdownServer()

