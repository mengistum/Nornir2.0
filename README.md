# Network automation codes - originally written for Cisco switches and routers
Network Automation using Nornir Automation Framework


You can download and use these codes. Here is the list of files you will need:

- devices.txt ==> contians the IP addresses of network equipments you need to SS
H to. Please modify it to the correct IP addresses you want to SSH to.

- commands.txt ==> list of commands you need to run --> One command per line. Pl
ease modify it with the correct commands you need to run. I have added all the c
ommands I used when I was checking for Phase-2&3 LAN Upgrade.
# """Network Automation Code""" -- Originally written for Cisco switches and rou

- config.yaml ==> an inventory list containing info about hosts, groups and defa
ults setup. Do NOT modify!

- myfuncs ==> a package containing functions written by MM. Do NOT modify!

- inventory ==> a folder containing list of yaml files. Do NOT modify!

- nrMMRunShowCmds ==> actual python code to run. Do NOT modify (unless you know
what you are doing)!


USAGE: Change directory to /src/Nornir (cd /src/Nornir), and run "python3 nrMMRu
nShowCmds.py" without the quotation marks. You will be prompted to enter files c
ontaining devices (enter "devices.txt" without the quotation mark), commands (en
ter "commands.txt" without the quotation mark), your SSH username and password.


OUTPUT: If you enter correct information, the result will be displayed on the te
rminal. It is also written to a folder created by the script (name starts with "
NNornir-" followed by datetime). When you open the folder, it consists of files
with the commands names.
