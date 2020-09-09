#!/opt/local/bin/perl
use warnings;
use strict;


use strict;
use warnings;

use File::Find;

find(sub {
  if (-f) {
    my $mtime = (stat _)[9];
    print "$mtime\n";
  }
}, '.');
