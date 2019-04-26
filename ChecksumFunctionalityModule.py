
import os;
import hashlib;


def hashfile(path,blocksize = 1024):
	fd = open(path,"rb");
	hasher = hashlib.md5();
	buf = fd.read(blocksize);

	while len(buf) > 0:
		hasher.update(buf);
		buf = fd.read(blocksize);

	fd.close();

	return hasher.hexdigest();


def GetChecksum(DirName):
	if(not os.path.isabs(DirName)):
		DirName = os.path.abspath(DirName);

	if(os.path.isdir(DirName)):
		
		duplicate = {};
		filecnt = 0;

		for folder, subfolder, files in os.walk(DirName):
			for file in files:
				DirName = os.path.join(folder,file);
				print(DirName);
				if os.path.isfile(DirName):
					file_hash = hashfile(DirName);
					filecnt += 1;

					if(file_hash in duplicate):
						duplicate[file_hash].append(DirName);
					else:
						duplicate[file_hash] = [DirName];

	return duplicate,filecnt;

def FileDuplicate(DirName):
	dictionary,filecnt = GetChecksum(DirName);
	return GetDuplicate(dictionary),filecnt;


def GetDuplicate(dictionary):	
	results = list(filter(lambda x: len(x) > 1,dictionary.values()));	
	List = list();
	
	fileCnt = 0;
	for result in results:
		for subresult in result:
			fileCnt +=1;
			if(fileCnt >= 2):
				List.append(subresult);
		fileCnt = 0;
	return List;


def DeleteDuplicateFiles(DirName):
	List,filecnt = FileDuplicate(DirName);

	for file in List:
		os.remove(file);
	return List,filecnt,len(List);  #list of duplicate files , total file scanned , duplicate file count 



def ChkFileExists(filename,cnt = 0):	#checks if file exists and return the new file name for eg Demo_Copy.txt, Demo_Copy_1.txt	

	if(not os.path.exists(filename)):
		return filename;
	
	elif("_Copy" not in filename):

		a = filename[0:filename.rfind('.')];
		b = filename[filename.rfind('.'):];
		newfilename = a + "_Copy" +  b;
		filename = newfilename;
	
	else:			
		a = filename[0:filename.rfind('_Copy')];
		b = filename[filename.rfind('.'):];
		newfilename = a + "_Copy_" + str(cnt) + b;
		filename = newfilename;		
	cnt += 1;
	return ChkFileExists(filename,cnt);	