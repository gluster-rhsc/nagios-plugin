1;3406;0c<?php
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
$upper_limit = round($MAX[1] / (1048576),2);
$opt[1] = "-X 0 --vertical-label \"$UNIT[1](Total:$upper_limit GB)\" -l 0 -r -u $upper_limit --title \"Swap usage $hostname / $servicedesc\" ";
$ds_name[1] = "Swap Usage";
$def[1] = "DEF:used_swap_in=$RRDFILE[1]:$DS[1]:AVERAGE " ;

$def[1] .= rrd::cdef("used_swap_out","used_swap_in,1048576,/");
$def[1] .= "AREA:used_swap_out#3D1AA8:\"Used \" ";
$def[1] .= "GPRINT:used_swap_out:LAST:\"%3.2lf GB LAST \" ";
$def[1] .= "GPRINT:used_swap_out:MAX:\"%3.2lf GB MAX \" ";
$def[1] .= "GPRINT:used_swap_out" . ':AVERAGE:"%3.2lf GB AVERAGE \j" ';

if ($WARN[1] != ""){
  $WAR = $WARN[1] / 1048576 ;
  $def[1] .= "LINE2:$WAR#FFA500:\"Warning       \\n\" ";
}
if ($CRIT[1] != "") {
  $CRT = $CRIT[1] / 1048576 ;
  $def[1] .= "LINE2:$CRT#FF0000:\"Critical \\n\" ";
}


?>