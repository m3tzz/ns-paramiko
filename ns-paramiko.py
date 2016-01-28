import paramiko
import time
import getpass
import sys

def load_file_host_config(host_file):

    ##### Read Host files ######
    file = open(host_file, 'r')
    ###### split the lines via /n #####
    host_tmp = file.read().split('\n')
    return host_tmp

def load_file_vip_config(vip_file):

    ##### Read Host files ######
    file = open(vip_file, 'r')
    ###### split the lines via /n #####
    #vip_tmp = file.read().split('\n')
    vip_tmp = file.read()
    return vip_tmp

def print_menu():

    print"\n"
    print"##################### NETSCALER #####################\n"
    print"Please choose one of the otpions below:\n"
    print"[1] - Send configs to NS.\n"
    print"[2] - Rollback configs to NS. \n\n"

def option_choosen(option,ns_ip):
     try :
            if (option == 1):
                print "\n###### SEND CONFIG TO NS - "+ns_ip[1]+" ########\n"
                send_config_to_ns(ip,username,password,output_buffer,file_vip)
            elif (option == 2):
                print "\n###### ROLLBACK CONFIG TO NS - "+ns_ip[1]+" ########\n"
                rollback_config_to_ns(ip,username,password,output_buffer,file_rollback_vip)
            else:
                print "\nSorry this option does not exist.\nThe script will be terminated!\n"
                sys.exit(0)
     except ValueError:
        print "\nSorry this option does not exist: "+ValueError+"\n.The script will be terminated!\n"
        sys.exit(0)

def send_config_to_ns(ip,username,password,output_buffer,file_vip):

    try:
        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()
        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # initiate SSH connection
        remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print "SSH connection established to %s" % ip+"\n"
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established\n"
    except paramiko.AuthenticationException:
        print "\nAuthentication Failed\n"
        sys.exit(0)
    except paramiko.SSHException:
        print "\nIssues with SSH service\n"
        sys.exit(0)
    except socket.error,e:
        print "\nConnection Error\n"
        sys.exit(0)

    # Strip the initial router prompt
    output = remote_conn.recv(output_buffer)
    # See what we have
    print output
    # Now let's try to send the NS a command
    enter="\n"
    ##### add new config #####


    for l in range (0,1):
            #remote_conn.send(enter.join(file_vip))
            remote_conn.send(file_vip)

    remote_conn.send("save ns config\n")
    # Wait for the command to complete
    time.sleep(5)

    output = remote_conn.recv(output_buffer)


    # See what we have
    print output

def rollback_config_to_ns(ip,username,password,output_buffer,file_rollback_vip):

    try:
        # Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()
        # Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # initiate SSH connection
        remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print "SSH connection established to %s" % ip+"\n"
        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established\n"
    except paramiko.AuthenticationException:
        print "\nAuthentication Failed\n"
        sys.exit(0)
    except paramiko.SSHException:
        print "\nIssues with SSH service\n"
        sys.exit(0)
    except socket.error,e:
        print "\nConnection Error\n"
        sys.exit(0)

    # Strip the initial router prompt
    output = remote_conn.recv(output_buffer)
    # See what we have
    print output
    # Now let's try to send the NS a command
    enter="\n"
    ##### add new config #####
    for l in range (0,1):
            #remote_conn.send(enter.join(file_rollback_vip))
            remote_conn.send(file_rollback_vip)
    remote_conn.send("save ns config\n")
    # Wait for the command to complete
    time.sleep(5)

    output = remote_conn.recv(output_buffer)



    #if "ERROR:" not in output:
    #    print "we receveid this error:"+ output
    #    sys.exit(0)

    # See what we have
    print output


if __name__ == '__main__':

    ########### read info from host file ############
    host_tmp = load_file_host_config('hosts_file.txt')

    ####### LOGIN TACACS ########
    print "\n\n##################### TACACS Login #####################\n"
    username = raw_input('\ninsert your username:')
    password = getpass.getpass("Enter your password:")
    ####### END LOGIN TACACS ########

    ###### print menu ######
    print_menu()
    ###### option ######
    option = int(raw_input("[option]:"))

    ######### split IP and Name of NS and run the instruction for all LBs on file #########
    for ns_ip in host_tmp:
        if len(ns_ip) <= 2:
            continue
        #### define what is IP of NS #####
        ns_ip = str(ns_ip).split(' ')
        ############ read info from config file ############
        file_vip = load_file_vip_config('newconfig.txt')
        #file_vip = file_vip_tmp.replace('{ip}','1.1.1.1')
        ############ read info from rollback file ############
        file_rollback_vip = load_file_vip_config('rollback.txt')

        ##### IP of LB #####
        ip=ns_ip[0]

        output_buffer = 1000000

        ##### Option Choosen ######
        option_choosen(option,ns_ip)


    sys.exit(0)
