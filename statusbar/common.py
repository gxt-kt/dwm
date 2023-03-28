#!/usr/bin/env python

import os
import fcntl
# import sys
# import subprocess
import re
import threading
# import time

PACKAGES_LISTS={
               'music_title':1,
               'music_pre':10,
               'music_play':1,
               'music_next':10,
               'icon':100,
               'screen':3,
               # 'pacman':36000,
               'net':1,
               'cpu':2,
               'memory':2,
               'wifi':2,
               'vol':1,
               'battery':3,
               'date':1,
               }



DWM_PATH="/home/gxt_kt/my_desktop/dwm/"
PACKAGES_PATH=DWM_PATH+"statusbar/"
TEMP_FILE="/home/gxt_kt/python_tmp"

MUSIC_PROGRAM="yesplaymusic"

black="#1e222a"
white="#D8DEE9"
grey="#373d49"
blue="#81A1C1"
blue2="#5E81AC"
blue3="#88C0D0"
blue4="#8FBCBB"
red="#d47d85"
green="#A3BE8C"
pink="#B48EAD"
yellow="#EBCB8B"
orange="#D08770"
darkblue="#7292b2"

threadLock = threading.Lock()
def write_to_file(string,package_name):
  threadLock.acquire()
  if (os.path.exists(TEMP_FILE)==False):
    os.system("touch "+TEMP_FILE)
  with open(TEMP_FILE, 'r+') as f:
    lines=f.readlines()
  with open(TEMP_FILE, 'w+') as f:
    find=False
    for line in lines :
      if re.match("^\^s",line) == None :
        continue
      flag=re.match("^\^s"+package_name,line)
      if flag==None :
        f.write(line)
      else :
        f.write(string)
        find=True
    if find==False :
      f.write(string)
  threadLock.release()

if __name__ == "__main__":
  pass
   
