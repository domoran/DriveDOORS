import tempfile
import subprocess
import os
import __main__

class DOORS:
    DOORSPATH = r"C:\Programme\IBM\Rational\DOORS\9.3\bin"

    ROOTDIR = os.path.dirname(os.path.dirname(os.path.dirname(__main__.__file__)))
    LIBDIR  = os.path.join(ROOTDIR, "lib", "dxl")
    DATALETDIR  = os.path.join(ROOTDIR, "DATALETS")
 
    PREFIXCODE = \
    """
    // Put this code to a file called 'redirection.inc'
    void print (Date d) { cout << d "" }
    void print (string s) { cout << s }
    void print (int i) { cout << i "" }
    void print (char c) { cout << c "" }
    void print (bool b) { cout << b "" }
    void print (real r) { cout << r "" }
    """

    def launchDXL (self, sCode):
        with tempfile.NamedTemporaryFile(delete=False) as flTmp:
            flTmp.write(DOORS.PREFIXCODE)
            flTmp.write(sCode)
            flTmp.close()
            
            print flTmp.name

            doorsexe = os.path.join(DOORS.DOORSPATH, "doors.exe")

            args = [doorsexe, "-a", DOORS.LIBDIR + ";" + DOORS.DATALETDIR, "-W", "-b", flTmp.name, "-u", self.username]
            if self.password:
                args.extend("-P", self.password)

            val = subprocess.check_output(args)

            print "DXL Returned = " + str(val)
            return val
        

    def __init__ (self, username = "Administrator", password = ""):
        self.username = username
        self.password = password


    def executeDatalet(self, name, *args, **kwargs):
        return self.launchDXL("#include <" + name  + ".dxl>")
        

if __name__ == '__main__':
    print DOORS.LIBDIR
    d = DOORS()
    for i in range(10):
        d.executeDatalet('HelloWorld', baseItem = "/")
