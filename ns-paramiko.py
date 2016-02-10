# author: Ruben Barbosa
# version: 2.0
# Description: Send configs to Netscaler Device and Rollback in case something went wrong

import paramiko
import time
import getpass
import sys
import os

# function to read files
def load_file_host_config(host_file):

    ##### Read Host files ######
    file = open(host_file, 'r')
    ###### split the lines via /n #####
    host_tmp = file.read().split('\n')
    return host_tmp

def load_file_vip_config(vip_file):

    ##### Read vip files ######
    file = open(vip_file, 'r')
    ###### split the lines via /n #####
    vip_tmp = file.read().split('\n')
    #vip_tmp = file.read()
    return vip_tmp

# function to print menu
def print_menu():

    print"\n"
    print"##################### NETSCALER #####################\n"
    print"Please choose one of the otpions below:\n"
    print"[1] - Generate the configs of new vip.\n"
    print"[2] - Send configs to NS.\n"
    print"[3] - Rollback configs to NS. \n\n"

# function to option choosen
def option_choosen(option,ns_ip):
     try :
            if (option == 1):
                print "\n###### GENERATE CONFIGS OF NEW VIP ########\n"
                # Passagem Parametros
                numberSVRS = int(raw_input('\ninsert number of servers:'))
                nameSVRS = raw_input('\ninsert name of servers:')
                protocol = raw_input('\ninsert name of protocol[e.g - TCP,SSL,HTTP]:')
                serviceSVRS = int(raw_input('\ninsert service running on servers[e.g - 8080,8443,9410]:'))
                newvip = raw_input('\ninsert name of New Vip[TLA of Prodcut]:')
                vipip1 = raw_input('\ninsert First IP of New Vip:')
                vipip2 = raw_input('\ninsert Second IP of New Vip:')
                #Export the configs to File
                f_ns1 = open('CONFIGS_OF_'+newvip.upper()+'.txt', 'w')
                sys.stdout = f_ns1
                print newVipPairs_NS(numberSVRS, nameSVRS,protocol, serviceSVRS, newvip, vipip1,vipip2)
                #Export the rollback to File
                f_ns2 = open('ROLLBACK_OF_'+newvip.upper()+'.txt', 'w')
                sys.stdout = f_ns2
                print rollback_newVipPAirs(numberSVRS, nameSVRS,protocol, serviceSVRS, newvip, vipip1,vipip2)
            elif (option == 2):
                print "\n###### SEND CONFIG TO NS - "+ns_ip[1]+" ########\n"
                send_config_to_ns(ip,username,password,buffer_size,waittime,file_vip)
            elif (option == 3):
                print "\n###### ROLLBACK CONFIG TO NS - "+ns_ip[1]+" ########\n"
                rollback_config_to_ns(ip,username,password,buffer_size,waittime,file_rollback_vip)
            else:
                print "\nSorry this option does not exist.\nThe script will be terminated!\n"
                sys.exit(0)
     except ValueError:
        print "\nSorry this option does not exist: "+ValueError+"\n.The script will be terminated!\n"
        sys.exit(0)

# function to send the configs to device
def send_config_to_ns(ip,username,password,buffer_size,waittime,file_vip):

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
    output = remote_conn.recv(buffer_size)
    # See what we have
    print output
    # Now let's try to send the NS a command
    enter="\n"

    # Read the content of the file
    for line in file_vip:
        if not line.strip():  # ignore blank lines
            continue
        elif line.startswith('#'):  # ignore comments
            continue
        else:   # process the line
            remote_conn.send(line+enter)

    remote_conn.send("save ns config\n")
    # Wait for the command to complete
    time.sleep(waittime)

    output = remote_conn.recv(buffer_size)

    # See what we have
    print output

def rollback_config_to_ns(ip,username,password,buffer_size,waittime,file_rollback_vip):

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
    output = remote_conn.recv(buffer_size)
    # See what we have
    print output
    # Now let's try to send the NS a command
    enter="\n"

    # Read the content of the file
    for line in file_rollback_vip:
        if not line.strip():  # ignore blank lines
            continue
        elif line.startswith('#'):  # ignore comments
            continue
        else:   # process the line
            remote_conn.send(line+enter)
            #time.sleep(3)
            #output = remote_conn.recv(buffer_size)
            #if output.find("Done") == -1:          # Check for failure note -1 is the position
            #    print output
            #    print "ERROR - Command failed:\n Finish program"
            #    sys.exit(0)

    remote_conn.send("save ns config\n")
    # Wait for the command to complete
    time.sleep(waittime)

    output = remote_conn.recv(buffer_size)

    # See what we have
    print output

# function to generate the configs of new vip
def newVipPairs_NS(numberSVRS, nameSVRS,protocol, serviceSVRS, newvip, vipip1,vipip2):

    if (protocol == 'HTTP' or protocol == 'http'):

        print "\nLB01-04\n#Add Servers"
        for i in range(0, numberSVRS):
            i += 1
            print "add server"+" "+nameSVRS+"00"+str(i)+" <IP> -state DISABLED"

        print "\n#Create "+protocol+" Services"
        for j in range(0, numberSVRS):
            j += 1
            print "add service svc-"+str(serviceSVRS)+"-"+nameSVRS+"00"+str(j)+" "+nameSVRS+"00"+str(j)+ " HTTP "+str(serviceSVRS)

        print "\n#HTTP & HTTPS Services for LB1/2 - RUN ONLY ON LB1"
        print "add cs vserver cs-80-"+newvip+" "+protocol+" "+vipip1+ " 80 -stateupdate ENABLED -caseSensitive OFF"
        print "add cs vserver cs-443-"+newvip+" SSL "+vipip1+" 443 -stateupdate ENABLED -caseSensitive OFF"
        print "\n#HTTP & HTTPS Services for LB3/4 - RUN ONLY ON LB4"
        print "add cs vserver cs-80-"+newvip+" "+protocol+" "+vipip2+" 80 -stateupdate ENABLED -caseSensitive OFF"
        print "add cs vserver cs-443-"+newvip+" SSL "+vipip2+" 443 -stateupdate ENABLED -caseSensitive OFF"
        print "\n#Create LB Container            "
        print "add lb vserver lb-80-"+newvip+".default "+protocol
        print "\n#Bind Certificate to 443 VIP     "
        print "bind ssl vserver cs-443-"+newvip+" -certkeyName wildcard.app.betfair.san"
        print "\n#Bind Services to LB vserver    "
        print "bind lb vserver  lb-80-"+newvip+".default svc-8080-"+nameSVRS+"00[1-"+str(numberSVRS)+"]"
        print "\n#Bind CS Vservers to LBs        "
        print "bind cs vserver cs-80-"+newvip+" lb-80-"+newvip+".default"
        print "bind cs vserver cs-443-"+newvip+" lb-80-"+newvip+".default"
        print "\n#GSLB Config ( Feature very important, this allow we have load balacing between Pairs on Netscalers)"
        print "\n#Add GSLB IPs as Servers          "
        print "add server gslb-cs-"+newvip+".belb0102 "+vipip1
        print "add server gslb-cs-"+newvip+".belb0304 "+vipip2
        print "\n#Add HTTP GSLB Service"
        print "add gslb vserver gslb-"+newvip+".services HTTP -backupLBMethod ROUNDROBIN"
        print "\n#Define GSLB HTTP Services on LB1/2 - RUN ONLY ON LB1"
        print "#(**downStateFlush = enabled, when a virtual server or a service goes down, the associated TCP session table is also cleared, forcing the client the open new TCP session, and a new LB decision is made.)"
        print "add gslb service gslb-80-"+newvip+".belb0102 gslb-cs-"+newvip+".belb0102 "+protocol+" 80 -publicIP "+vipip1+" -publicPort 80 -sitename gslb-ie1belb0102 -cltTimeout 180 -svrTimeout 360 -downStateFlush DISABLED"
        print "add gslb service gslb-80-"+newvip+".belb0304 gslb-cs-"+newvip+".belb0304 "+protocol+" 80 -publicIP "+vipip2+" -publicPort 80 -sitename gslb-ie1belb0304  -cltTimeout 180 -svrTimeout 360 -downStateFlush ENABLED"
        print "add gslb service gslb-443-"+newvip+".belb0102 gslb-cs-"+newvip+".belb0102 SSL 443 -publicIP "+vipip1+" -publicPort 443 -sitename gslb-ie1belb0102 -cltTimeout 180 -svrTimeout 360 -downStateFlush DISABLED"
        print "add gslb service gslb-443-"+newvip+".belb0304 gslb-cs-"+newvip+".belb0304 SSL 443 -publicIP "+vipip2+" -publicPort 443 -sitename gslb-ie1belb0304  -cltTimeout 180 -svrTimeout 360 -downStateFlush ENABLED"
        print "\n#Define GSLB HTTP Services on LB1/2 - RUN ONLY ON LB4"
        print "#(**downStateFlush = enabled, when a virtual server or a service goes down, the associated TCP session table is also cleared, forcing the client the open new TCP session, and a new LB decision is made.)"
        print "add gslb service gslb-80-"+newvip+".belb0102 gslb-cs-"+newvip+".belb0102 "+protocol+" 80 -publicIP "+vipip1+" -publicPort 80 -sitename gslb-ie1belb0102 -cltTimeout 180 -svrTimeout 360 -downStateFlush ENABLED"
        print "add gslb service gslb-80-"+newvip+".belb0304 gslb-cs-"+newvip+".belb0304 "+protocol+" 80 -publicIP "+vipip2+" -publicPort 80 -sitename gslb-ie1belb0304  -cltTimeout 180 -svrTimeout 360 -downStateFlush DISABLED"
        print "add gslb service gslb-443-"+newvip+".belb0102 gslb-cs-"+newvip+".belb0102 SSL 443 -publicIP "+vipip1+" -publicPort 443 -sitename gslb-ie1belb0102 -cltTimeout 180 -svrTimeout 360 -downStateFlush ENABLED"
        print "add gslb service gslb-443-"+newvip+".belb0304 gslb-cs-"+newvip+".belb0304 SSL 443 -publicIP "+vipip2+" -publicPort 443 -sitename gslb-ie1belb0304  -cltTimeout 180 -svrTimeout 360 -downStateFlush DISABLED"
        print "\n#Bind GSLB vservers to the VIP and give it the domain name."
        print "bind gslb vserver gslb-"+newvip+".services -serviceName gslb-80-"+newvip+".belb0102"
        print "bind gslb vserver gslb-"+newvip+".services -serviceName gslb-80-"+newvip+".belb0304"
        print "bind gslb vserver gslb-"+newvip+".services -domainName "+newvip+".services.betfair -TTL 5"

        print "save ns config"

    elif (protocol != 'HTTP' or protocol != 'http'):

        print "\nLB01-04\n#Add Servers"
        for i in range(0, numberSVRS):
            i += 1
            print "add server"+" "+nameSVRS+"00"+str(i)
        print "#Create "+protocol+" Services"
        for j in range(0, numberSVRS):
            j += 1
            print "add service svc-"+str(serviceSVRS)+"-"+nameSVRS+"00"+str(j)+" "+nameSVRS+"00"+str(j)+ " "+protocol+" "+str(serviceSVRS)
        print "\n#HTTP & HTTPS Services for LB1/2 - RUN ONLY ON LB1"
        print "add cs vserver cs-"+str(serviceSVRS)+"-"+newvip+" "+protocol+" "+vipip1+" "+str(serviceSVRS)+" -stateupdate ENABLED -caseSensitive OFF"

        print "\n#HTTP & HTTPS Services for LB3/4 - RUN ONLY ON LB4"
        print "add cs vserver cs-"+str(serviceSVRS)+"-"+newvip+" "+protocol+" "+vipip2+" "+str(serviceSVRS)+" -stateupdate ENABLED -caseSensitive OFF"


        print "\n#Create LB Container            "
        print "add lb vserver lb-"+str(serviceSVRS)+"-"+newvip+".default "+protocol

        print "\n#Bind Services to LB vserver    "
        print "bind lb vserver  lb-"+str(serviceSVRS)+"-"+newvip+".default svc-"+str(serviceSVRS)+"-"+nameSVRS+"00[1-"+str(numberSVRS)+"]"

        print "\n#Bind CS Vservers to LBs        "
        print "bind cs vserver cs-"+str(serviceSVRS)+"-"+newvip+" lb-"+str(serviceSVRS)+"-"+newvip+".default"

        print "\n#GSLB Config ( Feature very important, this allow we have load balacing between Pairs on Netscalers)"

        print "\n#Add LB IPs as Servers          "
        print "add server gslb-cs-"+newvip+".belb0102 "+vipip1
        print "add server gslb-cs-"+newvip+".belb0304 "+vipip2

        print "\n#Add HTTP GSLB Service"
        print "add gslb vserver gslb-"+newvip+".services HTTP -backupLBMethod ROUNDROBIN"

        print "\n#Define GSLB HTTP Services on LB1/2 - RUN ONLY ON LB1"
        print "#(**downStateFlush = enabled, when a virtual server or a service goes down, the associated TCP session table is also cleared, forcing the client the open new TCP session, and a new LB decision is made.)"
        print "add gslb service gslb-"+str(serviceSVRS)+"-"+newvip+".belb0102 gslb-cs-"+newvip+".belb0102 "+protocol+" "+str(serviceSVRS)+" -publicIP "+vipip1+" -publicPort 80 -sitename gslb-ie1belb0102 -cltTimeout 180 -svrTimeout 360 -downStateFlush DISABLED"
        print "add gslb service gslb-"+str(serviceSVRS)+"-"+newvip+".belb0304 gslb-cs-"+newvip+".belb0304 "+protocol+" "+str(serviceSVRS)+" -publicIP "+vipip2+" -publicPort 80 -sitename gslb-ie1belb0304  -cltTimeout 180 -svrTimeout 360 -downStateFlush ENABLED"

        print "\n#Define GSLB HTTP Services on LB3/4 - RUN ONLY ON LB4"
        print "\n#(**downStateFlush = enabled, when a virtual server or a service goes down, the associated TCP session table is also cleared, forcing the client the open new TCP session, and a new LB decision is made.)"
        print "add gslb service gslb-"+str(serviceSVRS)+"-"+newvip+".belb0102 gslb-cs-"+newvip+".belb0102 "+protocol+" "+str(serviceSVRS)+" -publicIP "+vipip1+" -publicPort 80 -sitename gslb-ie1belb0102 -cltTimeout 180 -svrTimeout 360 -downStateFlush ENABLED"
        print "add gslb service gslb-"+str(serviceSVRS)+"-"+newvip+".belb0304 gslb-cs-"+newvip+".belb0304 "+protocol+" "+str(serviceSVRS)+" -publicIP "+vipip2+" -publicPort 80 -sitename gslb-ie1belb0304  -cltTimeout 180 -svrTimeout 360 -downStateFlush DISABLED"

        print "\n#Bind GSLB vservers to the VIP and give it the domain name."
        print "bind gslb vserver gslb-"+newvip+".services -serviceName gslb-"+str(serviceSVRS)+"-"+newvip+".belb0102"
        print "bind gslb vserver gslb-"+newvip+".services -serviceName gslb-"+str(serviceSVRS)+"-"+newvip+".belb0304"
        print "bind gslb vserver gslb-"+newvip+".services -domainName "+newvip+".services.betfair -TTL 5"

        print "save ns config"

def rollback_newVipPAirs(numberSVRS, nameSVRS,protocol, serviceSVRS, newvip, vipip1,vipip2):
    if (protocol == 'HTTP' or protocol == 'http'):
        print "\n##### RollBack Plan ########\n"
        print "rm cs vserver cs-80-"+newvip
        print "rm cs vserver cs-443-"+newvip
        print "rm lb vserver lb-80-"+newvip+".default "+protocol
        print "rm server"+" "+nameSVRS+"[1-"+str(numberSVRS)+"]"
        print "\n##### GSLB CONFIG ########\n"
        print "rm gslb service gslb-80-"+newvip+".belb0102"
        print "rm gslb service gslb-80-"+newvip+".belb0304"
        print "rm gslb service gslb-443-"+newvip+".belb0102"
        print "rm gslb service gslb-443-"+newvip+".belb0304"
        print "rm gslb vserver gslb-"+newvip+".services"
        print "rm server gslb-cs-"+newvip+".belb0102"
        print "rm server gslb-cs-"+newvip+".belb0304"

        print "save ns config"

    elif (protocol != 'HTTP' or protocol != 'http'):
        print "\n##### RollBack Plan ########\n"
        print "rm cs vserver cs-"+str(serviceSVRS)+"-"+newvip
        print "rm lb vserver lb-"+str(serviceSVRS)+"-"+newvip+".default "+protocol
        print "rm server"+" "+nameSVRS+"[1-"+str(numberSVRS)+"]"
        print "\n##### GSLB CONFIG ########\n"
        print "rm gslb service gslb-"+str(serviceSVRS)+"-"+newvip+".belb0102"
        print "rm gslb service gslb-"+str(serviceSVRS)+"-"+newvip+".belb0304"
        print "rm gslb vserver gslb-"+newvip+".services"
        print "rm server gslb-cs-"+newvip+".belb0102"
        print "rm server gslb-cs-"+newvip+".belb0304"

        print "save ns config"


if __name__ == '__main__':

    ########### read info from host file ############
    host_tmp = load_file_host_config('hosts_file.txt')

    ####### LOGIN TACACS ########
    print "\n##################### TACACS Login #####################\n"
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

        buffer_size = 1000000
        waittime = 6

        ##### Option Choosen ######
        option_choosen(option,ns_ip)


    sys.exit(0)
