#!/usr/bin/python

import re
import sys
import commands
from optparse import OptionParser


def getUsageAndFree(command):
    status = commands.getstatusoutput(command)[1].split()
    path = status[-1]
    usagePer = status[-2]
    usedSpace = status[-3]
    availSpace = status[-4]
    device = status[-6]
    dmatch = re.compile('[0-9]+').match(usagePer)
    if (dmatch):
        usage = eval(dmatch.group(0))
        return (float(usage), float(100 - usage), usedSpace,
                availSpace, device, path)
    else:
        print "STATE UNKNOWN"
        sys.exit(3)


def getDisk(path):
    return getUsageAndFree("df -kh %s" % path)


def getInode(path):
    cmd = "df -i %s" % path
    usagePer, availablePer, used, avail, dev, path = getUsageAndFree(cmd)
    return usagePer, availablePer, dev, path


def appendStatus(lst, level, typ, device, mpath, usage):
    if 2 == level:
        level = "crit"
    elif 1 == level:
        level = "warn"
    else:
        level = "ok"
    lst.append("%s:%s:%s;%s;%s" % (level, device, mpath, usage))

parser = OptionParser()
parser.add_option('-w', '--warning', action='store', type='int',
                  dest='warn', help='Warning count in %', default=20)
parser.add_option('-c', '--critical', action='store', type='int',
                  dest='crit', help='Critical count in %', default=10)
parser.add_option('-p', '--path', action='append', type='string',
                  dest='mountPath', help='Mount path')

(options, args) = parser.parse_args()
if not options.mountPath:
    options.mountPath = []
    f = open("/etc/mtab")
    for i in f.readlines():
        if i.startswith("/"):
            options.mountPath.append(i.split()[0])
    f.close()

if not options.mountPath:
    parser.print_help()
    sys.exit(1)

crit = 100 - options.crit
warn = 100 - options.warn

disk = []
warnList = []
critList = []
diskList = []
level = -1
for path in options.mountPath:
    diskUsage, diskFree, used, avail, dev, mpath = getDisk(path)
    inodeUsage, inodeFree, idev, ipath = getInode(path)
    disk.append("%s=%.2f;%s;%s;0;100 %s=%.2f;%s;%s;0;100" % (path, diskUsage,
                                                             warn, crit, path,
                                                             inodeUsage, warn,
                                                             crit))
    #status.append(" %s %s(Used %s)" % (path, used, avail))

    if diskUsage >= crit or inodeUsage >= crit:
        if diskUsage >= crit:
            critList.append("crit:disk:%s;%s;%s" % (dev, mpath, diskUsage))
        else:
            critList.append("crit:inode:%s;%s;%s" % (idev, ipath, inodeUsage))
        if not level > 1:
            level = 2
    elif (diskUsage >= warn and diskUsage < crit) or (
            inodeUsage >= warn and inodeUsage < crit):
        if diskUsage >= warn:
            warnList.append("warn:disk:%s;%s;%s" % (dev, mpath, diskUsage))
        else:
            warnList.append("warn:inode:%s;%s;%s" % (idev, ipath, inodeUsage))
        if not level > 0:
            level = 1
    else:
        diskList.append("%s:%s" % (dev, mpath))
    #    okList.append("ok:disk:%s;%s;%s" % (dev, mpath, diskUsage))

msg = " ".join(critList + warnList)
if not msg:
    msg += " disks:mounts:(" + ",".join(diskList) + ")"

if 2 == level:
    print "CRITICAL : %s | %s" % (msg, " ".join(disk))
    sys.exit(2)
elif 1 == level:
    print "WARNING : %s | %s" % (msg, " ".join(disk))
    sys.exit(1)
else:
    print "OK : %s | %s" % (msg, " ".join(disk))
    sys.exit(0)
