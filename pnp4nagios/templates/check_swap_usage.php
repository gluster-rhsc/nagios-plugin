<?php
#                                                                                                                         
# Template for check_swap                                                                                                 
# Copyright (c) 2006-2010 Joerg Linge (http://www.pnp4nagios.org)                                                         
#                                                                                                                         
# RRDtool Options                                                                                                         
$opt[1] = "-X 0 --vertical-label $UNIT[1] -l 0 -u $MAX[1] --title \"Swap usage $hostname / $servicedesc\" ";
#                                                                                                                         
#                                                                                                                         
# Graphen Definitions                                                                                                     
$def[1]  = "DEF:free_swap_in=$RRDFILE[1]:$DS[1]:AVERAGE " ;
if ($MAX[1] != "") {
  $def[1] .= "AREA:$MAX[1]#F7C3C7:\"Total            $MAX[1] GB \\n\" ";
}

$def[1] .= rrd::cdef("total_swap", "$MAX[1],free_swap_in,-,free_swap_in,+");
$def[1] .= rrd::cdef("used_swap_out", "$MAX[1],free_swap_in,-");

if ($WARN[1] != "") {
  $def[1] .= rrd::cdef("warn", "total_swap,$WARN[1],-");
  $def[1] .= "LINE1:warn#ffff00:\"Warning        \" ";
}
if ($CRIT[1] != "") {
  $def[1] .= rrd::cdef("crit", "total_swap,$CRIT[1],-");
  $def[1] .= "LINE1:crit#ff0000:\"Critical \\n\" ";
}

$def[1] .= "AREA:used_swap_out#3D1AA8:\"Used        \" ";
$def[1] .= "GPRINT:used_swap_out:LAST:\"%3.2lf %sGB LAST \" ";
$def[1] .= "GPRINT:used_swap_out:MAX:\"%3.2lf %sGB MAX \" ";
$def[1] .= "GPRINT:used_swap_out" . ':AVERAGE:"%3.2lf %sGB AVERAGE \j" ';

?>
