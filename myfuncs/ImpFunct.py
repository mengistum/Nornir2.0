#!/usr/bin/env python

"""
Author: Meheretab Mengistu
Purpose: To provide frequently used functions in one place.
Version: 2.0
Date: August 16, 2020
"""

# Import getpass and netmiko modules
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,\
 NetMikoAuthenticationException


# Get Credentials
def get_credentials():
        """Get username and password

        Parameters:

        Returns:
        str: username
        str: password
        """

        username = input('\nPlease enter username: ')
        password = getpass()

        # Returns username and password
        return username, password


# Get a text file and return lists
def read_file(filename):
        """Read a file and return lists

        Parameters:
        filename - a text file to read

        Returns:
        list: lines
        """

        # Open file to read as 'file' using 'with' so that you do not \
        # have to explicitly close the file 'filename'.
        with open(filename) as file:
                lines = file.read().splitlines()

        # Return list of lines
        return lines


# Utilize Netmiko methods to connect to the network device and run \
# show commands
def connect_send(devices, commands, username, password):
        """SSH to devices, run the commands, and disconnect

        Parameters:
        devices - list of devices IP addresses
        commands - list of commands to run
        username - SSH username
        password - SSH password

        Returns:
        """

        # Iterate over the list of devices
        for ip in devices:
                # Prepare device object to send to Netmiko
                device = {'device_type':'cisco_ios', 'ip':ip, \
                'username':username, 'password':password}
                # Check whether there is Timeout or Authentication Error
                try:
                        # Setup connection to the device using Netmiko
                        connect_dev = ConnectHandler(**device)
                        # Prepare and open file to write to
                        filename = connect_dev.base_prompt + '.txt'
                        with open(filename, 'w') as f:
                                # Run each command on the device
                                for cmd in commands:
                                        f.write('*'*79)
                                        f.write(' '*15 + '\n' + cmd + '\n')
                                        f.write('*'*79)
                                        f.write('\n'*2)
                                        cmd_sent = connect_dev.send_command(cmd)
                                        f.write(cmd_sent + '\n'*2)
                                        f.write('#'*79)
                                        f.write('#'*79)
                                        # Print the result
                                        print(cmd_sent)
                                # Disconnect SSH to the device
                        connect_dev.disconnect()
                # Handle 'Authentication' and 'Timeout' errors.
                except (NetMikoAuthenticationException, \
                        NetMikoTimeoutException) as e:
                        print(str(e))


# Generate hosts.yaml file for Nornir
def generate_hosts_yaml(devices, filename):
        """Use devices IP info to generate hosts.yaml file

        Parameters:
        devices - list of devices IP addresses
        filename - a file to write hosts in yaml format

        Returns:
        """

        # Open hosts file (or create one) to add hosts
        with open(filename, 'w') as hf:
                # Make it YAML file by starting it with "---"
                hf.write('---')
                # Iterate over the list of IP addresses
                for ip in devices:
                        if ip[-2:]=='.1':
                                hf.write(f'\nSW_{ip}:')
                                hf.write(f'\n  hostname: {ip}')
                                hf.write('\n  groups:')
                                hf.write(f'\n    - BorderSW\n')
                        else:
                                hf.write(f'\nSW_{ip}:')
                                hf.write(f'\n  hostname: {ip}')
                                hf.write('\n  groups:')
                                hf.write(f'\n    - Switch\n')
                # Put "..." to indicate the end of the YAML file.
                hf.write('...')

