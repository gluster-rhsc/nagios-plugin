#===============================================================================
# Copyright 2014 Red Hat
# Name: gluster-nagios-plugin.spec 
#-------------------------------------------------------------------------------
# Purpose: RPM Spec file for installing and seting up nagios server
# Version 1.00:13 Feb 2014 Created.
#===============================================================================

%define  debug_package %{nil}

%define name      gluster-nagios
%define summary   gluster-nagios
%define version   1.1
%define release   1
%define license   GPLv2+
%define group     Applications/System
%define source    %{name}-%{version}.tar.gz
%define url       http://www.redhat.com
%define buildroot %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Name:      %{name}
Summary:   %{summary}
Version:   %{version}
Release:   %{release}
License:   %{license}
Group:     %{group}
Source0:   %{source}
BuildArch: noarch
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

Requires: rrdtool-perl
Requires: nagios
Requires: nagios-plugins-nrpe
Requires: php
Requires: httpd
Requires: pnp4nagios
Requires: check-mk-livestatus
Requires: nagios-plugins-all

%description
Gluster nagios plugins and pnp4nagios templates for monitoring disk,
network, cpu, memory and etc.,

%prep
%setup -q

%build

%install
rm -fr %{buildroot}/etc/nagios/gluster
rm -fr %{buildroot}/usr/lib64/nagios/plugins/eventhandlers
mkdir -p %{buildroot}/usr/lib64/nagios/plugins/eventhandlers
mkdir -p %{buildroot}/usr/share/nagios/html/pnp4nagios/templates.dist
mkdir -p %{buildroot}/etc/nagios/gluster/Default
cp -a check_cpu_multicore.php  %{buildroot}/usr/share/nagios/html/pnp4nagios/templates.dist
cp -a check_disk_and_inode.php  %{buildroot}/usr/share/nagios/html/pnp4nagios/templates.dist
cp -a check_interfaces.php  %{buildroot}/usr/share/nagios/html/pnp4nagios/templates.dist
cp -a check_memory.php  %{buildroot}/usr/share/nagios/html/pnp4nagios/templates.dist
cp -a check_swap_usage.php  %{buildroot}/usr/share/nagios/html/pnp4nagios/templates.dist
cp -a gluster-commands.cfg %{buildroot}/etc/nagios/gluster
cp -a gluster-host-groups.cfg %{buildroot}/etc/nagios/gluster
cp -a gluster-host-services.cfg %{buildroot}/etc/nagios/gluster
cp -a gluster-templates.cfg %{buildroot}/etc/nagios/gluster
cp -a node1.cfg %{buildroot}/etc/nagios/gluster/Default
cp -a check_remote_host.py %{buildroot}/usr/lib64/nagios/plugins
cp -a gluster_host_service_handler.py %{buildroot}/usr/lib64/nagios/plugins/eventhandlers


%clean
rm -rf %{buildroot}

%post
if [ $1 == 1 ]; then

NagiosCFGFile="/etc/nagios/nagios.cfg"
sed -i '/etc\/nagios\/objects\/localhost.cfg/d' $NagiosCFGFile

/sbin/iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT

if grep -q "#process_performance_data=0" $NagiosCFGFile; then
  sed -i -e 's/#process_performance_data=0/process_performance_data=1/g' $NagiosCFGFile
elif grep -q "process_performance_data=0" $NagiosCFGFile ; then
  sed -i -e 's/process_performance_data=0/process_performance_data=1/g' $NagiosCFGFile
fi


if grep -q "#enable_environment_macros=0" $NagiosCFGFile; then
  sed -i -e 's/#enable_environment_macros=0/enable_environment_macros=1/g' $NagiosCFGFile   
elif grep -q "process_performance_data=0" $NagiosCFGFile ; then
  sed -i -e 's/process_performance_data=0/process_performance_data=1/g' $NagiosCFGFile
fi

/sbin/service iptables save

if ! grep -q "#rhs performance monitoring" $NagiosCFGFile; then
cat >> $NagiosCFGFile <<EOF
#rhs performance monitoring

# Definitions specific to gluster
cfg_dir=/etc/nagios/gluster

service_perfdata_command=process-service-perfdata
host_perfdata_command=process-host-perfdata
broker_module=/usr/lib64/check_mk/livestatus.o /var/spool/nagios/cmd/live
EOF
fi

CommandFile="/etc/nagios/objects/commands.cfg"
if [ -f $CommandFile ]; then
sed -i -e "/# 'process-host-perfdata' command definition/,+5d" $CommandFile
sed -i -e "/# 'process-service-perfdata' command definition/,+5d" $CommandFile

if ! grep -q "check_nrpe" $CommandFile; then
cat >> $CommandFile <<EOF
define command{
       command_name check_nrpe
       command_line \$USER1\$/check_nrpe -H \$HOSTADDRESS\$ -c \$ARG1\$
}
EOF
fi

if ! grep -q "gluster nagios template" $CommandFile; then
cat >> $CommandFile <<EOF

### gluster nagios template ###
define command {
       command_name    process-service-perfdata
       command_line    /usr/bin/perl /usr/libexec/pnp4nagios/process_perfdata.pl
}

define command {
       command_name    process-host-perfdata
       command_line    /usr/bin/perl /usr/libexec/pnp4nagios/process_perfdata.pl -d HOSTPERFDATA
}

EOF
fi
fi
fi


%if 0%{?rhel} == 6
 /sbin/chkconfig nagios on
 /sbin/chkconfig httpd on
 /sbin/service iptables restart >/dev/null 2>&1
 /sbin/service nagios start >/dev/null 2>&1
 /sbin/service httpd start >/dev/null 2>&1
%endif

%files
%defattr(-, root, root, -)
/usr/share/nagios/html/pnp4nagios/templates.dist/check_cpu_multicore.php
/usr/share/nagios/html/pnp4nagios/templates.dist/check_disk_and_inode.php
/usr/share/nagios/html/pnp4nagios/templates.dist/check_interfaces.php
/usr/share/nagios/html/pnp4nagios/templates.dist/check_memory.php
/usr/share/nagios/html/pnp4nagios/templates.dist/check_swap_usage.php
/etc/nagios/gluster/gluster-commands.cfg
/etc/nagios/gluster/gluster-host-groups.cfg
/etc/nagios/gluster/gluster-host-services.cfg
/etc/nagios/gluster/gluster-templates.cfg
/etc/nagios/gluster/Default/node1.cfg
/usr/lib64/nagios/plugins/check_remote_host.py
/usr/lib64/nagios/plugins/eventhandlers/gluster_host_service_handler.py

%changelog
* Thu Feb 13 2014 Timothy Asir Jeyasingh <tjeyasin@redhat.com>
- Initial release
