import os

def config_rsyncnet():
	print '''For the following:
	
	Enter your username and password in the following format:
	
	1234@usw-s001.rsync.net
	
	where '1234' is your user ID and 'usw-s001' designates your main server
	'''
	user = raw_input('Enter the info here: ')
	
	directory = raw_input('What directory do you want to back up? For example, \
	backing up the Documents folder for username \'nayarb\' would be /Users/nayarb/Documents \
	on OS X.')
	
	# If you do not have an SSH keypair, uncomment the following line
	# os.system('ssh-keygen -t rsa')
	
	# Pushes the private key to your account
	pushkey = 'scp /var/root/.ssh/id_rsa.pub %s:.ssh/authorized_keys' % (user)
	
	if os.system(pushkey) == 0:
		print 'Pushing key to server successful.'
	else:
		print 'Pushing key to server failed! Check your \'user\' variable.'
		exit(0)
	
	# creates new file, inserts line, and adds permissions
	os.system('cat /var/root/rsyncnet.sh')
    os.system('chmod +x /var/root/rsyncnet.sh')
    
    # scheduling
    print '''
    The default schedule will backup your directory at 2am. If you'd like to change 
    that, edit /Library/LaunchAgents/rsyncnet.daily.plist and change 
    
    <integer>2</integer>
    
    to another number. For example, 10pm would be a value of 22.
    '''
    os.system('cd /Library/LaunchAgents')
    os.system('curl -O http://www.rsync.net/resources/examples/rsyncnet.daily.plist')
    os.system('launchctl load rsyncnet.daily.plist')
    
    finalt = raw_input('We\'re done! Would you like to test the script now? (y/n)')
    
    if finalt == 'y':
    	print 'Running script. Thanks for using me! :)'
    	os.system('/var/root/rsyncnet.sh')
    else:
    	print 'Thanks for using me! Please visit http://nayarb.info!'
    	exit(0)
    
if not os.geteuid() == 0:
	print 'Run this script as root. Type \'sudo su root\' and try again.'
	exit(0)
else:
    print '''
    Welcome to the unofficial rsync.net sync setup for Mac OS X! This little Python script will help
    you setup automatic backups for Mac OS X.

    This has only been tested on OS X 10.6 and 10.7.

    If you're a GNU/Linux, BSD user, or someone who likes something more cross-platform, a script will
    be available to you soon.

    I am not responsible for anything that goes wrong. You use this script at your own risk.
    
    Please visit http://nayarb.info for more information.

    Let's get started! 
    '''        
    config_rsyncnet()
