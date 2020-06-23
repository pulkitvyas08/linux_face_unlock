#!/bin/bash
function facerec(){
if [ "$1" = "new" ]; then
    sudo python3 /lib/Auth/RecFace/add_new.py
elif [ "$1" = "enable" ]; then
    sudo pam-auth-update --package
elif [ "$1" = "disable" ]; then
    sudo apt-get --reinstall install libpam-runtime libpam-modules
fi
}
