#!/usr/bin/env python

import os
import sys
import subprocess
import re
import time
import _thread
import common


icon_fg=common.black
icon_bg=common.green
icon_tr="0xff"
text_fg=common.black
text_bg=common.green
text_tr="0xff"

icon_color="^c"+str(icon_fg)+"^^b"+str(icon_bg)+str(icon_tr)+"^"
text_color="^c"+str(text_fg)+"^^b"+str(text_bg)+str(text_tr)+"^"
DELAY_TIME=10

filename= os.path.basename(__file__)
name=re.sub("\..*",'',filename)


def update(loop=False,exec=True):
  while True :
    icon="  "
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

def shutdown():
  os.system("shutdown -h now")
def reboot():
  os.system("reboot")
def sleep():
  os.system("systemctl suspend ")
  # os.system("systemctl hibernate ")
def lock():
  os.system("bash "+str(common.DWM_PATH)+"i3lock/lock.sh")

def system_rofi_set() :
    #      key:display information   value:function
    choose={"⏻ Shutdown":"shutdown",
            " Reboot":"reboot",
            "⏾ Sleep":"sleep",
            " Lock":"lock",
            }
    cmd="echo $(echo -e '"
    for choose_string in choose.keys():
      cmd+=choose_string+"\\n"
    cmd=cmd[:-2]
    cmd+="' | rofi -dmenu -window-title Power)"
    print(cmd)
    result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    choose_ret=result.stdout.decode('utf-8').replace("\n","")
    print(choose_ret)
    match_function=choose[choose_ret]
    try:
      exec(str(match_function)+"()")
    except Exception:
      pass

def click(string='') :
  match string:
    case 'L':
      system_rofi_set()
      pass
    case 'M':
      pass
    case 'R':
      pass
      os.system("nitrogen&")
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
   
