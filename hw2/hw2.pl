#!user/bin/perl
# HW2 comp 135
# Xu Liu
#
#  Main entrance for project 2
#  to run project 2 by  " perl hw2.pl"
#  All parameters can be changed in this file
#  -p  is path to data files
#  -s  is smooth number float type 
#  -k  is folds number int type
#  -t  is size of train set, is between 0 and 1
#

 
$index;
#calculate accuracy and std
open(out, ">>m0_ibm");
for($index = 0.1; $index <= 1; $index = $index + 0.1)
{
   print out `python NaiveBayes.py -p './ibmmac/' -s 0 -k 10 -t $index`;
} 
close out;

open(out, ">>m1_ibm");
for($index = 0.1; $index <= 1; $index += 0.1)
{
   print out `python NaiveBayes.py -p './ibmmac/' -s 1 -k 10 -t $index`;
}
close out;

open(out, ">>m0_sport");
for($index = 0.1; $index <= 1; $index += 0.1)
{
   print out `python NaiveBayes.py -p './sport/' -s 0 -k 10 -t $index`;
}
close out;

open(out, ">>m1_sport");
for($index = 0.1; $index <= 1; $index += 0.1)
{
   print out `python NaiveBayes.py -p './sport/' -s 1 -k 10 -t $index`;
}
close out;

open(out, ">>mf_ibm");
for($index = 0; $index <= 0.9; $index += 0.1)
{
   print out `python NaiveBayes.py -p './ibmmac/' -s $index -k 10 -t 0.5`;
}
close out;

open(out, ">>md_ibm");
for($index = 1; $index <= 10; $index += 1)
{
   print out `python NaiveBayes.py -p './ibmmac/' -s $index -k 10 -t 0.5`;
}
close out;

open(out, ">>mf_sport");
for($index = 0; $index <= 0.9; $index += 0.1)
{
   print out `python NaiveBayes.py -p './sport/' -s $index -k 10 -t 0.5`;
}
close out;

open(out, ">>md_sport");
for($index = 1; $index <= 10; $index += 1)
{
   print out `python NaiveBayes.py -p './sport/' -s $index -k 10 -t 0.5`;
}
close out;

#plotting
open(my $GP,'| gnuplot');
print {$GP} << "__GNUPLOT__";


set ylabel "Accuracy ";
set xlabel "Train set size"; 
set terminal png;

set output 'ibm_vs_trainsets.png';
plot  "m0_ibm" u 6:7 w lp title 'smooth = 0', "m0_ibm" u 6:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle,\\
     "m1_ibm"  u 6:7 w lp title 'smooth = 1', "m1_ibm" u 6:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle;

set output 'sport_vs_trainsets.png';
plot  "m0_sport" u 6:7 w lp title 'smooth = 0', "m0_sport" u 6:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle,\\
     "m1_sport"  u 6:7 w lp title 'smooth = 1', "m1_sport" u 6:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle;

set ylabel "Accuracy ";
set xlabel "Smooth (train set size = 0.5)"; 
set terminal png;
set output 'smooth_less_than_1.png';
plot  "mf_ibm" u 4:7 w lp title 'ibm', "mf_ibm" u 4:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle,\\
     "mf_sport"  u 4:7 w lp title 'sport', "mf_sport" u 4:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle;

set output 'smooth_lager_than_1.png';
plot  "md_ibm" u 4:7 w lp title 'ibm', "md_ibm" u 4:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle,\\
     "md_sport"  u 4:7 w lp title 'sport', "md_sport" u 4:7:((\$7) - (\$8)/2):((\$7) + (\$8)/2) w yerrorbars notitle;

__GNUPLOT__

close $GP;
 
