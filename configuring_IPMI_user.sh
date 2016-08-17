#!/bin/bash
#changes IPMI pw and user

ipmipasswd= "SET_PASSWORD_HERE"

if [ ! -f /usr/bin/ipmitool ]; then
	sudo yum -y install ipmitool 
fi 

sudo    /sbin/modprobe ipmi_devintf
sudo 	/sbin/modprobe ipmi_msghandler
sudo 	/sbin/modprobe ipmi_si
sudo 	/bin/sleep 5
sudo 	/usr/bin/ipmitool user set password 2 ${ipmipasswd}
sudo 	/usr/bin/ipmitool user disable 2
sudo 	/usr/bin/ipmitool channel setaccess 1 3 callin=on ipmi=on link=on privilege=4
sudo 	/usr/bin/ipmitool user set name 3 "SET_USER_HERE"
sudo 	/usr/bin/ipmitool user set password 3 ${ipmipasswd}
sudo 	/usr/bin/ipmitool user priv 3 4 1
sudo 	/usr/bin/ipmitool user enable 3
sudo 	/usr/bin/ipmitool user list 1
 	    echo "password changed"