import os
import random
from datetime import date

def changeIP():
    codes = ["TR","US-C","US","US-W","CA","CA-W","FR","DE","NL","NO","RO","CH","GB","HK"]
    try:
        os.system(f"windscribe connect {random.choice(codes)}")
    except: 
        os.system("windscribe disconnect")
        return False
    return True

def  timestamp():
    return date.today().isoformat()
