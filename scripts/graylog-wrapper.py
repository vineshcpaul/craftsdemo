#!/usr/bin/env python3

import subprocess,argparse



#Variables
fileBeatBin = "/usr/bin/filebeat"
fileBeatConf = "/etc/graylog/collector-sidecar/generated/filebeat.yml"
grayServer = "http://172.22.107.69"
grayPort = 9000

def parseArgs():
        parser = argparse.ArgumentParser()
        parser.add_argument("-l" , action='store', dest='logFile')
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

def checkRestCall():
	field = "file"
	keyword = "last%205%20minutes"
	curlURL = "curl -s -u admin:admin -i -H 'Accept: application/json'"
	restURL = ("%s:%d/api/search/universal/keyword?query=*&keyword=%s&fields=%s&decorate=true" % (grayServer,grayPort,keyword,field))
	curlCmd = curlURL + restURL
	print ("curl is %s" % curlCmd)
	
	

def main():
	args = parseArgs()
	print ("log file is %s" % args.logFile)
	cmd = ("sudo %s -c %s -once" % (fileBeatBin,fileBeatConf))
	runCommand(cmd)
	checkRestCall()
			

if __name__ == "__main__":
        main()

