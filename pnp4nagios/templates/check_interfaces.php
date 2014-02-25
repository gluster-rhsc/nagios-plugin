B1;3406;0cB1;3406;0c<?php
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

$VALUE_COUNT = 4;

$name = $NAME;
asort($name);
$c = count($name);
if ($c % $VALUE_COUNT != 0) {
    exit;
}

$interface_count = $c / $VALUE_COUNT;

for ($i = 0; $i < $interface_count; $i++) {
    $index = ($i * $VALUE_COUNT) + 1;

    list ($interface, $data_type) = explode (".", $name[$index+2]);
    $interface = str_replace(";","",$interface);
    $opt[$index+1] = "--vertical-label \"Speed in MB/s\" -X 0 -l 0 -u 128  -r --title \"Network Interface Load for $hostname / $interface\" ";

    $ds_name[$index+1] = "$interface:: Receiving and ";
    $def[$index+1]  = rrd::def ($interface . $data_type, $RRDFILE[$index+2], $DS[$index+2], "AVERAGE");
    $def[$index+1] .= rrd::line1($interface . $data_type, "#008000", $data_type);
    $def[$index+1] .= rrd::gprint ($interface . $data_type, array("LAST", "AVERAGE", "MAX"), "%10.4lf MB/s");

    list ($interface, $data_type) = explode (".", $name[$index+3]);
    $interface = str_replace(";","",$interface);
    $ds_name[$index+1] .= "Transmission speed";
    $def[$index+1] .= rrd::def ($interface . $data_type, $RRDFILE[$index+3], $DS[$index+3], "AVERAGE");
    $def[$index+1] .= rrd::line1 ($interface . $data_type, "#0000ff", $data_type) ;
    $def[$index+1] .= rrd::gprint ($interface . $data_type, array("LAST", "AVERAGE", "MAX"), "%10.4lf MB/s");
}
?>
