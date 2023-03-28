#!/usr/bin/env python

import os
import sys
import subprocess
import re
import time
from typing import Tuple
import _thread
import common


icon_fg=common.blue
icon_bg=common.black
icon_tr="0xff"
text_fg=common.blue
text_bg=common.black
text_tr="0xff"

icon_color="^c"+str(icon_fg)+"^^b"+str(icon_bg)+str(icon_tr)+"^"
text_color="^c"+str(text_fg)+"^^b"+str(text_bg)+str(text_tr)+"^"

DELAY_TIME=1

filename= os.path.basename(__file__)
name=re.sub("\..*",'',filename)


def get_speed(val:int)->str:
  ret="0"
  if(val<1024) :
    ret="{:^8}".format(str(val)+"B")
  elif val<1048576 :
    ret="{:^8}".format("{:.1f}".format(val/1024)+"KB")
  else :
    ret="{:^8}".format("{:.1f}".format(val/1048576)+"MB")
  return ret

def getnet()->Tuple[str,str]:
    rx_bytes_cur=0
    cmd="cat /sys/class/net/[ew]*/statistics/rx_bytes"
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    rx_bytes_string=result.stdout.decode('utf-8')
    for rx in rx_bytes_string.splitlines():
      rx_bytes_cur+=int(rx)
    TX_POSITON="~/.cache/rx_bytes"
    if (os.path.exists(TX_POSITON)==False):
      os.system("touch "+TX_POSITON)
    cmd="cat "+TX_POSITON
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    rx_bytes_pre=result.stdout.decode('utf-8').replace("\n","")
    rx_bytes=0
    if rx_bytes_pre!="":
        rx_bytes=abs(int(rx_bytes_cur)-int(rx_bytes_pre))
    # write new rx_bytes_cur
    cmd="echo "+str(rx_bytes_cur)+" > "+TX_POSITON
    os.system(cmd)

    tx_bytes_cur=0
    cmd="cat /sys/class/net/[ew]*/statistics/tx_bytes"
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    tx_bytes_string=result.stdout.decode('utf-8')
    for tx in tx_bytes_string.splitlines():
      tx_bytes_cur+=int(tx)
    TX_POSITON="~/.cache/tx_bytes"
    if (os.path.exists(TX_POSITON)==False):
      os.system("touch "+TX_POSITON)
    cmd="cat "+TX_POSITON
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    tx_bytes_pre=result.stdout.decode('utf-8').replace("\n","")
    tx_bytes=0
    if tx_bytes_pre!="":
        tx_bytes=abs(int(tx_bytes_cur)-int(tx_bytes_pre))
    # write new tx_bytes_cur
    cmd="echo "+str(tx_bytes_cur)+" > "+TX_POSITON
    os.system(cmd)

    send_string=str(get_speed(tx_bytes))
    recv_string=str(get_speed(rx_bytes))
    # print(send_string)
    # print(recv_string)
    return (" "+send_string,""+recv_string)

def update(loop=False,exec=True):
  while True :
    icon=""
    text=""
    for string in getnet():
      text+=string
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
   
