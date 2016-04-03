#!/usr/bin/python

import json, subprocess, getopt, sys, os

def usage():
	#Print correct usage of the script
	print "Usage:\n\n -p, --path: path to tarballs\n -v, --version: build version\n -c, --config: path to config file\n"
	print "Example: ./deptool.py -c /root/deptool/config.json -v 3678 -p /root/deptool/source\n"

#Define script arguments/options
try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:v:c:', ['config=', 'path=','version='])
except getopt.GetoptError, err:
        print(err)
        usage()
        sys.exit(2)

#If less than 7 arguments supplied - print usage and exit 
if len(sys.argv) < 7:
        usage()
        exit(2)

#Assigning variables
for opt, arg in opts:
    if opt in ('-v', '--version'):
        build_version = arg
    elif opt in ('-p', '--path'):
        source_path = arg
    elif opt in ('-c', '--config'):
        config_path = arg
    else:
        usage()
        exit(2)

#Static variables
dest_path = '/mnt/kixeye'

#Verify variables
if os.path.exists(config_path) != True:
	print "Specified config file %s is missing. Please verify location." % config_path
	exit(2)
elif os.path.exists(source_path) != True:
	print "Specified directory %s containing tarballs is missing. Please verify location." % source_path
	exit(2)

#Bash commands
copy_tarball = "scp '%s'/'%s'-'%s'.tar.gz root@'%s':'%s'/'%s'"
bkp_untar_cmd = "cd %s/%s && for i in `ls`; do rm -rf *.orig; \
cp $i $i.orig; done && tar xzf %s-%s.tar.gz"

#Open and decode .json config file
with open(config_path) as config_file:
    data = json.load(config_file)

#Iterate over a list of hosts retrieved from the config file
for artifact in data:
        print "Working on %s artifatct...\n" % artifact
        for host in data[artifact]['hosts']:
                print "Copying file(s) to %s:" % host
                #Copy tarballs to corresponding locations on servers specified in the config file 
                subprocess.call(copy_tarball % (source_path,artifact,build_version,host,dest_path,artifact), shell = True)
                print "Backing up existing version and unpacking %s-%s.tar.gz..." % (artifact,build_version)
                #Backup existing files in /mnt/kixeye/<artifact>
                subprocess.call(["ssh", "root@%s" % host, bkp_untar_cmd % (dest_path,artifact,artifact,build_version)])
                print ""