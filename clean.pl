#!/usr/bin/perl

use warnings;
use strict;

open INPUT, "<", "roast01.txt" or die "Could not open input file\n";
my @lines = <INPUT>;
close INPUT;

open OUTPUT, ">", "roast01.csv" or die "Could not open output file\n";

foreach my $line (@lines){
  $line =~ s/^\s+//;
  $line =~ s/\s+$//;

  if($line =~ m/^\s*$/){
    next;
  }
  elsif($line =~ m/^\[\d\d\/\d\d\/\d\d\d\d \d\d:\d\d:\d\d\] -/){
    print OUTPUT "$line\n";
  }
  elsif($line =~ m/^\[\d\d\/\d\d\/\d\d\d\d \d\d:\d\d:\d\d\] (Read|Written) data$/){
    print OUTPUT "$1,";
  }
  else{
    my($a,$b,$c,$d,$e,$f,$g,$h,$i,$j,$k,$l,$m,$n,$o) = split(" ", $line);
    print OUTPUT "$a,$b,$c,$d,$e,$f,$g,$h,$i,$j,$k,$l,$m,$n\n";
  }
}

close OUTPUT;
