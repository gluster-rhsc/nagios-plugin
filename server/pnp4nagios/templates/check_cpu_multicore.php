<?php
############################################################################
# Author: Nishanth Thomas                    e-mail:  nthomas@redhat.com   #
############################################################################
# PNP4Nagios Template: check_cpu_multicore.php   (this file)               #
# For Nagios Plugin:   check_cpu_multicore.py                              #
#                                                                          #
# This will plot graphs for:                                               #
# A graph for average CPU utilization across all cores                     #
# Separate graphs for CPU utilization for each cores                       #
#                                                                          #
############################################################################
#
# check_interfaces -- template to generate RRD graph
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

# Graph Total CPU usage (average across all cpu cores)
$def[1]=""; $opt[1]=""; $ds_name[1]="";
$opt[1] = "--vertical-label \"% Usage\" -r --lower-limit 0 --upper-limit 100 --title \"CPU for $hostname / $servicedesc\" --slope-mode -u 100 -N";
$ds_name[1] = "CPU Utilization - Average across all cores";

$def[1]  = "DEF:total_cpu_in=$RRDFILE[1]:$DS[2]:AVERAGE " ;
$def[1] .= "DEF:system_cpu_in=$RRDFILE[1]:$DS[3]:AVERAGE " ;
$def[1] .= "DEF:user_cpu_in=$RRDFILE[1]:$DS[4]:AVERAGE " ;

$def[1] .= "CDEF:user_cpu_out=user_cpu_in ";
$def[1] .= "LINE1:user_cpu_out#0000FF:\"User\t\t\" ";
$def[1]  .= rrd::gprint("user_cpu_out", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

$def[1] .= rrd::cdef("system_cpu_out", "system_cpu_in");
$def[1] .= "LINE1:system_cpu_out#008000:\"System\t\" ";
$def[1]  .= rrd::gprint("system_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

$def[1] .= rrd::cdef("total_cpu_out", "total_cpu_in");
$def[1] .= "LINE1:total_cpu_out#800080:\"Total\t\t\" ";
$def[1]  .= rrd::gprint("total_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

if ($WARN[2] != ""){
  $def[1] .= "LINE2:$WARN[2]#FFA500:\"Warning\\n\" ";
}
if ($CRIT[2] != ""){              
  $def[1] .= "LINE2:$CRIT[2]#FF0000:\"Critical\\n\" ";
}

# Graph Per-Core CPU usage
$def_n=2;
$index = 6;
$no_cpu=$ACT[1];

if($no_cpu>1)

for( $cpu_n=0; $cpu_n<$no_cpu; $cpu_n++) {
    $def[$def_n]='';
    $ds_name[$def_n] = "CPU Utlilization for core: $cpu_n";
    $opt[$def_n] = "--vertical-label \"% Usage\" --lower-limit 0 --upper-limit 100 --title \"CPU for $hostname / $servicedesc\" --slope-mode -N";
    
    $index_of_threshold_val = $index; 
    $def[$def_n]  = "DEF:total_cpu_in=$RRDFILE[$index]:$DS[$index]:AVERAGE " ;
    $index += 1;
    $def[$def_n] .= "DEF:system_cpu_in=$RRDFILE[$index]:$DS[$index]:AVERAGE " ;
    $index += 1;
    $def[$def_n] .= "DEF:user_cpu_in=$RRDFILE[$index]:$DS[$index]:AVERAGE " ;
    $index += 1;
    $def[$def_n] .= "DEF:idle_cpu_in=$RRDFILE[$index]:$DS[$index]:AVERAGE " ;
    $index += 1;

    $def[$def_n] .= "CDEF:user_cpu_out=user_cpu_in ";
    $def[$def_n] .= "LINE1:user_cpu_out#0000FF:\"User\t\t\" ";
    $def[$def_n]  .= rrd::gprint("user_cpu_out", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

    $def[$def_n] .= rrd::cdef("system_cpu_out", "system_cpu_in");
    $def[$def_n] .= "LINE1:system_cpu_out#008000:\"System\t\" ";
    $def[$def_n]  .= rrd::gprint("system_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

    $def[$def_n] .= rrd::cdef("total_cpu_out", "total_cpu_in");
    $def[$def_n] .= "LINE1:total_cpu_out#800079:\"Total\t\t\" ";
    $def[$def_n]  .= rrd::gprint("total_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

    if ($WARN[$index_of_threshold_val] != ""){
        $def[$def_n] .= "LINE2:$WARN[$index_of_threshold_val]#FFFF00:\"Warning\\n\" ";
    }
    if ($CRIT[$index_of_threshold_val] != ""){              
        $def[$def_n] .= "LINE2:$CRIT[$index_of_threshold_val]#FF0000:\"Critical\\n\" ";
    }
    $def_n++;
}
?>
