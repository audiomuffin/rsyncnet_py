from subprocess import call
import os

user = null
server = null

start()

def start():

    if not os.geteuid() == 0:
        print 'Run this script as root. Type \'sudo su root \' and try again.'
        exit(0)
    else:
        print '''
        Welcome to the unofficial rsync.net sync setup for Mac OS X! This little Python script will help
        you setup automatic backups for Mac OS X.

        This has only been tested on OS X 10.6 and 10.7.

        If you're a GNU/Linux, BSD user, or someone who likes something more cross-platform, scheduling is for
        OS X only.

        I am not responsible for anything that goes wrong. You use this script at your own risk.

        Let's get started! 
        '''        

        config_file()
 
def config_file():

     print 'Let\'s see if your config file exists.'

    # if file exists, open and read
    try:
        open(config.txt)
        # extract username and server from files
        # declare username and server as global variables
    except IOError as e:
        # if config file doesn't exist, ask to make a new one
        print 'You don\'t seem to have a config file. I\'ll make one for you.'
        # ask for username/number and set as global variable
        askuser = raw_input('What is your rsync.net username?: ')
        # ask for rsync.net server and set as global variable
        askserv = raw_input('What server is your rsync.net account hosted from?: ')
        # write in format 'askuser@askserv.rsync.net' to config file
            
    # ask if SSH key pair exists
    askconfig = raw_input('Have you created an SSH key pair? (If you\'re not sure, you probably haven\'t) (y/n): ')
    if askconfig == 'yes':
        # if it exists, push key to server
        scp()
    else:
        # else, generate the key
        keygen()

def keygen():
    print '''
    Sit back. We\'re generating a key for you.

    Don't add a password, just answer \'no\' for all the following questions.
    '''
    # run 'ssh-keygen -t rsa'

    scp()

def scp():
    asker = raw_input('Is this the only computer you\'re planning to sync, or the first one 
    you\'re setting up? (y/n): ')

    if asker == y:
        print "Pushing the key to the server."
        # run 'scp /var/root/.ssh/id_rsa.pub askuser@askserv.rsync.net:.ssh/authorized_keys'
    else:
        print "Pushing the key to the server."
        # run cat ~/.ssh/id_rsa.pub | ssh askuser@askserv.rsync.net 'dd of=.ssh/authorized_keys oflag=append conv=notrunc'

    script()

def script():
    # if script does not exist
        # run 'touch /var/root/rsyncnet.sh'
        # run 'cat /var/root/rsyncnet.sh' and append the template for the script
            # should be like '/usr/bin/rsync -av /Users/JenniferMack 1234@usw-s001.rsync.net:'
        # run 'chmod +x /var/root/rsyncnet.sh'
        # set up schedule 'schedules()'
    # else, run '/var/root/rsyncnet.sh'

def schedules():
    print 'We\'ll set up the schedule.'
    # run 'cd /Library/LaunchAgents'
    # run 'curl -O http://www.rsync.net/resources/examples/rsyncnet.daily.plist'
    # run 'launchctl load rsyncnet.daily.plist'
    askme = raw_input('Your backups will occur at 2am, every day. Is this okay? (y/n): ')
    # if yes, exit program
        # thanks for using this script! If it helped you, please consider contributing by going to http://nayarb.info/support!
    # else, edit the script
