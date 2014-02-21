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

$opt[1] = "-X 0 --vertical-label $UNIT[1] -l 0 -u $MAX[1] --title \"Swap usage $hostname / $servicedesc\" ";

$def[1] = "DEF:used_swap_in=$RRDFILE[1]:$DS[1]:AVERAGE " ;
if ($MAX[1] != "") {
  $def[1] .= "AREA:$MAX[1]#ADD8E6:\"Free             \\n\" ";
  $def[1] .= "LINE2:$MAX[1]#000000:\"Total              $MAX[1] GB \\n\" ";
}

$def[1] .= "CDEF:used_swap_out=used_swap_in ";
$def[1] .= "AREA:used_swap_out#3D1AA8:\"Used \" ";
$def[1] .= "GPRINT:used_swap_out:LAST:\"%3.2lf %sGB LAST \" ";
$def[1] .= "GPRINT:used_swap_out:MAX:\"%3.2lf %sGB MAX \" ";
$def[1] .= "GPRINT:used_swap_out" . ':AVERAGE:"%3.2lf %sGB AVERAGE \j" ';

if ($WARN[1] != ""){
  $def[1] .= "LINE2:$WARN[1]#FFA500:\"Warning        \" ";
}
if ($CRIT[1] != "") {
  $def[1] .= "LINE2:$CRIT[1]#FF0000:\" Critical \\n\" ";
}


?>