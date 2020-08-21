# Network automation codes - originally written for Cisco switches and routers
Network Automation using Nornir Automation Framework


You can download and use these codes for Cisco IOS XE devices. Here is the list of files you will need:

- devices.txt ==> contians the IP addresses of network equipments you need to SS
H to. Please modify it to the correct IP addresses you want to SSH to.

- show\_commands.txt ==> list of show commands you need to run --> One command per line. Please modify it with the correct commands you need to run. I have added all the commands I used when I was checking for Phase-2&3 LAN Upgrade.

- config\_commands.txt ==> list of commands to run in "config t" mode --> One command per line. You can enter "do write memory" to save at the end of the configuration change. As Cisco IOS XE devices do not have "commit", please make sure (quadriple check) your commands are correct.

- config.yaml ==> an inventory list containing info about hosts, groups and defa
ults setup. Do NOT modify!

- myfuncs ==> a package containing functions written by MM. Do NOT modify!

- inventory ==> a folder containing list of yaml files. Do NOT modify!

- nr\_show\_cmds.py ==> actual python script to run show commands. Do NOT modify (unless you know what you are doing)!

- nr\_common\_config\_changes.py ==> actual python script to perform configuration changes on one or more device(s). Do NOT modify (unless you know what you are doing)!

USAGE: Change directory to /src/Nornir (cd /src/Nornir); modify either show\_commands.txt or config\_commands.txt and devices.txt files; and run "python3 nr\_show\_cmds.py" or "python3 nr\_common\_config\_changes.py" without the quotation marks. You will be prompted to enter files containing devices and commands (simply press ENTER to use the default files), and enter your SSH username and password.


OUTPUT: If you enter correct information, the result will be displayed on the te
rminal. It is also written to a folder created by the script (name starts with "Nornir-" followed by datetime). When you open the folder, it consists of files
with the commands names.
