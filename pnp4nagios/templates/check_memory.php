<?php
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
$def[1]=""; $opt[1]=""; $ds_name[1]="";
$opt[1] = "--vertical-label \"$UNIT[1]\"  -l 0 -u $MAX[1]   --title \"Memory usage for $hostname / $servicedesc\" --slope-mode -N";
$ds_name[1] = "Memory utilization";



$def[1]  = "DEF:total_mem_in=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:used_mem_in=$RRDFILE[1]:$DS[2]:AVERAGE " ;
$def[1] .= "DEF:buffer_mem_in=$RRDFILE[1]:$DS[3]:AVERAGE " ;
$def[1] .= "DEF:cached_mem_in=$RRDFILE[1]:$DS[4]:AVERAGE " ;

$def[1] .= "CDEF:total_mem_out=total_mem_in ";
$def[1] .= "LINE2:total_mem_out#000000:\"Total       \" ";
$def[1] .= "GPRINT:total_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:total_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:total_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

$def[1] .= "CDEF:used_mem_out=used_mem_in ";
$def[1] .= "LINE2:used_mem_out#0000ff:\"Used        \" ";
$def[1] .= "GPRINT:used_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:used_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:used_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

$def[1] .= "CDEF:buffer_mem_out=buffer_mem_in ";
$def[1] .= "LINE2:buffer_mem_out#008000:\"Buffer      \" ";
$def[1] .= "GPRINT:buffer_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:buffer_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:buffer_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

$def[1] .= "CDEF:cached_mem_out=cached_mem_in ";
$def[1] .= "LINE2:cached_mem_out#800080:\"Cached      \" ";
$def[1] .= "GPRINT:cached_mem_in:LAST:\"%10.2lf %s$UNIT[1] LAST \" ";
$def[1] .= "GPRINT:cached_mem_in:MAX:\"%10.2lf %s$UNIT[1] MAX \" ";
$def[1] .= "GPRINT:cached_mem_in" . ':AVERAGE:"%10.2lf %sGB AVERAGE \j" ';

if ($WARN[1] != ""){
  $def[1] .= "LINE2:$WARN[1]#FFA500:\"Warning            \" ";
}
if ($CRIT[1] != "") {
  $def[1] .= "LINE2:$CRIT[1]#FF0000:\" Critical  \\n\" ";
  }

?>