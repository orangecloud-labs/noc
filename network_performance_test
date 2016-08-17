#!/bin/bash 

function check_installs {
	distro=`uname -r`
	echo "Your distro: $distro"
	CHECKLIST='/tmp/_checklist'
	if [ -f $CHECKLIST ];
	then
		echo "" > $CHECKLIST
	else
		touch $CHECKLIST
	fi

	if ! [ "$(command -v traceroute)" ]; then
		echo 'traceroute is not installed' >&2
		echo 'traceroute' > /tmp/_checklist
	fi

	if ! [ "$(command -v curl)" ]; then
		echo 'curl is not installed' >&2
		echo 'curl' >> /tmp/_checklist
	fi

	if ! [ "$(command -v mtr)" ]; then
		echo 'mtr is not installed' >&2
		echo 'mtr' >> /tmp/_checklist
	fi

	if ! [ "$(command -v wget)" ]; then
		echo 'wget is not installed' >&2
		echo 'wget' >> /tmp/_checklist
	fi

	if ! [ "$(command -v gedit)" ]; then
		echo 'gedit is not installed - it will be used to display results' >&2
		echo 'gedit' >> /tmp/_checklist
	fi

	if ! [ "$(command -v dig)" ]; then
		echo 'dig of dnsutils is not installed. dnsutils package is required' >&2
		echo 'dnsutils' >> /tmp/_checklist
	fi

	CHECKLIST_ITEMS_COUNT=`cat $CHECKLIST | wc -w`

	if (( $CHECKLIST_ITEMS_COUNT > 0 )); then
		echo "Do you want me to install missing package(s) for you ? (y/n)"
		read OPTION
		if [ $OPTION = "y" ]; then
			echo -e "Choose (number) your installer: \n1. pacman\n2. apt-get\n3. yum\n4. zypper"
			read INSTALLER
			if (( $INSTALLER == 1 )); then
				while read PACKAGE
				do
					sudo pacman -S --noconfirm $PACKAGE
				done < "$CHECKLIST"
			elif (( $INSTALLER == 2 )); then
				while read PACKAGE
				do
					sudo apt-get -q -y install $PACKAGE
				done < "$CHECKLIST"
			elif (( $INSTALLER == 3 )); then
				while read PACKAGE
				do
					sudo yum -y install $PACKAGE
				done < "$CHECKLIST"
			elif (( $INSTALLER == 4 )); then
				while read PACKAGE
				do
					sudo zypper --non-interactive install $PACKAGE
				done < "$CHECKLIST"
			else
				exit
			fi
		fi
		initiate
	else
		initiate
	fi

	echo $1
}

function initiate {
	start
}

function start {
	if (( uname == "Linux" )); then
		echo "CDN Domain: (WITHOUT http!)"
		read DOMAIN

		FIND_HTTP='http://'
                FIND_HTTPS='https://'
                if [[ $DOMAIN == *"$FIND_HTTP"* || $DOMAIN == *"$FIND_HTTPS"* ]]; then
                        DOMAIN=`echo $DOMAIN | sed 's/https\?:\/\///'`
                fi
		
		echo "File: (RELATIVE PATH LIKE: /path/to/file.ext OR LEAVE BLANK)"
		read FILE

		if [[ ${FILE:0:1} != "/" ]]; then
			FILE="/$FILE"
		fi

		echo "This may take some time. After I am done you will see new window with results, please, send it over to support@maxcdn.com\n"

		trace $DOMAIN
		curl $DOMAIN$FILE
		pub_ip
		ping $DOMAIN
		mtr $DOMAIN
		wget $DOMAIN$FILE
		dns $DOMAIN
		view
	fi
}

function trace {
	echo -e "\n========================================\nTRACEROUTE FROM CIENT MACHINE\n========================================\n" > /tmp/idabic_trace.log
	sudo traceroute -T $1 >> /tmp/idabic_trace.log
}

function curl {
	echo -e "\n========================================\nHTTP CURL FROM CLIENT MACHINE\n========================================\n" > /tmp/idabic_curl.log
	bash -c "curl -I http://$1 >> /tmp/idabic_curl.log"
	echo -e "\n========================================\nHTTPS CURL FROM CLIENT MACHINE\n========================================\n" > /tmp/idabic_curl_https.log
	bash -c "curl -I https://$1 >> /tmp/idabic_curl_https.log"
}

function pub_ip {
	echo -e "\n========================================\nCLIENT PUBLIC IP\n========================================\n" > /tmp/idabic_pub_ip.log
	bash -c "wget -qO- http://ipecho.net/plain >> /tmp/idabic_pub_ip.log"
}

function ping {
	echo -e "\n========================================\nPING FROM CLIENT MACHINE\n========================================\n" > /tmp/idabic_ping.log
	bash -c "ping -c 10 $1 >> /tmp/idabic_ping.log"
}

function mtr {
	echo -e "\n========================================\nMTR FROM CLIENT MACHINE\n========================================\n" > /tmp/idabic_mtr.log
	bash -c "mtr -tcp -c 50 -s 1500 --report $1 >> /tmp/idabic_mtr.log"
}

function wget {
	echo -e "\n========================================\nHTTP WGET FROM CLIENT MACHINE\n========================================\n" > /tmp/idabic_wget.log
	bash -c "wget -O /dev/null -d -a /tmp/idabic_wget.log http://$1"
	echo -e "\n========================================\nHTTPS WGET FROM CLIENT MACHINE\n========================================\n" > /tmp/idabic_wget_https.log
	bash -c "wget -O /dev/null -d -a /tmp/idabic_wget_https.log https://$1"
}

function dns {
	echo -e "\n========================================\nDNS\n========================================\n" > /tmp/idabic_dns.log
	bash -c "dig $1 >> /tmp/idabic_dns.log"
	echo -e "\n========================================\nDNS WITH PUBLIC RESOLVER\n========================================\n" > /tmp/idabic_dns_public.log
	bash -c "dig $1 @8.8.8.8 >> /tmp/idabic_dns_public.log"
}

function view {
	END_TIME=`date`
	cat /tmp/idabic_* > /tmp/idabic_results ; echo -e "\n========================================\nSTART TIME\n========================================\n$START_TIME" >> /tmp/idabic_results ; echo -e "\n========================================\nEND TIME\n========================================\n$END_TIME" >> /tmp/idabic_results
	gedit /tmp/idabic_results
}
START_TIME=`date`
check_installs
