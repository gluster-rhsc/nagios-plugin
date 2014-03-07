#===============================================================================
# Copyright 2014 Red Hat
# Name: gluster-nrpe-plugin.spec 
#-------------------------------------------------------------------------------
# Purpose: RPM Spec file for installing gluster nrpe plugins
# Version 1.00:13 Feb 2014 Created.
#===============================================================================

%define  debug_package %{nil}

Name:                   gluster-nrpe
Version:                1.1
Release:                1
Summary:                gluster nrpe plugins for nodes
Group:                  System Environment/Base
License:                GPLv2+
URL:                    http://www.redhat.com/
BuildRoot:              %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:                gluster-nrpe.tar.gz


Requires: nrpe
Requires: sysstat

%description
Gluster nrpe plugins script for monitoring disk, network, cup and memory
details and configure nrpe to work with nagios server.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/usr/lib64/nagios/plugins/gluster
cp sadf.py %{buildroot}/usr/lib64/nagios/plugins/gluster
cp check_disk_and_inode.py %{buildroot}/usr/lib64/nagios/plugins/gluster

%clean
rm -rf %{buildroot}

%post
if [ $1 == 1 ]; then
/sbin/iptables -A INPUT -p tcp --dport 5666 -j ACCEPT
/sbin/iptables-save

sed -i 's/10 \* \* \* \* root \/usr\/lib64\/sa\/sa1/1 \* \* \* \* root \/usr\/lib64\/sa\/sa1/g' /etc/cron.d/sysstat

cat >> /etc/nagios/nrpe.cfg <<EOF
### gluster nrpe plugins ###
command[check_disk_and_inode]=/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.py -w 80 -c 90 -l -i /boot -i /var -i /root -n
command[check_memory]=/usr/lib64/nagios/plugins/gluster/sadf.py -m -w 80 -c 90
command[check_swap_usage]=/usr/lib64/nagios/plugins/gluster/sadf.py -s -w 80 -c 90
command[check_cpu_multicore]=/usr/lib64/nagios/plugins/gluster/sadf.py -cp -w 80 -c 90
command[check_interfaces]=/usr/lib64/nagios/plugins/gluster/sadf.py -n -e lo
EOF
fi

%if 0%{?rhel} == 6
 /sbin/chkconfig nrpe on
 /sbin/service iptables restart >/dev/null 2>&1
 /sbin/service crond restart >/dev/null 2>&1
%endif



%preun
if [ $1 = 0 ]; then
    sed -i '/gluster nrpe plugins/d' /etc/nagios/nrpe.cfg
    sed -i '/check_disk_and_inode/d' /etc/nagios/nrpe.cfg
    sed -i '/check_memory/d' /etc/nagios/nrpe.cfg
    sed -i '/check_swap_usage/d' /etc/nagios/nrpe.cfg
    sed -i '/sadf.py/d' /etc/nagios/nrpe.cfg
    sed -i '/check_cpu_multicore.py/d' /etc/nagios/nrpe.cfg
fi


%files
%defattr(-,root,root,-)
/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.py
/usr/lib64/nagios/plugins/gluster/sadf.py


%changelog
* Thu Feb 13 2014 Timothy Asir Jeyasingh <tjeyasin@redhat.com>
- Initial release
