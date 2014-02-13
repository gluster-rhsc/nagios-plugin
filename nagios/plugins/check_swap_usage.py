#!/usr/bin/python

from optparse import OptionParser
import sys
import math

def parse_input():
    parser = OptionParser(usage="%prog -w <warning threshold> -c <critical threshold> [ -h ]",version="%prog ")
    parser.add_option("-w", "--warning",
                      action="store", type="string", dest="warn_threshold", help="Warning threshold for used in percentage")
    parser.add_option("-c", "--critical",
                      action="store", type="string", dest="crit_threshold", help="Critical threshold for used in percentage")
    (options, args) = parser.parse_args()
    return options

def readLines(filename):
    f = open(filename, "r")
    lines = f.readlines()
    return lines

def get_swap_details():
    detail = {}
    for line in readLines('/proc/meminfo'):
        if line.split()[0] == 'SwapTotal:':
            detail['swapTotal'] = line.split()[1]
        if line.split()[0] == 'SwapFree:':
            detail['swapFree'] = line.split()[1]
    return detail

def to_gb(value):
    result = float(value) / (1024*1024)
    res = math.ceil(result*100)/100
    return str(res)

def used(total,free):
    result = int(total) - int(free)
    return result

def print_val(msg_type,details,options,percent_free):
    free_crit_value = (int(details['swapTotal']) * int(options.crit_threshold)) / 100
    free_war_value = (int(details['swapTotal']) * int(options.warn_threshold)) / 100
    print "SWAP " + msg_type + " - " + str(percent_free) + "% free (" + to_gb(details['swapFree']) + "GB out of " + to_gb(details['swapTotal']) + "GB) |" +\
        "swap=" + to_gb(details['swapFree']) + "GB;" + to_gb(free_war_value) + ";" + to_gb(free_crit_value) + ";0;" + to_gb(details['swapTotal'])

def display_swap_details(options):
    details = get_swap_details()
    free = (float(details['swapFree']) * 100) / int(details['swapTotal'])
    percent_free = math.ceil(free * 100)/100
    if int(percent_free) <= int(options.crit_threshold):
        print_val("CRITICAL",details,options,percent_free)
        sys.exit(2)
    if int(percent_free) <= int(options.warn_threshold):
        print_val("WARNING",details,options,percent_free)
        sys.exit(1)
    else:
        print_val("OK",details,options,percent_free)
        sys.exit(0)


def memory_check():
    options = parse_input()
    if not options.crit_threshold:
        print "UNKNOWN: Missing critical threshold value."
        sys.exit(3)
    if not options.warn_threshold:
        print "UNKNOWN: Missing warning threshold value."
        sys.exit(3)
    if int(options.crit_threshold) >= int(options.warn_threshold):
        print "UNKNOWN: Critical percentage can't be equal to or greater than warning percentage."
        sys.exit(3)
    display_swap_details(options)


if __name__ == '__main__':
    memory_check()
