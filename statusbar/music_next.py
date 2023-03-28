#!/usr/bin/env python

import os
import sys
import subprocess
import re
import time
import _thread
import common

music_program=common.MUSIC_PROGRAM

icon_fg=common.black
icon_bg=common.blue
icon_tr="0xff"
text_fg=common.blue
text_bg=common.black
text_tr="0xff"

icon_color="^c"+str(icon_fg)+"^^b"+str(icon_bg)+str(icon_tr)+"^"
text_color="^c"+str(text_fg)+"^^b"+str(text_bg)+str(text_tr)+"^"
DELAY_TIME=5

filename= os.path.basename(__file__)
name=re.sub("\..*",'',filename)

def update(loop=False,exec=True):
  while True :
    icon="󰒭 "
    text=""
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
      os.system("playerctl next "+"-p "+str(music_program))
    case 'M':
      pass
    case 'R':
      pass
    case 'U':
      pass
    case 'D':
      pass
    case  _: pass

def notify(str='') :
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
   
