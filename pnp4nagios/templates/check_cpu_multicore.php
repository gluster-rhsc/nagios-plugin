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

# Graph Total CPU usage (average across all cpu cores)
$def[1]=""; $opt[1]=""; $ds_name[1]="";
$opt[1] = "--vertical-label \"CPU Percent\" -l 0 --title \"CPU for $hostname / $servicedesc\" --slope-mode -u 100 -N";
$ds_name[1] = "CPU Utilization - Average across all cores";

$def[1]  = "DEF:total_cpu_in=$RRDFILE[1]:$DS[2]:AVERAGE " ;
$def[1] .= "DEF:system_cpu_in=$RRDFILE[1]:$DS[3]:AVERAGE " ;
$def[1] .= "DEF:user_cpu_in=$RRDFILE[1]:$DS[4]:AVERAGE " ;
$def[1] .= "DEF:idle_cpu_in=$RRDFILE[1]:$DS[5]:AVERAGE " ;

$def[1] .= "CDEF:user_cpu_out=user_cpu_in ";
$def[1] .= "AREA:user_cpu_out#ADD8E6:\"User\t\t\" ";
$def[1]  .= rrd::gprint("user_cpu_out", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

$def[1] .= rrd::cdef("system_cpu_out", "system_cpu_in");
$def[1] .= "STACK:system_cpu_out#6CBB3C:\"System\t\" ";
$def[1]  .= rrd::gprint("system_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

$def[1] .= rrd::cdef("total_cpu_out", "total_cpu_in,user_cpu_in,-,system_cpu_in,-");
$def[1] .= "STACK:total_cpu_out#D462FF:\"Total\t\t\" ";
$def[1]  .= rrd::gprint("total_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

$def[1] .= "CDEF:idle_cpu_out=idle_cpu_in ";
$def[1] .= "STACK:idle_cpu_out#C0C0C0:\"Idle\t\t\" ";
$def[1]  .= rrd::gprint("idle_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

if ($WARN[2] != ""){
  $def[1] .= "LINE2:$WARN[2]#FFA500:\"Warning   \" ";
}
if ($CRIT[2] != ""){              
  $def[1] .= "LINE2:$CRIT[2]#FF0000:\"Critical  \" ";
}

# Graph Per-Core CPU usage
$def_n=2;
$index = 6;
$no_cpu=$ACT[1];

if($no_cpu>1)

for( $cpu_n=0; $cpu_n<$no_cpu; $cpu_n++) {
    $def[$def_n]='';
    $ds_name[$def_n] = "CPU Utlilization for core: $cpu_n";
    $opt[$def_n] = "--vertical-label \"CPU Percent \" -l 0 --title \"CPU for $hostname / $servicedesc\" --slope-mode -u 100 -N";
    
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
    $def[$def_n] .= "AREA:user_cpu_out#ADD8E6:\"User\t\t\" ";
    $def[$def_n]  .= rrd::gprint("user_cpu_out", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

    $def[$def_n] .= rrd::cdef("system_cpu_out", "system_cpu_in");
    $def[$def_n] .= "STACK:system_cpu_out#6CBB3C:\"System\t\" ";
    $def[$def_n]  .= rrd::gprint("system_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

    $def[$def_n] .= rrd::cdef("total_cpu_out", "total_cpu_in,user_cpu_in,-,system_cpu_in,-");
    $def[$def_n] .= "STACK:total_cpu_out#D462FF:\"Total\t\t\" ";
    $def[$def_n]  .= rrd::gprint("total_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

    $def[$def_n] .= "CDEF:idle_cpu_out=idle_cpu_in ";
    $def[$def_n] .= "STACK:idle_cpu_out#C0C0C0:\"Idle\t\t\" ";
    $def[$def_n]  .= rrd::gprint("idle_cpu_in", array("LAST", "AVERAGE", "MAX"), "%6.2lf%%");

    if ($WARN[$index_of_threshold_val] != ""){
        $def[$def_n] .= "LINE2:$WARN[$index_of_threshold_val]#FFFF00:\"Warning   \" ";
    }
    if ($CRIT[$index_of_threshold_val] != ""){              
        $def[$def_n] .= "LINE2:$CRIT[$index_of_threshold_val]#FF0000:\"Critical  \" ";
    }
    $def_n++;
}
?>
