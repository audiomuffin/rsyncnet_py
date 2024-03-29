# current version: 0.2.0

import os

if not os.geteuid() == 0: # checks to see if program is run by root user
    print 'Run this script as root. Type \'sudo su root\' and try again.'
    exit(0)
else:
    print '''
    \nWelcome to the unofficial rsync.net sync setup for Mac OS X! This little Python script will help
    you setup automatic backups for Mac OS X, using rsync.net, or any other rsync provider.

    This has only been tested on OS X 10.6 and 10.7. The Unix version is testing.
    
    I am not responsible for anything that goes wrong. You use this script at your own risk.
    
    Please visit http://nayarb.info for more information.

    Let's get started!\n
    '''
    
    # asks user what OS they are using
nixbool = True
    
global oschoice
    
while nixbool:
    nixask = raw_input('Which OS are you using? Input m for Mac OS X, and u for Unix or Unix-like OS (such as GNU/Linux or BSD (m/u): ')
    if nixask == 'm':
        oschoice = 'm'
        nixbool = False
    elif nixask == 'u':
        oschoice = 'u'
        nixbool = False
    else:
        print 'Invalid input! Try again.'
    
global user
global directory

print '''\nFor the following, enter your username and password in the following format:
    
1234@usw-s001.rsync.net
    
where '1234' is your user ID and 'usw-s001' designates your main server.
This information should be available in the introductory rsync.net email.
'''
    
# uses SSH to check if user info checks out
userbool = True
    
while userbool:
    user = raw_input('Enter the info here: ')
    sshcheck = 'ssh %s' % (user)
    print '\nWhen asked, please enter your rsync.net password.\n'
    if os.system(sshcheck) == 0:
        print '\nYour account is valid.\n'
        userbool = False
    else:
        print '\nIncorrect login info. Try again.\n'

print '''
\nWhat directory do you want to back up? For example,
backing up the Documents folder for username \'nayarb\' would be /Users/nayarb/Documents
on OS X.
    
For GNU/Linux or BSD, it might be /home/nayarb/Documents.
'''

dirbool = True

# checks to see if the directory input exists
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
        print 'On to the next step.\n' # if they do, skips to the next step
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
            pushbool = False
        else:
            print 'Pushing key to server failed! Check your \'user\' variable.'
            exit(0)
    elif pushme == 'n': # adds an ssh key to exising authorized_keys file
        pushkey = 'cat ~/.ssh/id_rsa.pub | ssh %s \'dd of=.ssh/authorized_keys oflag=append conv=notrunc\'' % (user) # pushes key as to not erase others
        if os.system(pushkey) == 0:
            print 'Pushing key to server successful.'
            pushbool = False
        else:
            print 'Pushing key to server failed! Check your \'user\' variable.'
            exit(0)
    else:
        print 'Invalid input! Try again.'

# creates new file, inserts line, and adds permissions
echomod = ('echo \'/usr/bin/rsync -av %s %s:\' > /var/root/rsyncnet.sh') % (directory, user)
os.system(echomod)
os.system('chmod +x /var/root/rsyncnet.sh')
    
# set up the schedule
schedbool = True
    
if oschoice == 'm': # for Mac OS X
    while schedbool:
        schedme = raw_input('\nWould you like to set up a schedule? (y/n) ')
        if schedme == 'y':
            os.system('curl -O http://www.rsync.net/resources/examples/rsyncnet.daily.plist')
            os.system('mv rsyncnet.daily.plist /Library/LaunchAgents/rsyncnet.daily.plist')
            os.system('launchctl load /Library/LaunchAgents/rsyncnet.daily.plist')
            print '''
            \nYour schedule has been set up! It will backup your directory at 2am.
            If you want to change that, edit the "Integers" variable on the File
            /Library/LaunchAgents/rsyncnet.daily.plist with your favorite text editor.\n
            '''
            schedbool = False
        elif schedme == 'n':
            print 'Moving on.'
            schedbool = False
        else:
            print 'Invalid input! Try again.'
else: # for Unix (and OS X users who prefer cron) WARNING: NOT TESTED YET
    while schedbool:
        schedme = raw_input('\nWould you like to set up a schedule? (y/n) ')
        if schedme == 'y':
            print '''
            \nSorry, but you\'ll have to edit this by hand. I'll run crontab -e 
            for you and you can edit it. If you don't know how to do it, search 
            it up on Google. For now, you can copy/paste this to have it backing 
            up at 2am:
                
            * 2 * * * /var/root/rsyncnet.sh
                
            Just change the 2 into any number between 0 and 23 for what hour you'd
            like.\n
            '''
            raw_input('\nPress a key to continue.\n')
                
            os.system('crontab -e')
            schedbool = False
        elif schedme == 'n':
            print 'Moving on.'
            schedbool = False
        else:
            print 'Invalid input! Try again.'
            
# ask to test the script        
finbool = True

while finbool:   
    finalt = raw_input('We\'re done! Would you like to test the script now? (y/n) ')
    if finalt == 'y':
        print 'Running script. Thanks for using rsync_net_osx! :)'
        os.system('/var/root/rsyncnet.sh')
        finbool = False
    elif finalt == 'n':
        print 'Thanks for using me! Please visit http://nayarb.info!'
        finbool = False
    else:
        print 'Invalid input! Try again.'
