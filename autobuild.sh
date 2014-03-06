#!/bin/sh

echo
echo ... Gluster Nagios autogen ...
echo

## Check all dependencies are present
MISSING=""

# Check for rpmbuild
env rpmbuild --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
  RPMBUILD=rpmbuild
else
  MISSING="$MISSING rpmbuild"
fi

# Check for tar
env tar --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
  MISSING="$MISSING tar"
fi

## If dependencies are missing, warn the user and abort
if [ "x$MISSING" != "x" ]; then
  echo "Aborting."
  echo
  echo "The following build tools are missing:"
  echo
  for pkg in $MISSING; do
    echo "  * $pkg"
  done
fi
 
echo "Constructing gluster-nrpe"

rm -fr gluster-nrpe-1.1
mkdir gluster-nrpe-1.1

cp -a nagios/plugins/check_cpu_multicore.py gluster-nrpe-1.1
cp -a nagios/plugins/check_memory.py gluster-nrpe-1.1/
cp -a nagios/plugins/check_disk_and_inode.py gluster-nrpe-1.1/
cp -a nagios/plugins/check_swap_usage.py gluster-nrpe-1.1/
cp -a nagios/plugins/sadf.py gluster-nrpe-1.1/

tar -czf gluster-nrpe.tar.gz gluster-nrpe-1.1

rm -fr ~/rpmbuild/SOURCES/gluster-nrpe*
rm -fr ~/rpmbuild/BUILD/gluster-nrpe*
rm -fr ~/rpmbuild/BUILDROOT/gluster-nrpe*
rm -fr gluster-nrpe-1.1

mv gluster-nrpe.tar.gz ~/rpmbuild/SOURCES

echo "Constructing gluster-nagios"

rm -fr gluster-nagios-1.1
mkdir gluster-nagios-1.1

echo "Copying files: check_cpu_multicore.php"
echo "check_disk_and_inode.php"
echo "check_interfaces.php"
echo "check_memory.php"
echo "check_swap_usage.php"

cp -a server/pnp4nagios/templates/check_cpu_multicore.php gluster-nagios-1.1
cp -a server/pnp4nagios/templates/check_disk_and_inode.php gluster-nagios-1.1
cp -a server/pnp4nagios/templates/check_interfaces.php gluster-nagios-1.1
cp -a server/pnp4nagios/templates/check_memory.php gluster-nagios-1.1
cp -a server/pnp4nagios/templates/check_swap_usage.php gluster-nagios-1.1
cp -a server/config/gluster-commands.cfg gluster-nagios-1.1
cp -a server/config/gluster-host-groups.cfg gluster-nagios-1.1
cp -a server/config/gluster-host-services.cfg gluster-nagios-1.1
cp -a server/config/gluster-templates.cfg gluster-nagios-1.1
cp -a server/config/node1.cfg gluster-nagios-1.1 gluster-nagios-1.1

tar -czf gluster-nagios-1.1.tar.gz gluster-nagios-1.1

rm -fr ~/rpmbuild/SOURCES/gluster-nagios*
rm -fr ~/rpmbuild/BUILD/gluster-nagios*
rm -fr ~/rpmbuild/BUILDROOT/gluster-nagios*
rm -fr gluster-nagios-1.1

mv gluster-nagios-1.1.tar.gz ~/rpmbuild/SOURCES

echo "Clean rpmbuild directories"
rm -fr ~/rpmbuild/RPMS/noarch/*
rm -fr ~/rpmbuild/RPMS/x86_64/*

echo "Building rpm"
rpmbuild -ba gluster_nrpe.spec
rpmbuild -ba server/pnp4nagios/gluster_nagios.spec
