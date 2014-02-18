#!/usr/bin/python

import sys
import math
import argparse

def parse_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--warning",
                      action="store", type=int, help="Warning threshold for used in percentage")
    parser.add_argument("-c", "--critical",
                      action="store", type=int, help="Critical threshold for used in percentage")
    args = parser.parse_args()
    return args

def readLines(filename):
    f = open(filename, "r")
    lines = f.readlines()
    return lines

def get_mem_details():
    detail = {}
    for line in readLines('/proc/meminfo'):
        if line.split()[0] == 'MemTotal:':
            detail['memTotal'] = line.split()[1]
        if line.split()[0] == 'MemFree:':
            detail['memFree'] = line.split()[1]
        if line.split()[0] == 'Buffers:':
            detail['buffers'] = line.split()[1]
        if line.split()[0] == 'Cached:':
            detail['cached'] = line.split()[1]
    return detail

def to_mb(value):
    result = float(value) / (1024*1024)
    res =math.ceil(result * 100)/100
    return str(res)

def used(total,free):
    result = int(total) - int(free)
    return result

def print_val(msg_type,details,options,percent_used):
    used_crit_value = (int(details['memTotal']) * options.critical) / 100
    used_war_value = (int(details['memTotal']) * options.warning) / 100
    print msg_type + " - " + str(percent_used) + "% Used (" + to_mb(used(details['memTotal'],details['memFree'])) + "GB out of " + to_mb(details['memTotal']) + "GB)|" +\
        "Total=" + to_mb(details['memTotal']) + "GB;" + to_mb(used_war_value) + ";" + to_mb(used_crit_value) + ";0;" + to_mb(details['memTotal']) +\
        " Used=" + to_mb(used(details['memTotal'],details['memFree']))+\
        "GB Buffers="+ to_mb(details['buffers']) +\
        "GB Cached="+ to_mb(details['cached']) + "GB"

def display_mem_details(options):
    details = get_mem_details()
    free = (float(details['memFree']) * 100) / int(details['memTotal'])
    percent_free = math.ceil(free * 100)/100
    percent_used = 100 - percent_free
    if int(percent_used) >= options.critical:
        print_val("CRITICAL",details,options,percent_used)
        sys.exit(2)
    if int(percent_used) >= options.warning:
        print_val("WARNING",details,options,percent_used)
        sys.exit(1)
    else:
        print_val("OK",details,options,percent_used)
        sys.exit(0)


def memory_check():
    options = parse_input()
    if not options.critical:
        print "UNKNOWN: Missing critical threshold value."
        sys.exit(3)
    if not options.warning:
        print "UNKNOWN: Missing warning threshold value."
        sys.exit(3)
    if int(options.critical) <= int(options.warning):
        print "UNKNOWN: Critical percentage can't be equal to or lesser than warning percentage."
        sys.exit(3)
    display_mem_details(options)


if __name__ == '__main__':
    memory_check()
