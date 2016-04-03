################################
### Software deployment tool ###
################################

### Description ###

'deptool.py' script facilitates deployment of software into a cluster of Linux servers.

'source' directory contains tarballs with the source code/software in the following format: ‘<artifact>-<Version#>.tar.gz’.
Path to the source directory must be supplied to the script as a CLI argument using -p or --path option.

'config.json' is a configuration file in JavaScript Object Notation format. It describes which hosts each artifact should be deployed to.
Path to the configuration file must be supplied to the script as a CLI argument using -c or --config option.

deptool.py also must be supplied with a third argument -v or --version which describes software version which is about to be deployed. 

### Deployment ###

Run deptool.py script with the three mandatory arguments. Run without any arguments to see detailed help.

### Roll back ###

deptool.py creates a backup copy of every file at the destination directory before unpacking new version of software and stores it as <filename>.orig.
To roll back simply run "mv <filename>.orig <filename>". 



