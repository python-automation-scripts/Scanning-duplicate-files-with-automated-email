import os;
import time;
import schedule;
import datetime;
from sys import *;
import EmailModule;
import ChecksumFunctionalityModule as module;

FileScanCount = 0;
FileDeleteCount = 0;
OutputFile = "";
 
def CreateOutput(DirName,LogDir = "Log"):
	
	LogDir = os.path.join(DirName,LogDir);
	
	if(not os.path.exists(LogDir)):
		os.mkdir(LogDir);
	
	seperator = "-" * 160;
	FileName =  os.path.join(LogDir,str("Marvellous %s.log"%(time.ctime())).replace(':','_').replace(' ','_') );
	
	List,FileScanCnt,FileDeletedCnt =  module.DeleteDuplicateFiles(DirName);

	global FileScanCount,FileDeleteCount,OutputFile
	FileScanCount = FileScanCnt;
	FileDeleteCount = FileDeletedCnt;
	OutputFile = FileName;

	data = "";
	for element in List:
		data += str(element) + "\n";

	fd = open(FileName,"x");
	fd.write(seperator + "\n");
	fd.write("Marvellous Duplicate Deleted Files Logger : "+time.ctime() + "\n");
	fd.write(seperator + "\n\n");
	fd.write(data);
	fd.close();

	return FileName;


def CreateMail(To,FileName,ScanTime,FileScanCnt,FileDeletedCnt):
	username = "harshalghule20@gmail.com";
	password = "**********************";
	to = To;
	
	subject  = """
	Marvellous Duplicate File Log Generated at : %s
	""" %(time.ctime());

	body =  """
	Hello %s 
	Welcome to Automation.
	Please find attached documents which contains log of duplicate files which are deleted.
	Scanning process started at : %s
	Total number files scanned : %s 
	Total number of duplicate files found : %s

	This is autogenerated mail.
	Please do not reply.

	Thanks & Regards,
	Harshal Narayan Ghule
	""" %(To[0:To.rfind('@')],ScanTime,FileScanCnt,FileDeletedCnt);

	if EmailModule.is_connected():
		EmailModule.sendmail(username,password,To,FileName,subject,body);


def main():
	
	if (argv[1] == "-h") or (argv[1] == "-H"):
		print("\n\n\t\t........................This is FileSystem Automation........................\n\n");
		print("\n " + argv[0]+ " -h For Help");
		print("\n " + argv[0]+ " -u For Usage");		
		exit();

	if (argv[1] == "-u") or (argv[1] == "-U"):
		print("\n <Usage> " + argv[0]+ " Directory_Name(path) Time_Interval(minutes) Email_ID ");
		exit();

	if  len(argv) != 4:
		print("Invalid number arguments");
		exit();

	try:
		DirName = argv[1];
		Time_Interval = int(argv[2]);
		To_Email = argv[3];
		ScanTime = time.ctime();
		
		schedule.every(Time_Interval).minutes.do(lambda : CreateOutput(DirName));
		schedule.every().day.at("00:05").do( lambda : CreateMail(To_Email,OutputFile,ScanTime,FileScanCount,FileDeleteCount));
		
		while True:
			schedule.run_pending();
			time.sleep(1);

	except Exception as E:
		fd = open("Error_Log.log",'a');
		logmsg = "\n\n Error :  %s \n Log Time : %s \n\n"%(E,time.ctime());
		fd.write(logmsg);
		fd.close();

if(__name__ == "__main__"):
	main();