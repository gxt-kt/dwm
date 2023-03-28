#!/usr/bin/env python

import os
import sys
import subprocess
import re
import time
import _thread
import common
import screeninfo


icon_fg=common.black
icon_bg=common.green
icon_tr="0xff"
text_fg=common.black
text_bg=common.green
text_tr="0xff"

icon_color="^c"+str(icon_fg)+"^^b"+str(icon_bg)+str(icon_tr)+"^"
text_color="^c"+str(text_fg)+"^^b"+str(text_bg)+str(text_tr)+"^"
DELAY_TIME=3

filename= os.path.basename(__file__)
name=re.sub("\..*",'',filename)

def update(loop=False,exec=True):
  while True :
    icon=" 󰹑"

    # TODO:
    # 暂时有个问题是执行和xrandr相关的命令会卡顿，暂时没找到解决方法
    # 如果有人知道怎么用python得到得到连接显示器数量，欢迎提issue或pr，谢谢.
    connected_ports=0

    # cmd="autorandr --fingerprint"
    # result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # port_string=result.stdout.decode('utf-8') # note that no replace('\n','')
    # connected_ports=int(port_string.count('\n'))

    # cmd="xrandr | grep -Eo '\\bconnected\\b'"
    # p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    # tmp=p.communicate()
    # connected_ports=str(tmp).count('connected')

    # cmd="xrandr | grep -Eo '\\bconnected\\b'"
    # result=subprocess.Popen(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # connected_string=result.stdout.decode('utf-8').replace('\n','')
    # connected_ports=connected_string.count('connected')

    # cmd="echo $(xrandr | grep -w 'connected' | awk '{print $1}' | wc -l)"
    # result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # connected_ports=result.stdout.decode('utf-8').replace('\n','')

    connected_monitors=0
    screen_info=str(screeninfo.get_monitors())
    connected_monitors=screen_info.count('Monitor')
    # cmd="echo $(xrandr --listmonitors | sed 1d | awk '{print $4}' | wc -l)"
    # result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # connected_monitors=result.stdout.decode('utf-8').replace('\n','')

    # TODO:
    # text=" "+str(connected_monitors)+"/"+str(connected_ports)+" "
    text=" "+str(connected_monitors)+" "
    txt="^s"+str(name)+"^"+str(icon_color)+str(icon)+str(text_color)+str(text)
    common.write_to_file(txt+"\n",str(name))
    if loop == False : 
      if exec==True :
        os.system("xsetroot -name '"+str(txt)+"'")
      break
    time.sleep(DELAY_TIME)

def update_thread():
  _thread.start_new_thread(update,(False,False))

def get_all_screen_status() :
    eDP=""
    HDMI=""
    DP=""

    cmd='xrandr | rg "\\beDP.*? .*? " -o'
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    eDP=result.stdout.decode('utf-8')

    cmd='xrandr | rg "\\bHDMI.*? .*? " -o'
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    HDMI=result.stdout.decode('utf-8')

    cmd='xrandr | rg "\\bDP.*? .*? " -o'
    result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    DP=result.stdout.decode('utf-8')

    return (eDP,HDMI,DP)

def Set_Auto():
  os.system("autorandr --change")
  pass
def Set_4k_L____2k_P_R_2_0():
  os.system("\
  xrandr --output DP-0 --off \
  --output DP-1 --off \
  --output DP-2 --off \
  --output DP-3 --off \
  --output HDMI-0 --primary --mode 2560x1440 --rate 120 --scale 2.0x2.0 --pos 3840x0 --rotate normal \
  --output eDP-1-0 --mode 3840x2160 --rate 60 --dpi 192 --pos 0x0 --rotate normal \
  ")
  pass
def Set_4k_L____2k_P_R_1_75():
  os.system("\
  xrandr --output DP-0 --off \
  --output DP-1 --off \
  --output DP-2 --off \
  --output DP-3 --off \
  --output HDMI-0 --primary --mode 2560x1440 --rate 120 --scale 1.75x1.75 --pos 3840x0 --rotate normal \
  --output eDP-1-0 --mode 3840x2160 --rate 60 --dpi 192 --pos 0x0 --rotate normal \
  ")
  pass
def Set_4k_L____2k_P_R_1_5():
  os.system("\
  xrandr --output DP-0 --off \
  --output DP-1 --off \
  --output DP-2 --off \
  --output DP-3 --off \
  --output HDMI-0 --primary --mode 2560x1440 --rate 120 --scale 1.5x1.5 --pos 3840x0 --rotate normal \
  --output eDP-1-0 --mode 3840x2160 --rate 60 --dpi 192 --pos 0x0 --rotate normal \
  ")
  pass
def Set_4k_S___1k_S_2_0():
  os.system("\
  xrandr --output DP-0 --off \
  --output DP-1 --off \
  --output DP-2 --off \
  --output DP-3 --off \
  --output HDMI-0 --primary --mode 1920x1080 --rate 60 --scale 2x2 --pos 0x0 --rotate normal \
  --output eDP-1-0 --mode 3840x2160 --rate 60 --dpi 192 --pos 0x0 --rotate normal \
  ")
  pass
def Set_4k_Single():
  os.system("\
  xrandr  --output DP-0 --off \
  --output DP-1 --off \
  --output DP-2 --off \
  --output DP-3 --off \
  --output HDMI-0 --off \
  --output eDP-1-0 --mode 3840x2160   --rate 60 --dpi 192 \
  ")
  pass

def screen_rofi_set() :
    #      key:display information   value:function
    choose={
            "Auto":"Set_Auto",
            "4k(L)+2k(P)(R)(2.0)":"Set_4k_L____2k_P_R_2_0",
            "4k(L)+2k(P)(R)(1.75)":"Set_4k_L____2k_P_R_1_75",
            "4k(L)+2k(P)(R)(1.5)":"Set_4k_L____2k_P_R_1_5",
            "4k(S)+1k(S)(2)":"Set_4k_S___1k_S_2_0",
            "4k_Single":"Set_4k_Single",
            }
    cmd="echo $(echo -e '"
    for choose_string in choose.keys():
      cmd+=choose_string+"\\n"
    cmd=cmd[:-2]
    cmd+="' | rofi -dmenu -window-title Screen)"
    print(cmd)
    result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    choose_ret=result.stdout.decode('utf-8').replace("\n","")
    print(choose_ret)
    match_function=choose[choose_ret]
    try:
      exec(str(match_function)+"()")
    except Exception:
      pass

def notify(string='') :
    send_string=""
    for string_ in get_all_screen_status():
      send_string+=string_
    os.system("notify-send "+" '󰹑 Screen Info' "+"'"+send_string+"' -r 1212")
    pass

def click(string='') :
  match string:
    case 'L':
      screen_rofi_set()
    case 'M':
      pass
    case 'R':
      notify()
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
