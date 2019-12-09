#!/usr/bin/python

# A script to ssh into a cisco device, set the terminal length
# such that paging is turned off, then run commands.
# the results go into 'resp', then are displayed.
# Tweak to your hearts content!

import paramiko
import cmd
import time
import sys


buff = ''
resp = ''

my_file = open("arista_ip_all.txt", "rb")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
for line in my_file:
		l = [i.strip() for i in line.decode().split(',')]
		IP = l[1]
		hostname = l[0]
		try:
			ssh.connect(IP, username='sshuser', password='sshpassword', timeout=10)
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        # komutcalistir!
			chan = ssh.invoke_shell()
			chan.settimeout(10)
			chan.send('routing-context vrf MGMT\n')
			time.sleep(1)
			chan.send('copy running-config scp://ftpuser@ftphostaddress/home/%s_%s\n' % (hostname,IP))
			time.sleep(2)
			chan.send('ftppassword\n')
			time.sleep(1)		
			#resp = chan.recv(9999)
			#output = resp.decode('ascii').split(',')
						#chan.send('\r\n')
						#time.sleep(1)	
			buff = ''
			while buff.find('complete') < 0:
				resp = chan.recv(9999)
				output = resp.decode('ascii').split(',')
				print (''.join(output))
				#print  ('%s, "Write OK"\n'%(IP))
		except paramiko.AuthenticationException:
			print ('%s, "Authentication Failed"\n'%(IP))
		except paramiko.SSHException as sshException:
			print('%s, "Unable to establish SSH connection"\n'%(IP))
		except paramiko.ssh_exception.NoValidConnectionsError as novalidconnection:
			print('%s, "Unable to connect Port 22"\n'%(IP))
		except Exception:
			#print('%s, "Error"\n'%(IP))
			pass


my_file.close()
ssh.close()


