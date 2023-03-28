#!/usr/bin/env python

import os
import sys
import subprocess
import re
import time
from typing import Tuple
import common
import _thread

import psutil

icon_fg=common.black
icon_bg=common.green
icon_tr="0xff"
text_fg=common.black
text_bg=common.green
text_tr="0xff"

icon_color="^c"+str(icon_fg)+"^^b"+str(icon_bg)+str(icon_tr)+"^"
text_color="^c"+str(text_fg)+"^^b"+str(text_bg)+str(text_tr)+"^"
DELAY_TIME=1

filename= os.path.basename(__file__)
name=re.sub("\..*",'',filename)


def update(loop=False,exec=True):
  while True :
    icon=" ﬘"
    text=str(int(psutil.virtual_memory()[2]))+"% "
    txt="^s"+str(name)+"^"+str(icon_color)+str(icon)+str(text_color)+str(text)
    common.write_to_file(txt+"\n",str(name))
    if loop == False : 
      if exec==True :
        os.system("xsetroot -name '"+str(txt)+"'")
      break
    time.sleep(DELAY_TIME)

def update_thread():
  _thread.start_new_thread(update,(False,False))

def click(string='') :
  match string:
    case 'L':
      pass
    case 'M':
      pass
    case 'R':
      pass
      os.system("alacritty -t statusutil --class floatingTerminal -e btop")
    case 'U':
      pass
    case 'D':
      pass
    case  _: pass

def notify(string='') :
  pass

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if(sys.argv[1]=="update") :
      pass
    else :
      click(sys.argv[1])
      update(exec=False)
  else :
    update()
   
