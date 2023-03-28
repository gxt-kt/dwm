#!/usr/bin/env python

import os
import sys
import subprocess
import re
import time
import common
import _thread


icon_fg=common.green
icon_bg=common.black
icon_tr="0xff"
text_fg=common.green
text_bg=common.black
text_tr="0xff"

icon_color="^c"+str(icon_fg)+"^^b"+str(icon_bg)+str(icon_tr)+"^"
text_color="^c"+str(text_fg)+"^^b"+str(text_bg)+str(text_tr)+"^"
DELAY_TIME=3

filename= os.path.basename(__file__)
name=re.sub("\..*",'',filename)

def get_battery_status():
  charge_icon=""

  cmd="echo $(acpi | sed 's/^Battery 0: //g' | awk -F ',' '{print $1}') "
  result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  charge_sta=result.stdout.decode('utf-8').replace('\n','')


  cmd="echo $(acpi -b | sed 2d | awk '{print $4}' | grep -Eo '[0-9]+')"
  result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  battery_text=result.stdout.decode('utf-8').replace('\n','')

  charge_icon=""
  bat_icon=""
  if (str(charge_sta)=="Discharging") :
    bat=int(battery_text)
    if(bat>=95): bat_icon="";
    elif(bat>=90): bat_icon="";
    elif(bat>=80): bat_icon="";
    elif(bat>=70): bat_icon="";
    elif(bat>=60): bat_icon="";
    elif(bat>=50): bat_icon="";
    elif(bat>=40): bat_icon="";
    elif(bat>=30): bat_icon="";
    elif(bat>=20): bat_icon="";
    elif(bat>=10): bat_icon="";
    else : bat_icon="󱃍"
  elif (str(charge_sta)=="Charging") :
    bat=int(battery_text)
    if(bat>=95): bat_icon="󰂅";
    elif(bat>=90): bat_icon="󰂋";
    elif(bat>=80): bat_icon="󰂊";
    elif(bat>=70): bat_icon="󰢞";
    elif(bat>=60): bat_icon="󰂉";
    elif(bat>=50): bat_icon="󰢝";
    elif(bat>=40): bat_icon="󰂈";
    elif(bat>=30): bat_icon="󰂇";
    elif(bat>=20): bat_icon="󰂆";
    elif(bat>=10): bat_icon="󰢜";
    else : bat_icon="󰢟"
  elif (str(charge_sta)=="Full") :
    bat_icon="󰂅";
  else :
    bat_icon="󰂑";
  return (bat_icon,battery_text)

def update(loop=False,exec=True):
  while True :
    icon=""
    text=""
    icon,text=get_battery_status()
    icon=" "+icon
    text=""+text
    text+=" "
    txt="^s"+str(name)+"^"+str(icon_color)+str(icon)+str(text_color)+str(text)
    common.write_to_file(txt+"\n",str(name))
    if loop == False : 
      if exec==True :
        os.system("xsetroot -name '"+str(txt)+"'")
      break
    time.sleep(DELAY_TIME)

def update_thread():
  _thread.start_new_thread(update,(False,False))

def notify(str='') :
  pass
  # cmd='notify-send "  CPU tops"  "$(ps axch -o cmd:15,%cpu --sort=-%cpu | head  | '+"sed 's/$/&%/g')"+'"'+" -r 1014"
  # os.system(cmd)

def click(str='') :
  match str:
    case 'L':
      os.system("gnome-power-statistics&")
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


if __name__ == "__main__":
  if len(sys.argv) > 1:
    if(sys.argv[1]=="update") :
      pass
    else :
      click(sys.argv[1])
      update(exec=False)
  else :
    update()
