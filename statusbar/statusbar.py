#!/usr/bin/env python

import os
import sys
import fcntl
import subprocess
import _thread
import time
import re
import common
import threading
# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

packages_list=common.PACKAGES_LISTS

# import packages
for name in packages_list.keys():
  exec('import ' + str(name))


def ExecOtherFile():
  cmd='python3 '+ common.PACKAGES_PATH + str(sys.argv[1]) + '.py '
  for string in sys.argv[2:]:
    cmd=cmd+string+' '
  result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)


def MainRefresh():
  tmp=""
  lines=""

  common.threadLock.acquire()
  if (os.path.exists(common.TEMP_FILE)==False):
    os.system("touch "+common.TEMP_FILE)
  with open(common.TEMP_FILE, 'r+') as f:
    lines=f.readlines()
  common.threadLock.release()

  packages=packages_list.keys()
  for name in packages:
    match_string="^\^s"+str(name)
    for line in lines :
      flag=re.match(str(match_string),line)
      if flag!=None :
        exec(str(name)+"_txt"+"=line.encode('utf-8').decode('utf-8').replace('\\n','')")
        tmp+=locals()[str(name)+"_txt"]
        break
  os.system("xsetroot -name '"+str(tmp)+"'")


def Run() :
  # add new thread
  # for name in packages_list:
  #   exec("_thread.start_new_thread("+str(name)+".update,(True,))")

  # scheduler = BlockingScheduler()
  scheduler = BackgroundScheduler()
  for key,value in packages_list.items():
    cmd="scheduler.add_job("+str(key)+".update_thread, 'interval', seconds="+str(int(value))+", id='"+str(key)+"')"
    exec(cmd)
  # scheduler.add_job(MainRefresh, 'interval', seconds=1, id='MainRefresh')
  scheduler.start()

  while True :
    # print("debug point 1")
    MainRefresh()
    time.sleep(0.5)



if __name__ == "__main__":
  if len(sys.argv) > 1:
    if(sys.argv[1]=="cron") :
      Run()
      pass
    elif(sys.argv[1]=="update") :
      pass
    else :
      # for string in sys.argv :
      #   print(string)
      #   # cmd="echo '" +str(string) + "'" + ">> python_debug"
      #   cmd="echo '" +str(string) + "'"
      #   # cmd = "echo '123' >> python_debug"
      #   result = subprocess.run(cmd, shell=True, timeout=3, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

      ExecOtherFile()
  # Run()
   
