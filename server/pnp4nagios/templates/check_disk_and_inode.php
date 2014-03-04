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

#
# set graph labels
$i = 0;
$k = 0;
foreach ($this->DS as $KEY=>$VAL) {
  if ($i == 0) {
    $VAL['NAME'] = str_replace("_","/",$VAL['NAME']);
    $ds_name[$KEY] = "Disk Utilization";
    $name[$KEY] = "Disk Utilization for mount: " . $VAL['NAME'];
     
    # set graph labels
    $opt[$KEY]     = "--vertical-label \"% Usage\" --lower-limit 0 --upper-limit 100 --title \"$name[$KEY]\" ";
    # Graph Definitions
    $def[$KEY]     = rrd::def( "var1", $VAL['RRDFILE'], $VAL['DS'], "AVERAGE" ); 

    # disk graph rendering
    if ($VAL['ACT'] >= $VAL['CRIT']) {
     $def[$KEY]    .= rrd::line1( "var1", "#008000", "Disk Usage" );
    } elseif ($VAL['ACT'] >= $VAL['WARN']) {
      $def[$KEY]    .= rrd::line1( "var1", "#008000", "Disk Usage" );
    }else {
      $def[$KEY]    .= rrd::line1( "var1", "#008000", "Disk Usage" );
    }
    $def[$KEY] .= rrd::gprint  ("var1", array("LAST","MAX","AVERAGE"), "%3.4lf %S%%");
    $i = 1;
    $k = $KEY;
  }
  else {
    # inode graph rendering
    $def[$k]    .= rrd::def( "var2", $VAL['RRDFILE'], $VAL['DS'], "AVERAGE" );
    if ($VAL['ACT'] >= $VAL['CRIT']) {
      $def[$k]    .= rrd::line1( "var2", "#0000FF", "Inode Usage" );
    } elseif ($VAL['ACT'] >= $VAL['WARN']) {
      $def[$k]    .= rrd::line1( "var2", "#0000FF", "Inode Usage" );
    }else {
      $def[$k]    .= rrd::line1( "var2", "#0000FF", "Inode Usage" );
    }
    $def[$k] .= rrd::gprint  ("var2", array("LAST","MAX","AVERAGE"), "%3.4lf %S%%");
    $i = 0;

    # create warning line and legend
    $def[$k] .= rrd::line2( $VAL['WARN'], "#FFA500", "Warning\\n");

    # create critical line and legend
    $def[$k] .= rrd::line2( $VAL['CRIT'], "#FF0000", "Critical\\n");

  }
}
?>
