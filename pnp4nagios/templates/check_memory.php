<?php
#                                                                                                                         
# Plugin: check_nrpe_cpu_core_stat                                                                                        
# pst                                                                                                                     
#                                                                                                                         
#
$def[1]=""; $opt[1]=""; $ds_name[1]="";
$opt[1] = "--vertical-label \"$UNIT[1]\"  -l 0 -u $MAX[1]   --title \"Memory usage for $hostname / $servicedesc\" --slope-mode -N";
$ds_name[1] = "Memory utilization";



$def[1]  = "DEF:total_mem_in=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:used_mem_in=$RRDFILE[1]:$DS[2]:AVERAGE " ;
$def[1] .= "DEF:buffer_mem_in=$RRDFILE[1]:$DS[3]:AVERAGE " ;
$def[1] .= "DEF:cached_mem_in=$RRDFILE[1]:$DS[4]:AVERAGE " ;

$def[1] .= "CDEF:total_mem_out=total_mem_in ";
$def[1] .= "AREA:total_mem_out#BCF5FD:\"Total       \" ";
$def[1] .= "GPRINT:total_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:total_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:total_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

$def[1] .= "CDEF:used_mem_out=used_mem_in ";
$def[1] .= "AREA:used_mem_out#DD86F5:\"Used        \" ";
$def[1] .= "GPRINT:used_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:used_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:used_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

$def[1] .= "CDEF:buffer_mem_out=buffer_mem_in ";
$def[1] .= "AREA:buffer_mem_out#2B62FA:\"Buffer      \" ";
$def[1] .= "GPRINT:buffer_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:buffer_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:buffer_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

$def[1] .= "CDEF:cached_mem_out=cached_mem_in ";
$def[1] .= "LINE1:cached_mem_out#2FFF00:\"Cached      \" ";
$def[1] .= "GPRINT:cached_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:cached_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:cached_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

if ($WARN[1] != ""){
  $def[1] .= "LINE1:$WARN[1]#FFFF00:\"Warning            \" ";
}
if ($CRIT[1] != "") {
  $def[1] .= "LINE1:$CRIT[1]#FF0000:\" Critical  \\n\" ";
  }

?>