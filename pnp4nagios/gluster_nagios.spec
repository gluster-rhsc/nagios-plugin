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
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a * /usr/local/pnp4nagios/share/templates.dist

%clean
rm -rf %{buildroot}

%post
if [ $1 == 1 ]; then
cat >> /etc/nagios/objects/commands.cfg <<EOF

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

%files
%defattr(-, root, root, -)

%changelog
* Thu Feb 13 2014 Timothy Asir Jeyasing
- Initial release
