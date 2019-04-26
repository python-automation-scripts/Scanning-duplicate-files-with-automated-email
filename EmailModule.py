import re;
import smtplib;
import urllib.request as urllib2
import os;
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def is_connected():
	try:
		urllib2.urlopen("http://216.58.192.142",timeout = 10);
		return True;
	except Exception as err:
		print("not connected",err);
		return False;


def sendmail(UserName , Password , To , Attachment = None ,Subject = None,Body = None):
	if(not os.path.exists(Attachment)):
		return;

	filename = Attachment;
	
	try:
		msg = MIMEMultipart();
			
		msg['From'] = UserName;
		msg['To'] = To;
		msg['Subject'] = Subject;
			
		msg.attach(MIMEText(Body,'plain'));
		attachment = open(filename, "rb");
		p = MIMEBase('application', 'octet-stream');
		p.set_payload((attachment).read());
		encoders.encode_base64(p); 
		p.add_header('Content-Disposition', "attachment; filename= %s" % filename);   
		msg.attach(p); 
			
		email_text = msg.as_string();

		server = smtplib.SMTP_SSL("smtp.gmail.com",465);
		server.ehlo();
		server.login(UserName,Password);
		server.sendmail(UserName,To,email_text);
		server.quit();
		print("Log file send successfully");

	except Exception as E:
		print(E);




