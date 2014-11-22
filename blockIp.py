import subprocess
import os
import datetime
import urllib2
import smtplib

# Path to access logs 
path = "<PATH>"

# List of terms to search for
terms = "php\|my\|manager\|MY\|My\|PHP\|admin\|Admin\|Manager"

# Set your to and from address for report
frm =   "ADDRESS"  
to  =   "ADDRESS"

# Set password for gmail
uname = 'USERNAME'
pword = 'PASSwORD'

# getDate returns year, month and date and adds 0 to single digit months/days 
def getDate():

	d = datetime.date.today()
	year = str(d.year)
        month = str(d.month)
	day = str(d.day)
	
	if len(month) == 1:
                month = "0" + month

	if len(day) == 1:
		day = "0" + day

	return (year, month, day)

# getIps parses ips out of accesslogs for current day
def getIps():

	date =  getDate()
	cmd = "cat " + path + "localhost_access_log." + date[0] + "-"+ date[1] + "-" + date[2] + ".txt | grep '" + terms + "'"
	output = subprocess.check_output(cmd, shell=True)

	# NOTE: Regex below will find all numbers with the format x.x.x.x so if your uri contains soemthing like 
	#       /phpMyAdmin-3.0.0.0-all-languages/scripts/setup.php HTTP/1.1 it will try to block 3.0.0.0 
	#ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', output)
 
	ip = output.splitlines()
	ip = [i.split(" ", 1)[0] for i in ip]
	ip = list(set(ip))
	
	return ip

# blockIp blocks the ips
def blockIp(ip):

	for i in ip:
		cmd = "ufw deny from " + i
	#	output = subprocess.check_output(cmd, shell=True)
		print cmd

# sendReport sends the list of ip's that have been blocked
def sendReport(ip): 

	from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "I just blocked these ip addresses :)"
        msg['From'] = frm
        msg['To'] = to

        body = "These are blocked: "

	for i in ip:
		body = body + i + ", "

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(uname,pword)
        server.sendmail(frm, to, msg.as_string())
        server.quit()

# main fuction 
def main():

	ip = getIps()
	blockIp(ip)
	sendReport(ip)

# =======================
if __name__ == "__main__":
        main();
