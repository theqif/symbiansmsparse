#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;

use CGI::Carp qw/fatalsToBrowser/;

my $all = [];

foreach my $f ( </Users/qif/Desktop/n73/Mail2/00001001_S/*/*> )
{
  push @{$all}, &breakdown ($f);
}

#my @tmp = sort { $a->{'t'} <=> $b->{'t'} } @{$all};
#die Dumper (\@tmp);

&as_html($all);

exit;

sub breakdown
{
  my $f = shift;
  my $c = slurp($f);
  my $t = timeof($f);

  return
  {
  'raw'  => $f,
  't'    => $t,
  'nt'   => epoch_conv($t),
  'nums' => grab_nums($c),
  'msg'  => grab_msg($c),
  };
}


sub as_html
{
  my $recs = shift;
  print &html_head . per_row($recs) . &html_foot;
}


# pass in arrayref, unwrap it for a map,
# build tr-html as anonarray element
# join them & return!
sub per_row
{
  return join "\n",
  map
  {
    my $aa = $_->{'t'};
    my $bb = $_->{'nt'};
    my $cc = $_->{'msg'};

    my $dd = join "<br/>", @{$_->{'nums'}};

    "<tr><td>$aa</td><td>$bb</td><td>$cc</td><td>$dd</td></tr>";
  }
  (@{shift()});
}
  
sub html_foot
{
  return "</table></body></html>";
}

sub html_head
{
  return<<EOHEAD;
Content-type: text/html

<html><head><title>Symbian messaging parse test</title></head>
<body>

<table border='1' valign='break'>
 <tr>
  <th> Epoch </th>
  <th> Nice </th>
  <th> Message </th>
  <th> Numbers </th>
 </tr>

EOHEAD
}

sub grab_msg
{
  my $c = shift;

  my $ar = [split //, $c]; #print Dumper ($ar);

  my $s = 0;
  my $aa = "";
  foreach (split //, $c)
  {
    $s++; next if ($s < 60);
    $aa .= $_;
  }

  if ($aa =~ /^(.+?).\)4/) { return $1; }

  return "<font color='red'>blank</font>";
}
sub grab_nums
{
  if ($_[0] =~ m#\d\+\d\d+#) { return [$_[0] =~ /\d(\+\d\d+)/g]; }

  return [];
}

sub slurp
{
  my $f = shift;

  open (IN, $f) or die "cant open : $f: $!";
  local $/=undef;
  my $c = <IN>;
  close IN;
  return $c;
}
sub epoch_conv { return scalar localtime(shift); }
sub timeof
{
  my $f = shift;
  my ($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size, $atime,$mtime,$ctime,$blksize,$blocks) = stat($f);
  return $mtime;
}
