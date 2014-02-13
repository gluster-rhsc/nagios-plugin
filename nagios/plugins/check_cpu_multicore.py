#!/usr/bin/python

############################################################################
# Author: Nishanth Thomas                    e-mail:  nthomas@redhat.com   #
############################################################################
# Nagios Plugin:   check_cpu_multicore.py                          #
#                                                                          #
# This plugin will colllect the CPU Statistics(Average and per core)       #
# Dependency:                                                              #
# This plugin uses 'mpstat'command to get the statistics.                  # 
# 'mpstat' is part of 'sysstat' which is not present in                    #
# RHEL by default. So 'sysstat' package should be installed on the taget   #
# system for this plugin to work correctly                                 #
#                                                                          #
############################################################################
import re,sys,commands,os,getopt

warn=85.00
crit=90.00

try:
    opts, args = getopt.getopt(sys.argv[1:],"hw:c:",["help", "warning=", "critical="])
except getopt.GetoptError as e:
    print (str(e))
    print 'Usage:check_cpu_profile_Multicore.py [-w warning] [-c critical] '
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', "--help"):
        print 'Usage:check_cpu_profile_Multicore.py [-w warning] [-c critical] '
        sys.exit()
    elif opt in ("-w", "--warning"):
        warn = arg
    elif opt in ("-c", "--critical"):
        warn = arg
    else:
        print 'Usage:check_cpu_profile_Multicore.py [-w warning] [-c critical] '
        sys.exit(2)

command_no_cpus = "nproc"
no_of_cpu = commands.getoutput(command_no_cpus)
out_reqd=int(no_of_cpu)+1

#if int(cpunumber) >= int(no_of_cpu):
#    print "Specified CPU Doesnot Exists"
#    sys.exit(2)

command_cpu_stat = "mpstat -P ALL 1 1| tail -n "+str(out_reqd)
#command_cpu_stat = "mpstat -P "+cpunumber+" 1 1 | grep Average"

#print command_cpu_stat

cpu_status = commands.getoutput(command_cpu_stat)
#print cpu_status
cpu_full_list = cpu_status.split("\n")
#print cpu_full_list
perf_data="num_of_cpu="+no_of_cpu+" "
cpu_usage_all_cores=0.0
idle_time_all_cores=''
for cpu in cpu_full_list:
#    print cpu
    cpu_list=cpu.split()
    idle_cpu = cpu_list[10]
    total_cpu = 100 - float(idle_cpu)
    sys_cpu = cpu_list[4]
    user_cpu = cpu_list[2]
    perf_data_total = str(total_cpu)+"%;"+str(warn)+";"+str(crit)
#    print perf_data_total
    perf_data += "cpu_"+cpu_list[1]+"_total="+perf_data_total+" cpu_"+cpu_list[1]+"_system="+sys_cpu+"% cpu_"+cpu_list[1]+"_user="+user_cpu+"% cpu_"+cpu_list[1]+"_idle="+idle_cpu+"% "
    if cpu_list[1] == 'all':
        cpu_usage_all_cores = total_cpu
        idle_time_all_cores = idle_cpu


if  cpu_usage_all_cores > crit:
    print "CPU Status CRITICAL: Total CPU: "+str(cpu_usage_all_cores)+"% Idle CPU: "+idle_time_all_cores+"%|"+perf_data
    sys.exit(2)
elif cpu_usage_all_cores > warn:
    print "CPU Status WARN: Total CPU: "+str(cpu_usage_all_cores)+"% Idle CPU: "+idle_time_all_cores+"%|"+perf_data
    sys.exit(1)
else:
    print "CPU Status OK: Total CPU: "+str(cpu_usage_all_cores)+"% Idle CPU: "+idle_time_all_cores+"%|"+perf_data
    sys.exit(0)

