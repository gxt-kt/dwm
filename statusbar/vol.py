#!/usr/bin/env python

import os
import sys
import subprocess
import re
import time
import _thread
import common


icon_fg=common.black
icon_bg=common.blue
icon_tr="0xff"
text_fg=common.black
text_bg=common.blue
text_tr="0xff"

icon_color="^c"+str(icon_fg)+"^^b"+str(icon_bg)+str(icon_tr)+"^"
text_color="^c"+str(text_fg)+"^^b"+str(text_bg)+str(text_tr)+"^"
DELAY_TIME=1

filename= os.path.basename(__file__)
name=re.sub("\..*",'',filename)

vol_text="--"
vol_icon="ﱝ"
volumuted=""

# ref: https://github.com/TheWeirdDev/Bluetooth_Headset_Battery_Level
# Bug need Install : pip3 install git+https://github.com/pybluez/pybluez@master
def GetBluetoothBattery():
    # from bluetooth_battery import BatteryStateQuerier, BatteryQueryError, BluetoothError
    from bluetooth_battery import BatteryStateQuerier, BatteryQueryError 
    from bluetooth import  BluetoothError
    try:
        # Autodetects SPP port
        query = BatteryStateQuerier("94:37:F7:73:DB:03")
        # # or with given port
        # query = BatteryStateQuerier("11:22:33:44:55:66", "4")
        # result = int(query)  # returns integer between 0 and 100
        # result = str(query)  # returns "0%".."100%"
        icon="󰥊"
        result =int(query)
        if(result>=95) : icon="󰥈"
        elif(result>=90) : icon="󰥆"
        elif(result>=80) : icon="󰥅"
        elif(result>=70) : icon="󰥄"
        elif(result>=60) : icon="󰥃"
        elif(result>=50) : icon="󰥂"
        elif(result>=40) : icon="󰥁"
        elif(result>=30) : icon="󰥀"
        elif(result>=20) : icon="󰤿"
        elif(result>=10) : icon="󰤾"
        else : icon="󰥇"

        # return str("󰥰"+result)
        return str(icon)
        # Can raise BatteryQueryError when the device is unsupported
    except BluetoothError as e:
        # Handle device is offline
        return "󱔑"
    except BatteryQueryError as e:
        # Handle device is unsupported
        return "󱃓"


def GetBluetoothBatteryByPactl():
    icon="󰥊"
    # cmd = 'pactl list cards | grep -E "bluetooth\.battery" '
    cmd = 'pactl list cards | grep -E "bluetooth\.battery" | grep -E "[0-9]*%" | grep -Eo "[0-9]*" '
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    battery=result.stdout.decode('utf-8').replace('\n','')
    if battery!="" : 
      result =int(battery)
      if(result>=95) : icon="󰥈"
      elif(result>=90) : icon="󰥆"
      elif(result>=80) : icon="󰥅"
      elif(result>=70) : icon="󰥄"
      elif(result>=60) : icon="󰥃"
      elif(result>=50) : icon="󰥂"
      elif(result>=40) : icon="󰥁"
      elif(result>=30) : icon="󰥀"
      elif(result>=20) : icon="󰤿"
      elif(result>=10) : icon="󰤾"
      else : icon="󰥇"
    else :
      icon="󱔑"
    return icon



def get_vol_content():
  global vol_text
  global vol_icon
  global volumuted

  cmd="echo $(pactl info | grep 'Default Sink' | awk '{print $3}')"
  result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  sink=str(result.stdout.decode('utf-8').replace('\n',''))

  cmd="echo $(pactl list sinks | grep "+str(sink)+" -A 6 | sed -n '7p' | grep 'Mute: no')"
  result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  volumuted=str(result.stdout.decode('utf-8').replace('\n',''))

  cmd="echo $(pactl list sinks | grep "+str(sink)+" -A 7 | sed -n '8p' | awk '{printf int($5)}' )"
  result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  vol_text=str(result.stdout.decode('utf-8').replace('\n',''))

  if volumuted=="" :
    vol_text="--"
    vol_icon="ﱝ"
  else :
    vol=int(vol_text)
    vol_text=vol_text
    if vol==0 : 
      vol_icon="婢"
      vol_text="00"
    # elif vol<10 : vol_icon="奔" 
    # elif vol<50 : vol_icon="奔"
    else : vol_icon="墳"
  return str(vol_icon)+str(vol_text)+"%"+" "+GetBluetoothBatteryByPactl()
  # return str(vol_icon)+str(vol_text)+"%"+" "+GetBluetoothBattery()
  # return str(vol_icon)+str(vol_text)+"%"

def update(loop=False,exec=True):
  while True :
    icon=""
    icon=" "+get_vol_content()+" "
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

def notify(string='') :
  global vol_text
  global vol_icon
  global volumuted
  get_vol_content();

  cmd=""
  if volumuted=="" :
    cmd="notify-send -r 9527 '婢  mute'  "
  else :
    cmd="notify-send -r 9527 -h int:value:"+str(int(vol_text))+" -h string:hlcolor:#dddddd "+'"'+str(vol_icon)+" Volume"+'"' ;
  os.system(cmd)
  pass

def click(string='') :
  match string:
    case 'L':
      notify()
      pass
    case 'M':
      os.system("pactl set-sink-mute @DEFAULT_SINK@ toggle")
      notify()
      pass
    case 'R':
      os.system("killall pavucontrol || pavucontrol --class floatingTerminal &")
      pass
    case 'U':
      pass
      os.system("pactl set-sink-volume @DEFAULT_SINK@ +5%; notify")
      notify()
    case 'D':
      os.system("pactl set-sink-volume @DEFAULT_SINK@ -5%; notify")
      notify()
      pass
    case  _: pass


if __name__ == "__main__":
  if len(sys.argv) > 1:
    if(sys.argv[1]=="update") :
      pass
    elif(sys.argv[1]=="notify") :
      notify()
    else :
      update(exec=False)
      click(sys.argv[1])
      update(exec=False)
  else :
    update()
