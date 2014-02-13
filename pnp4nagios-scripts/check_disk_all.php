<?php
#
# set graph labels
$i = 0;
$k = 0;
foreach ($this->DS as $KEY=>$VAL) {
  if ($i == 0) {
    $ds_name[$KEY] = str_replace("_","/",$VAL['NAME']);
    # set graph labels
    $opt[$KEY]     = "--title \"File System $ds_name[$KEY]\" ";
    # Graph Definitions
    $def[$KEY]     = rrd::def( "var1", $VAL['RRDFILE'], $VAL['DS'], "AVERAGE" ); 

    if ($VAL['MAX'] != "") {
      $def[$KEY] .= rrd::hrule( $VAL['MAX'], "#003300", "Max size $MAX[1] \\n");
    }
    # create warning line and legend
    if ($VAL['WARN'] != "") {
      $def[$KEY] .= rrd::hrule( $VAL['WARN'], "#FFFF00", "Warning on $WARN[1] \\n");
    }
    #create critical line and legend
    if ($VAL['CRIT'] != "") {
      $def[$KEY] .= rrd::hrule( $VAL['CRIT'], "#FF0000", "Critical on $CRIT[1]\\n");
    }

  if ($VAL['ACT'] >= $VAL['CRIT']) {
    $def[$KEY] .= rrd::gradient( "var1", "#A9F5F2", "#FF0000", "Disk Usage%");
  } elseif ($VAL['ACT'] >= $VAL['WARN']) {
      $def[$KEY] .= rrd::gradient( "var1", "#A9F5F2", "#FFFF00", "Disk Usage%");
  }else {
    $def[$KEY] .= rrd::gradient( "var1", "#00FFFF", "#4000FF", "Disk Usage%");
  }
    $i = 1;
    $k = $KEY;
  }
  else {
    $def[$k]    .= rrd::def( "var2", $VAL['RRDFILE'], $VAL['DS'], "AVERAGE" );
    if ($VAL['ACT'] >= $VAL['CRIT']) {
      $def[$k]    .= rrd::line1( "var2", "#FF0040", "Inode Usage\\n" );
    } elseif ($VAL['ACT'] >= $VAL['WARN']) {
      $def[$k]    .= rrd::line1( "var2", "#DBA901", "Inode Usage\\n" );
    }else {
      $def[$k]    .= rrd::line1( "var2", "#088A29", "Inode Usage\\n" );
    }
    $i = 0;
  }
}

?>
