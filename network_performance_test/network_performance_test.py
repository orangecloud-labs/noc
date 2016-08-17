import os
import sys
import platform
import os.path
import platform

if platform.system() == "Windows":
    import msvcrt

def check_installs():
	print("Your distro: " + platform.linux_distribution()[0])
	if os.path.isfile('/tmp/_checklist') == True:
		f = open('/tmp/_checklist', 'r+')
		f.truncate()
	if os.path.isfile('/tmp/_checklist') != True:
		os.system("bash -c \"touch /tmp/_checklist\"")
	os.system("bash -c \"command -v traceroute >/dev/null 2>&1 || { echo 'traceroute is not installed' >&2 && echo 'traceroute' > /tmp/_checklist; }\"")
	os.system("bash -c \"command -v curl >/dev/null 2>&1 || { echo 'curl is not installed' >&2 && echo 'curl' >> /tmp/_checklist; }\"")
	os.system("bash -c \"command -v mtr >/dev/null 2>&1 || { echo 'mtr is not installed' >&2 && echo 'mtr' >> /tmp/_checklist; }\"")
	os.system("bash -c \"command -v wget >/dev/null 2>&1 || { echo 'wget is not installed' >&2 && echo 'wget' >> /tmp/_checklist; }\"")
	os.system("bash -c \"command -v dig >/dev/null 2>&1 || { echo 'dig of dnsutils is not installed. dnsutils package is required.' >&2 && echo 'dnsutils' >> /tmp/_checklist; }\"")
	os.system("bash -c \"command -v gedit >/dev/null 2>&1 || { echo 'gedit is not installed' >&2 && echo 'gedit' >> /tmp/_checklist; }\"")

	checklist_items = []
	checklist_items_count = 0
	with open('/tmp/_checklist') as f2:
		checklist_items = f2.readlines()
		checklist_items_count = len(checklist_items)
	if checklist_items_count > 0:
		print("Do you want me to install missing package(s) for you ? (y/n)\n")
		q = sys.stdin.readline()
		if q.rstrip('\n') == "y":
			installer = ''
			print("Choose installer you are using:\n1. pacman\n2. apt-get\n3. yum\n4. zypper")
			d = sys.stdin.readline()
			if d.rstrip('/n') == "1":
				print("You have chosen option 1: sudo pacman -S <package>\n")
				installer = "sudo pacman -S"
			if d.rstrip('\n') == "2":
				print("You have chosen option 2: sudo apt-get install <package>\n")
				installer = "sudo apt-get install"
			if d.rstrip('\n') == "3":
				print("You have chosen option 3: sudo yum install <package>\n")
				installer = "sudo yum install"
			if d.rstrip('\n') == "4":
				print("You have chosen option 4: sudo zypper --non-interactive install <package>\n")
				installer == "sudo zypper --non-interactive install"
			install_packages(installer)
		if q.rstrip('\n') == "n":
			exit(1)
	if checklist_items_count == 0:
		initiate()

def install_packages(installer):
	print("Installing...\n")
	content = []
	with open('/tmp/_checklist') as f:
		content = f.readlines()
	print(content)
	for c in content:
		print("Installing " + c.rstrip('\n') + "...\n")
		os.system("bash -c \"" + installer + " " + c.rstrip('\n') + "\"")
	initiate()

def initiate():
	getch()

def trace(domain):
	os.system("bash -c \"echo '-----------------------------------------------\nTRACEROUTE FROM CLIENT MACHINE\n' > /tmp/idabic_trace.log\"")
	os.system("bash -c \"traceroute " + domain + " >> /tmp/idabic_trace.log\"")

def curl(t, f):
	os.system("bash -c \"echo '-----------------------------------------------\nHTTP CURL FROM CLIENT MACHINE\n' > /tmp/idabic_curl.log\"")
	os.system("bash -c \"curl -I \"http://" + t + f + " >> /tmp/idabic_curl.log")
	os.system("bash -c \"echo '-----------------------------------------------\nHTTPS CURL FROM CLIENT MACHINE\n' > /tmp/idabic_curl_https.log\"")
	os.system("bash -c \"curl -I \"https://" + t + f + " >> /tmp/idabic_curl_https.log")

def pub_ip():
	os.system("bash -c \"echo '-----------------------------------------------\nCLIENT IP - PUBLIC\n' > /tmp/idabic_pub_ip.log\"")
	os.system("bash -c \"curl -s checkip.dyndns.org | sed -e 's/.*Current IP Address: //' -e 's/<.*$//'\" >> /tmp/idabic_pub_ip.log")

def ping(domain):
	os.system("bash -c \"echo '-----------------------------------------------\nPING FROM CLIENT MACHINE\n' > /tmp/idabic_ping.log\"")
	os.system("bash -c \"ping -c 10 \"" + domain + " >> /tmp/idabic_ping.log")

def mtr(domain):
	os.system("bash -c \"echo '-----------------------------------------------\nMTR FROM CLIENT MACHINE\n' > /tmp/idabic_mtr.log\"")
	os.system("bash -c \"mtr -tcp -c 50 -s 1500 --report \"" + domain + " >> /tmp/idabic_mtr.log")

def wget(t, f):
	os.system("bash -c \"echo '-----------------------------------------------\nHTTP WGET FROM CLIENT MACHINE (DEBUG)\n' > /tmp/idabic_wget.log\"")
	os.system("bash -c \"wget -O /dev/null -d -a /tmp/idabic_wget.log \"http://" + t + f)
	os.system("bash -c \"echo '-----------------------------------------------\nHTTPS WGET FROM CLIENT MACHINE (DEBUG)\n' > /tmp/idabic_wget_https.log\"")
	os.system("bash -c \"wget -O /dev/null -d -a /tmp/idabic_wget_https.log \"https://" + t + f)

def dns(domain):
	os.system("bash -c \"echo -e '-----------------------------------------------\nDNS\n' > /tmp/idabic_dns.log\"")
	os.system("bash -c \"dig \"" + domain + " >> /tmp/idabic_dns.log")
	os.system("bash -c \"echo -e '-----------------------------------------------\nDNS WITH PUBLIC RESOLVER\n' > /tmp/idabic_dns_public.log\"")
	os.system("bash -c \"dig " + domain + " @8.8.8.8 \" >> /tmp/idabic_dns_public.log")

def view():
	os.system("bash -c \"cat /tmp/idabic_*.log > /tmp/results\"")
	os.system("bash -c \"gedit /tmp/results\"")

def getch():
    if platform.system() == "Linux":
        print("CDN Domain: \n")
        t = sys.stdin.readline()

        for prefix in ('http://', 'https://'):
            if t.startswith(prefix):
                t = t[len(prefix):]
                break

        print("File: \n")
        f = sys.stdin.readline()

        if f[:1] != "/":
            f = "/" + f

        print("This may take some time. After I am done you will see new window with results, please, send it over to support@maxcdn.com\n")
        trace(t.rstrip('\n'))
        curl(t.rstrip('\n'), f.rstrip('\n'))
        pub_ip()
        ping(t.rstrip('\n'))
        mtr(t.rstrip('\n'))
        wget(t.rstrip('\n'), f.rstrip('\n'))
        dns(t.rstrip('\n'))
        view()
    else:
        msvcrt.getch()

check_installs()
print("Voila!")
