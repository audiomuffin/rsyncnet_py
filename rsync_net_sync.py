# current version: 0.1.2

import os

def mac_rsyncnet():
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
    on OS X.\n
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
    schedbool = True

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
    
def win_rsyncnet():
    print '\nSorry! This hasn\'t been implemented yet. :(\n'
    
def nix_rsyncnet():
    print '\nSorry! This hasn\'t been implemented yet. :(\n'

    
if not os.geteuid() == 0: # checks to see if program is run by root user
    print 'Run this script as root. Type \'sudo su root\' and try again.'
    exit(0)
else:
    print '''
    \nWelcome to the unofficial rsync.net sync setup for Mac OS X! This little Python script will help
    you setup automatic backups for Mac OS X, using rsync.net, or any other rsync provider.

    This has only been tested on OS X 10.6 and 10.7.

    If you're a GNU/Linux, BSD user, or someone who likes something more cross-platform, a script will
    be available to you soon.

    I am not responsible for anything that goes wrong. You use this script at your own risk.
    
    Please visit http://nayarb.info for more information.

    Let's get started!
    ''' 

global user
global directory

choosebool = True
    
while choosebool:
    choicex = raw_input('Choose which you\'d like to sync (m/w/u): ')
    if choicex == 'm':
        mac_rsyncnet()
        choosebool = False
    elif choicex == 'w':
        win_rsyncnet()
    elif choicex == 'u':
        nix_rsyncnet()
    else:
        print 'Invalid input! Try again.'