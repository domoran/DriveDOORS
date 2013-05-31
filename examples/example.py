import os
import sys

API_ROOT = os.path.realpath(os.path.join(__file__, "..", "..", "api", "python"))
sys.path.append(API_ROOT)

from DriveDOORS import DOORS
import types

doors = DOORS(username = "Administrator", password = "") 

ItemTree = eval(doors.executeDatalet ("getHierarchy", baseItem="/Playground"))


def processTree(items, level = 0):
    for i in items:
        if type(i) == types.StringType:
            print ("--" * level) + ((level or "") and "> ") + i
        elif type(i) == types.ListType:
            processTree(i, level+1)


processTree (ItemTree)
        
