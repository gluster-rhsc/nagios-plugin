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


def showNetStat():
    s = getLatestSadfNetStat()
    if not s:
        sys.stdout.write("IFACE UNKNOWN\n")
        sys.exit(3)

    devNames = []
    perfLines = []
    for dev in s['network']['net-dev']:
        devNames.append(dev['iface'])
        perfLines.append("%s.rxpck=%s %s.txpck=%s %s.rxkB=%s %s.txkB=%s" %
                         (dev['iface'], dev['rxpck'],
                          dev['iface'], dev['txpck'],
                          dev['iface'], dev['rxkB'],
                          dev['iface'], dev['txkB']))

    sys.stdout.write("IFACE OK: %s |%s\n" % (", ".join(devNames),
                                             " ".join(perfLines)))
    sys.exit(0)


def showUsage():
    usage = "usage: %s <net>\n" % os.path.basename(sys.argv[0])
    sys.stderr.write(usage)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        showUsage()
        sys.exit(-1)

    statType = sys.argv[1]

    if statType.upper() == "NET":
        showNetStat()
