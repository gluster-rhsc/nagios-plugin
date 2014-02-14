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

%description
Gluster nagios plugins and pnp4nagios templates for monitoring disk,
network, cpu, memory and etc.,

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}/usr/local/pnp4nagios/share/templates.dist
cp check_cpu_multicore.php %{buildroot}/usr/local/pnp4nagios/share/templates.dist
cp check_disk_and_inode.php %{buildroot}/usr/local/pnp4nagios/share/templates.dist
cp check_interfaces.php %{buildroot}/usr/local/pnp4nagios/share/templates.dist
cp check_memory.php %{buildroot}/usr/local/pnp4nagios/share/templates.dist
cp check_swap_usage.php %{buildroot}/usr/local/pnp4nagios/share/templates.dist

%clean
rm -rf %{buildroot}

%post
if [ $1 == 1 ]; then
CommandFile="/etc/nagios/objects/commands.cfg"
if ! grep -q "gluster nagios template" $CommandFile; then
cat >> $CommandFile <<EOF

### gluster nagios template ###
define command {
       command_name check_disk_and_inode
       command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_disk_and_inode
}

define command {
command_name check_cpu_multicore
command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_cpu_multicore
}

define command {
       command_name check_memory
       command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_memory
}

define command {
       command_name check_swap_usage
       command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_swap_usage
}

define command {
       command_name check_interfaces
       command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_interfaces
}
EOF
fi
fi

%files
%defattr(-, root, root, -)
/usr/local/pnp4nagios/share/templates.dist/check_cpu_multicore.php
/usr/local/pnp4nagios/share/templates.dist/check_disk_and_inode.php
/usr/local/pnp4nagios/share/templates.dist/check_interfaces.php
/usr/local/pnp4nagios/share/templates.dist/check_memory.php
/usr/local/pnp4nagios/share/templates.dist/check_swap_usage.php


%changelog
* Thu Feb 13 2014 Timothy Asir Jeyasingh <tjeyasin@redhat.com>
- Initial release
