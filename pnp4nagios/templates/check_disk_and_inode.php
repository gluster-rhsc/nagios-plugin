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
    $ds_name[$KEY] = str_replace("_","/",$VAL['NAME']);
    # set graph labels
    $opt[$KEY]     = "--lower-limit 0 --upper-limit 100 --title \"Logical Volume: $ds_name[$KEY]\" ";
    # Graph Definitions
    $def[$KEY]     = rrd::def( "var1", $VAL['RRDFILE'], $VAL['DS'], "AVERAGE" ); 

    # create warning line and legend
    if ($VAL['WARN'] != "") {
      $def[$KEY] .= rrd::hrule( $VAL['WARN'], "#FFA500", "Warning Level \\n");
    }
    # create critical line and legend
    if ($VAL['CRIT'] != "") {
      $def[$KEY] .= rrd::hrule( $VAL['CRIT'], "#FF0000", "Critical Level\\n");
    }

  # disk graph rendering
  if ($VAL['ACT'] >= $VAL['CRIT']) {
    $def[$KEY]    .= rrd::line1( "var1", "#000000", "Disk Usage\\n" );
  } elseif ($VAL['ACT'] >= $VAL['WARN']) {
    $def[$KEY]    .= rrd::line1( "var1", "#000000", "Disk Usage\\n" );
  }else {
    $def[$KEY]    .= rrd::line1( "var1", "#000000", "Disk Usage\\n" );
  }
    $i = 1;
    $k = $KEY;
  }
  else {
    # inode graph rendering
    $def[$k]    .= rrd::def( "var2", $VAL['RRDFILE'], $VAL['DS'], "AVERAGE" );
    if ($VAL['ACT'] >= $VAL['CRIT']) {
      $def[$k]    .= rrd::line1( "var2", "#0000FF", "Inode Usage\\n" );
    } elseif ($VAL['ACT'] >= $VAL['WARN']) {
      $def[$k]    .= rrd::line1( "var2", "#0000FF", "Inode Usage\\n" );
    }else {
      $def[$k]    .= rrd::line1( "var2", "#0000FF", "Inode Usage\\n" );
    }
    $i = 0;
  }
}

?>
