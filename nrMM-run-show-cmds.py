#!/usr/bin/env python

"""
Author: Meheretab Mengistu
Purpose: A script based on Nornir framework to run one or more \
        "show commands" on one or more network devices, and save \
        the output to files.
Version: 2.0
Date: August 16, 2020
"""

# Import NORNIR module, datetime module, OS module \
# and myfuncs module (module written by me)
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from myfuncs.ImpFunct import get_credentials, read_file, generate_hosts_yaml
from datetime import datetime
import os


# Generate defaults.yaml file with username and password
def generate_defaults_yaml(username,password):
        """Use user credentials to generate defaults.yaml file

        Parameters:
        username - username to SSH to the remote device
        password - password to SSH to the remote device

        Returns:
        """

        # Open (or create and open) defaults.yaml file to store
        # username/password to SSH to devices
        with open('inventory/defaults.yaml', 'w') as df:
                df.write(f'---\nusername: {username}\npassword: {password}\n')


def main():

        # Execution begins here

        # The following lines added to make it easy for human users to read
        print('\n' + '*' * 79)
        print('\n       Network automation built using NORNIR Automation Framework!!    \n')
        print('*' * 79 + '\n')

        # Get IP addresses of devices you want to connect and generate hosts.yaml file
        devices_txt = input('Please enter txt file containing IP addresses: ')
        devices = read_file(devices_txt)
        generate_hosts_yaml(devices, 'inventory/hosts.yaml')

        # Get the list of commands to run on each device
        commands_txt = input('Please enter the text file containing commands: ')
        commands = read_file(commands_txt)

        # Get user credentials from the user and generate defaults.yaml file
        username, password = get_credentials()
        generate_defaults_yaml(username, password)

        # Instantiate a Nornir object
        nr = InitNornir(config_file='config.yaml')

        # Get the current time and modify it by replacing ':'' with ''
        time_now = datetime.now().isoformat(timespec='seconds')
        modified_time = time_now.replace(':','')

        # Create new Folder as a holder for the output files
        dirname = 'Nornir-' + modified_time
        os.mkdir(dirname)

        # Iterate on each command
        for cmd in commands:
                nr_result = nr.run(task=netmiko_send_command, command_string=cmd)
                # Print AggregatedResult to screen
                print_result(nr_result)
                # Replace '|' and ' ' characters with '_' for filename
                cmd_name = cmd.replace('|','_').replace(' ','_')
                # Create a filename from each command and write to a file
                filename = '/'.join((dirname, f'result_{cmd_name}.txt'))
                with open(filename, 'w+') as f:
                        # Print to a file in a human-friendly format
                        for device, results in nr_result.items():
                                if not results[0].failed:
                                        print(f'\n"{device}": \n\n{results[0].result}\n\n', file=f)

        # Generate placeholder username and password to delete the real
        # production username/password
        generate_defaults_yaml('cisco', 'password')


if __name__ == "__main__":

        main()

        # Freeze screen until any key pressed
        input('Enter any key to exit!!!')
