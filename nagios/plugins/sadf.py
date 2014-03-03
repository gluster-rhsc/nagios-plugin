#!/usr/bin/python
# sadf.py -- nagios plugin uses sadf output for perf data
# Copyright (C) 2014 Red Hat Inc
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
#

import os
import sys
import shlex
import subprocess
import json
import datetime
import math
import argparse
_twoMinutes = datetime.timedelta(minutes=2)
_sadfCpuCommand = "sadf -j -- -P ALL"
_sadfMemoryCommand = "sadf -j -- -r"
_sadfNetworkCommand = "sadf -j -- -n DEV"
_sadfSwapSpaceCommand = "sadf -j -- -S"


class sadfCmdExecFailedException(Exception):
    message = "sadf command failed"

    def __init__(self, rc=0, out=(), err=()):
        self.rc = rc
        self.out = out
        self.err = err

    def __str__(self):
        o = '\n'.join(self.out)
        e = '\n'.join(self.err)
        if o and e:
            m = o + '\n' + e
        else:
            m = o or e

        s = self.message
        if m:
            s += '\nerror: ' + m
        if self.rc:
            s += '\nreturn code: %s' % self.rc
        return s


def execCmd(command):
    proc = subprocess.Popen(command,
                            close_fds=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    return (proc.returncode, out, err)


def _sadfExecCmd(sadfCmd):
    now = datetime.datetime.now()
    start = (now - _twoMinutes).strftime("%H:%M:%S")
    end = now.strftime("%H:%M:%S")
    cmd = sadfCmd + " -s %s -e %s" % (start, end)

    try:
        (rc, out, err) = execCmd(shlex.split(cmd))
    except (OSError, ValueError) as e:
        raise sadfCmdExecFailedException(err=[str(e)])

    if rc != 0:
        raise sadfCmdExecFailedException(rc, [out], [err])

    j = json.loads(out)
    return j['sysstat']['hosts'][0]['statistics']


def _getLatestStat(stats):
    if not stats:
        return {}
    lstat = stats[0]
    latestTime = datetime.datetime.strptime(lstat['timestamp']['time'],
                                            "%H:%M:%S")
    for s in stats[1:]:
        thisTime = datetime.datetime.strptime(s['timestamp']['time'],
                                              "%H:%M:%S")
        if latestTime < thisTime:
            lstat = s
            latestTime = thisTime

    return lstat


def getLatestSadfCpuStat():
    return _getLatestStat(_sadfExecCmd(_sadfCpuCommand))


def getLatestSadfMemStat():
    return _getLatestStat(_sadfExecCmd(_sadfMemoryCommand))


def getLatestSadfNetStat():
    return _getLatestStat(_sadfExecCmd(_sadfNetworkCommand))


def getLatestSadfSwapStat():
    return _getLatestStat(_sadfExecCmd(_sadfSwapSpaceCommand))


def showCpuStat(warnLevel, critLevel):
    s = getLatestSadfCpuStat()
    if not s:
        sys.stdout.write("CPU UNKNOWN\n")
        sys.exit(3)
    perfLines = []
    idleCpu = 0
    for cpu in s['cpu-load']:
        if cpu['cpu'] == 'all':
            idleCpu = cpu['idle']
        perfLines.append(
            ("cpu_%s_total=%s%%;%s;%s cpu_%s_system=%s%% "
             "cpu_%s_user=%s%% cpu_%s_idle=%s%%" % (
                 cpu['cpu'], 100-cpu['idle'],
                 warnLevel, critLevel,
                 cpu['cpu'], cpu['system'],
                 cpu['cpu'], cpu['user'],
                 cpu['cpu'], cpu['idle'])))
        if len(s['cpu-load'])-1 == 1:
            break
    totalCpuUsage = 100 - idleCpu
    if totalCpuUsage > critLevel:
        sys.stdout.write(
            ("CPU Status CRITICAL: Total CPU:%s%% Idle CPU:%s%% "
             "| num_of_cpu=%s %s\n" % (totalCpuUsage, idleCpu,
                                       len(s['cpu-load'])-1,
                                       " ".join(perfLines))))
    elif totalCpuUsage > warnLevel:
        sys.stdout.write(
            ("CPU Status WARNING: Total CPU:%s%% Idle CPU:%s%% "
             "| num_of_cpu=%s %s\n" % (totalCpuUsage, idleCpu,
                                       len(s['cpu-load'])-1,
                                       " ".join(perfLines))))
    else:
        sys.stdout.write(
            ("CPU Status OK: Total CPU:%s%% Idle CPU:%s%% "
             "| num_of_cpu=%s %s\n" % (totalCpuUsage, idleCpu,
                                       len(s['cpu-load'])-1,
                                       " ".join(perfLines))))

    sys.exit(0)


def showSwapStat(warning, critical):
    s = getLatestSadfSwapStat()
    if not s:
        sys.stdout.write("IFACE UNKNOWN\n")
        sys.exit(3)
    totalSwap = s['memory']['swpfree'] + s['memory']['swpused']
    crit_value = (totalSwap * critical) / 100
    war_value = (totalSwap * warning) / 100
    if s['memory']['swpused'] >= crit_value:
        sys.stdout.write("CRITICAL")
        eStat = 2
    elif s['memory']['swpused'] >= war_value:
        sys.stdout.write("WARNING")
        eStat = 1
    else:
        sys.stdout.write("OK")
        eStat = 0
    sys.stdout.write("- %.2f%% used(%skB out of %skB)|Used=%skB;%s;"
                     "%s;0;%s\n" % (s['memory']['swpused-percent'],
                                    s['memory']['swpused'],
                                    totalSwap,
                                    s['memory']['swpused'],
                                    war_value,
                                    crit_value,
                                    totalSwap))
    sys.exit(eStat)


def showMemStat(warning, critical):
    s = getLatestSadfMemStat()
    if not s:
        sys.stdout.write("IFACE UNKNOWN\n")
        sys.exit(3)
    print s
    totalMem = s['memory']['memfree'] + s['memory']['memused']
    crit_value = (totalMem * critical) / 100
    war_value = (totalMem * warning) / 100
    if s['memory']['memused'] >= crit_value:
        sys.stdout.write("CRITICAL")
        eStat = 2
    elif s['memory']['memused'] >= war_value:
        sys.stdout.write("WARNING")
        eStat = 1
    else:
        sys.stdout.write("OK")
        eStat = 0
    sys.stdout.write("- %.2f%% used(%skB out of %skB)|Total=%skB;%s;%s;0;%s"
                     " Used=%skB Buffered=%skB"
                     " Cached=%skB\n" % (s['memory']['memused-percent'],
                                         s['memory']['memused'],
                                         totalMem,
                                         totalMem,
                                         war_value,
                                         crit_value,
                                         totalMem,
                                         s['memory']['memused'],
                                         s['memory']['buffers'],
                                         s['memory']['cached']))
    sys.exit(eStat)


def showNetStat(iface_list=None, list_type=None):
    s = getLatestSadfNetStat()
    if not s:
        sys.stdout.write("IFACE UNKNOWN\n")
        sys.exit(3)

    devNames = []
    perfLines = []
    for dev in s['network']['net-dev']:
        if list_type == "exclude":
            if dev['iface'] in iface_list:
                continue
        elif list_type == "include":
            if dev['iface'] not in iface_list:
                continue
        devNames.append(dev['iface'])
        perfLines.append("%s.rxpck=%s %s.txpck=%s %s.rxkB=%6.4f %s.txkB=%6.4f"
                         % (dev['iface'], dev['rxpck'],
                            dev['iface'], dev['txpck'],
                            dev['iface'], dev['rxkB'],
                            dev['iface'], dev['txkB']))

    sys.stdout.write("IFACE OK: %s |%s\n" % (", ".join(devNames),
                                             " ".join(perfLines)))
    sys.exit(0)


def parse_input():
    parser = argparse.ArgumentParser(usage='%(prog)s [-h] (\
\n-m -w <warning> -c <critical> |\n-s -w <warning> -c <critical>\
 |\n-cp -w <warning> -c <critical> |\n-n [-e EXCLUDE [EXCLUDE ...]\
 | -i INCLUDE [INCLUDE ...]])')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--memory', action='store_true',
                       help="Gives details related to memory")
    group.add_argument('-s', '--swap', action='store_true',
                       help="Gives details related to swap")
    group.add_argument('-cp', '--cpu', action='store_true',
                       help="Gives details related to cpu")
    group.add_argument('-n', '--network', action='store_true',
                       help="Gives details related to network")
    parser.add_argument("-w", "--warning", action="store", type=int,
                        help="Warning threshold in percentage")
    parser.add_argument("-c", "--critical", action="store", type=int,
                        help="Critical threshold in percentage")
    parser.add_argument("-e", "--exclude", action="store", nargs='+',
                        help="Parameters to be excluded")
    parser.add_argument("-i", "--include", action="store", nargs='+',
                        help="Parameters to be included")
    args = parser.parse_args()
    if args.memory or args.swap or args.cpu:
        if not args.critical or not args.warning:
            print "UNKNOWN:Missing critical/warning threshold value."
            sys.exit(3)
        if args.exclude or args.include:
            print "UNKNOWN:Exclude/Include is not valid for the given option."
            sys.exit(3)
        if args.critical <= args.warning:
            print "UNKNOWN:Critical must be greater than Warning."
            sys.exit(3)
    else:
        if args.critical or args.warning:
            print "UNKNOWN:Warning/Critical is not valid for the given option."
            sys.exit(3)
    return args


if __name__ == '__main__':
    args = parse_input()
    if args.memory:
        showMemStat(args.warning, args.critical)
    if args.swap:
        showSwapStat(args.warning, args.critical)
    if args.cpu:
        showCpuStat(args.warning, args.critical)
    if args.network:
        if args.exclude:
            showNetStat(args.exclude, "exclude")
        if args.include:
            showNetStat(args.include, "include")
        showNetStat()
