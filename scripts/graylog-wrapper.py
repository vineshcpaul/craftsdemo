#!/usr/bin/env python3

import argparse,re
import json
import subprocess 
from pprint import pprint



#Variables
fileBeatBin = "/usr/bin/filebeat"
fileBeatConf = "/etc/graylog/collector-sidecar/generated/filebeat.yml"
grayServer = "http://172.22.107.69"
grayPort = 9000

def parseArgs():
        parser = argparse.ArgumentParser()
        parser.add_argument("-l" , action='store', dest='logFile')
        parser.add_argument("-k" , action='store', dest='keyWord',default='last 5 minutes')
        return parser.parse_args()

def runCommand(command):
	print ("Command to run : %s" % command)
	p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	for line in p.communicate():
		if not line is None:
			print ("%s" % line)
	rc = p.returncode
	if rc > 0:
		print ("Command failed : %s" % command)
	elif rc == 0:
		print ("Command success: %s" % command)

def checkRestCall(keyword,jsonFile):
	field = "file"
	keyword = "last%20300%20minutes"
	curlURL = "curl -s -u admin:admin -i -H 'Accept: application/json'"
	restURL = ("%s:%d/api/search/universal/keyword?query=*&keyword=%s&fields=%s&decorate=true&pretty=true&limit=1" % (grayServer,grayPort,keyword,field))
	curlCmd = curlURL + ' "' + restURL + '"'
	print ("curl is %s" % curlCmd)
	p = subprocess.Popen(curlCmd,shell=True, universal_newlines=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	fh = open(jsonFile,'w')
	flag = 0
	for line in p.stdout.readlines():
        	matchObj = re.search(r'^{',line)
        	if matchObj:
                	flag = 1
        	if flag:
                	fh.write(line)
	fh.close()
            

def parseJson(jsonFile,logfile):
	with open(jsonFile) as data_file:
		data = json.load(data_file)
		#print ("file is %s" % data["messages"][0]['message']['file'])
		fileName = data["messages"][0]['message']['file']
		print ("filename is %s" % fileName)
		print ("logfile is %s" % logfile)
		if fileName == logfile:
			print ("log files are matching, so it has been recieved")
		else:
			print ("log file are not matching , the log might not be in the server")
	

def main():
	args = parseArgs()
	print ("log file is %s" % args.logFile)
	print ("keyword is %s" % args.keyWord)
	args.keyWord = re.sub('\s+',"%20",args.keyWord)
	jsonFile = "graylog-query.json"
	print ("keyword is %s" % args.keyWord)
	cmd = ("sudo %s -c %s -once" % (fileBeatBin,fileBeatConf))
	runCommand(cmd)
	checkRestCall(args.keyWord,jsonFile)
	fileName = parseJson(jsonFile,args.logFile)
		
			

if __name__ == "__main__":
        main()

