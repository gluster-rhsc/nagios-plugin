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


%description
Gluster nrpe plugins script for monitoring disk, network, cup and memory
details and configure nrpe to work with nagios server.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/usr/lib64/nagios/plugins/gluster
cp check_cpu_multicore.py %{buildroot}/usr/lib64/nagios/plugins/gluster
cp check_memory.py %{buildroot}/usr/lib64/nagios/plugins/gluster
cp check_swap_usage.py %{buildroot}/usr/lib64/nagios/plugins/gluster
cp sadf.py %{buildroot}/usr/lib64/nagios/plugins/gluster
cp check_disk_and_inode.py %{buildroot}/usr/lib64/nagios/plugins/gluster

%clean
rm -rf %{buildroot}

%post
if [ $1 == 1 ]; then
cat >> /etc/nagios/nrpe.cfg <<EOF
### gluster nrpe plugins ###
command[check_disk_and_inode]=/usr/lib64/nagios/plugins/check_disk_and_inode.py -w 20 -c 10
command[check_memory]=/usr/lib64/nagios/plugins/check_memory.py -w 70 -c 85
command[check_swap_usage]=/usr/lib64/nagios/plugins/check_swap_usage.py -w 30 -c 15
command[check_cpu_multicore]=/usr/lib64/nagios/plugins/check_cpu_multicore.py -w 80 -c 90
command[check_interfaces]=/usr/lib64/nagios/plugins/sadf.py net
EOF
fi


%preun
if [ $1 = 0 ]; then
    sed -i '/gluster nrpe plugins/d' /etc/nagios/nrpe.cfg
    sed -i '/check_disk_and_inode/d' /etc/nagios/nrpe.cfg
    sed -i '/check_memory/d' /etc/nagios/nrpe.cfg
    sed -i '/check_swap_usage/d' /etc/nagios/nrpe.cfg
    sed -i '/sadf.py/d' /etc/nagios/nrpe.cfg
    sed -i '/check_cpu_multicore.py/d' /etc/nagios/nrpe.cfg
fi


%posttrans
/sbin/service nrpe condrestart >/dev/null 2>&1


%files
%defattr(-,root,root,-)
/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.py
/usr/lib64/nagios/plugins/gluster/check_cpu_multicore.py
/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.py
/usr/lib64/nagios/plugins/gluster/check_memory.py
/usr/lib64/nagios/plugins/gluster/check_swap_usage.py
/usr/lib64/nagios/plugins/gluster/sadf.py
/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.pyc
/usr/lib64/nagios/plugins/gluster/check_cpu_multicore.pyc
/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.pyc
/usr/lib64/nagios/plugins/gluster/check_memory.pyc
/usr/lib64/nagios/plugins/gluster/check_swap_usage.pyc
/usr/lib64/nagios/plugins/gluster/sadf.pyc
/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.pyo
/usr/lib64/nagios/plugins/gluster/check_cpu_multicore.pyo
/usr/lib64/nagios/plugins/gluster/check_disk_and_inode.pyo
/usr/lib64/nagios/plugins/gluster/check_memory.pyo
/usr/lib64/nagios/plugins/gluster/check_swap_usage.pyo
/usr/lib64/nagios/plugins/gluster/sadf.pyo


%changelog
* Thu Feb 13 2014 Timothy Asir Jeyasingh <tjeyasin@redhat.com>
- Initial release
