#!/usr/bin/perl

#@fluxfiles = `find /Users/katescholberg/Documents/snreview/cimreview/huedepohl -name "s*" `;

open (INFILES,"infiles.dat");

while(<INFILES>) {

  chop($_);
#  print $_;
  $fluxfile = $_;
  print $fluxfile,"\n";

 $command =  "root -b -q \'make_2d_fluxes.C(\"/Users/rishigundakaram/projects/SURF2020/snowglobes/ternary_plot/fluxdb/\",\"Huedepohl\",\"".$fluxfile."\"".",0)\'";

  print $command,"\n";

  system($command);
}


