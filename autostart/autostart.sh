#! /bin/sh

# If you find fcitx5 icon is located at the most left of the straybar, please increase the delay value
sleep 1 # need to wait dwm start complete and fcitx5 start complete

# Notice that cron need exec before other program
cron() {
    let i=1
    while true; do
        [ $((i % 3)) -eq 0 ] && ~/my_desktop/dwm/autostart/autoscreen.sh # check screen and autoset
        sleep 1; let i+=1
    done
}
cron&


cfw & # clash for windows
crow & # translate
blueman-manager & # bluetooth manager
copyq & # copy software

picom --experimental-backends& 


pkill -f statusbar.py
python3 ~/my_desktop/dwm/statusbar/statusbar.py cron &>/dev/null


libinput-gestures-setup start # touchpad open gesture
xinput --set-prop 15 'libinput Accel Speed' 0.5 # set touchpad sensitivity

xhost + # add support for docker gui app
