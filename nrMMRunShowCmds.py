from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from myfuncs.ImpFunct import get_credentials, read_file, generate_hosts_yaml


# Generate defaults.yaml file with username and password
def generate_defaults_yaml(username,password):
	'''Use user credentials to generate defaults.yaml file

	Parameters:
	username - username to SSH to the remote device
	password - password to SSH to the remote device

	Returns:
	'''
	with open('inventory/defaults.yaml', 'w') as df:
		df.write(f'---\nusername: {username}\npassword: {password}\n')


if __name__=='__main__':

	# Cosemtics for users
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
	
	# Iterate on each command
	for cmd in commands:
		nr_result = nr.run(task=netmiko_send_command, command_string=cmd)
		# Print AggregatedResult to screen
		print_result(nr_result)
		# Replace '|' and ' ' characters with '_' for filename
		cmd_name = cmd.replace('|','_').replace(' ','_')
		# Create a filename from each command and write to a file
		filename = f'result_{cmd_name}.txt'
		with open(filename, 'w+') as f:
			for key in nr_result.keys():
				print(nr_result[key][0], file=f)

	# Freeze screen until any key pressed
	input('Enter any key to exit!!!')