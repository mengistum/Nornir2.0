#!/usr/bin/env python

"""
Author: Meheretab Mengistu
Purpose: To modify configuration on Cisco switches
Version: 1.0
Date: August 20, 2020
"""

# Import NORNIR module, datetime module, OS module
# and myfuncs module (module written by me)
import os
from datetime import datetime
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_config
from nornir.plugins.functions.text import print_result
from myfuncs.imp_funct import get_credentials, read_file, generate_hosts_yaml


# Generate defaults.yaml file with username and password
def generate_defaults_yaml(username, password):
    """Use user credentials to generate defaults.yaml file

    Parameters:
    username - username to SSH to the remote device
    password - password to SSH to the remote device

    Returns:
    """

    # Open (or create and open) defaults.yaml file to store
    # username/password to SSH to devices
    with open('inventory/defaults.yaml', 'w') as default_file:
        default_file.write(f'---\nusername: {username}\npassword: {password}\n')


def main():
    """Execution begins here
    """
    # The following lines added to make it easy for human users to read
    print('\n' + '*' * 79)
    print('\n       Network automation built using NORNIR Automation Framework!!    \n')
    print('*' * 79 + '\n')

    # Get IP addresses of devices you want to connect and generate hosts.yaml file
    devices_txt = input('Please enter .txt file containing IP addresses [devices.txt]: ')\
     or 'devices.txt'
    devices = read_file(devices_txt)
    generate_hosts_yaml(devices, 'inventory/hosts.yaml')

    # Get the list of commands to run on each device
    commands_txt = input('Please enter .txt file containing commands [commands_config.txt]: ')\
     or 'commands_config.txt'

    # Get user credentials from the user
    username, password = get_credentials()
    # Generate 'inventory/defaults.yaml' file containing user credential
    generate_defaults_yaml(username, password)

    yes_or_no = input('\nYou are about to make configuration changes. \
Are you sure about the changes(Y/N)?[default is N]  ') or 'N'
    if yes_or_no.upper() == 'Y':
        second_y_or_n = input('\nWe are asking you again. Are you sure(Y/N)?[Y]  ') or 'Y'
        if second_y_or_n.upper() == 'N':
            print('\n\nConfiguration change cancelled during second Y/N confirmation request!!\n')
        else:
            # Instantiate a Nornir object from .yaml file
            nr_obj = InitNornir(config_file='config.yaml')

            # Get the current time
            time_now = datetime.now().isoformat(timespec='seconds')

            # Create a Folder as a holder for the output files
            dirname = 'Nornir-failed-' + time_now.replace(':', '')
            os.mkdir(dirname)

            # Run configuration changes using netmiko_send_config method
            nr_result = nr_obj.run(task=netmiko_send_config, config_file=commands_txt)
            # Print the result of the change on the client monitor
            print_result(nr_result)

            # Create a filename to store failed devices
            filename = '/'.join((dirname, 'failed_dev.txt'))
            # Open the file to write the IP Addresses of failed devices
            with open(filename, 'w') as failed_dev:
                # Print out devices with failed config changes
                for device, results in nr_result.items():
                    if results[0].failed:
                        # Split device string at "_" sign and take the IP address
                        print(f"{device.split('_')[1]}", file=failed_dev)

            # Replace username/password with a placeholder account
            generate_defaults_yaml('cisco', 'password')

    else:
        print('\n\nConfiguration change cancelled!!\n')


if __name__ == "__main__":

    main()

    # Press any key to exit
    input("Press any key to exit!!!")
