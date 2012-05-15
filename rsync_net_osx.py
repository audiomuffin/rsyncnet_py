# current version: 0.0.2

import os

def config_rsyncnet():
    print '''For the following:
    
    Enter your username and password in the following format:
    
    1234@usw-s001.rsync.net
    
    where '1234' is your user ID and 'usw-s001' designates your main server.
    
    This information should be available in the introductory rsync.net email.
    '''

    global user

    user = raw_input('Enter the info here: ')

    print '''What directory do you want to back up? For example,
    backing up the Documents folder for username \'nayarb\' would be /Users/nayarb/Documents
    on OS X.'''

    global directory

    dirbool = True

    # CHECK DIRECTORY NOT WORKING YET
    while dirbool:
        directory = raw_input('Enter the directory here: ') # user inputs desired directory
        if not os.path.exists(directory): # checks to see if directory exists
            print 'Directory does not exist! Enter a new one.' # if it doesn't, asks the user to enter another directory
        else:
            dirbool = False

    # SSH Keypair setup
    sshbool = True

    while sshbool:
        sshkey = raw_input('Do you have a SSH keypair setup? (y/n) ') # asks user if they have an SSH keypair set up
        if sshkey == 'y':
            print 'On to the next step.' # if they do, skips to the next step
            sshbool = False
        elif sshkey == 'n':
            print 'I\'ll create an SSH keypair for you.'
            os.system('ssh-keygen -t rsa') # if they don't, creates a pair
            sshbool = False
        else:
            print 'Invalid input! Try again.'
    
    # Pushes the private key to your account
    pushbool = True

    while pushbool:
        pushme = raw_input('Is this the only computer you will sync? (y/n) ')
        if pushme == 'y':
            pushkey = 'scp /var/root/.ssh/id_rsa.pub %s:.ssh/authorized_keys' % (user) # pushes key to override all keys
            if os.system(pushkey) == 0:
                print 'Pushing key to server successful.'
            else:
                print 'Pushing key to server failed! Check your \'user\' variable.'
                exit(0)
            pushbool = False;
        elif pushme == 'n':
            pushkey = 'cat ~/.ssh/id_rsa.pub | %s \'dd of=.ssh/authorized_keys oflag=append conv=notrunc\'' % (user) # pushes key as to not erase others
            if os.system(pushkey) == 0:
                print 'Pushing key to server successful.'
            else:
                print 'Pushing key to server failed! Check your \'user\' variable.'
                exit(0)
            pushbool = False;
        else:
            print 'Invalid input! Try again.'

    # creates new file, inserts line, and adds permissions
    echomod = ('echo \'/usr/bin/rsync -av %s %s:\' > /var/root/rsyncnet.sh') % (directory, user)
    os.system(echomod)
    os.system('chmod +x /var/root/rsyncnet.sh')
    
    # set up the schedule
    os.system('cd /Library/LaunchAgents')
    os.system('curl -O http://www.rsync.net/resources/examples/rsyncnet.daily.plist')
    os.system('launchctl load rsyncnet.daily.plist')
    
    finbool = True

    while finbool:   
        finalt = raw_input('We\'re done! Would you like to test the script now? (y/n)')
        if finalt == 'y':
            print 'Running script. Thanks for using me! :)'
            os.system('/var/root/rsyncnet.sh')
            finbool = False
        elif finalt == 'n':
            print 'Thanks for using me! Please visit http://nayarb.info!'
            exit(0)
            finbool = False
        else:
            print 'Invalid input! Try again.'

    
if not os.geteuid() == 0: # checks to see if program is run by root user
    print 'Run this script as root. Type \'sudo su root\' and try again.'
    exit(0)
else:
    print '''
    Welcome to the unofficial rsync.net sync setup for Mac OS X! This little Python script will help
    you setup automatic backups for Mac OS X, using rsync.net, or any other rsync provider.

    This has only been tested on OS X 10.6 and 10.7.

    If you're a GNU/Linux, BSD user, or someone who likes something more cross-platform, a script will
    be available to you soon.

    I am not responsible for anything that goes wrong. You use this script at your own risk.
    
    Please visit http://nayarb.info for more information.

    Let's get started! 
    '''        
    config_rsyncnet()
