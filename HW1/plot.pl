#!user/bin/perl
# HW1 comp 135
# Xu Liu

@array;
$index;
$train = "_train_norm.arff";
$test = "_test_norm.arff";


 

#plotting
open(my $GP,'| gnuplot');

print {$GP} << "__GNUPLOT__";


set ylabel "Accuracy (%)";
set xlabel "Number of features";

set xrang[0:];
set xtics ("14" 0, "24" 1, "34" 2, "44" 3, "54" 4, "64" 5, "74" 6, "84" 7, "94" 8);
set terminal png;



set ylabel "Accuracy";
set xlabel "Number of features";
set output 'k5.png';
plot "output_5" u 2  w lp title 'origin', "output_5" u 3 w lp title '14 features', "output_5" u 4 w lp title 'all features';
set output 'k1.png';
plot "output_1" u 2  w lp title 'origin', 'output_1' u 3 w lp title '14 features', 'output_1' u 4 w lp title 'all features';

set ylabel "Accuracy";
set xlabel "Times of relief";

set xrang[0:9];
set xtics ("100" 0, "200" 1, "300" 2, "400" 3, "500" 4, "600" 5, "700" 6, "800" 7, "900" 8, "1000" 9);
set terminal png;

set output 'm_effect.png';
plot "output_m" u 3 w lp title "14 features", "output_m" u 4 w lp title "all features";
__GNUPLOT__

close $GP;

#remove temp files
#`rm temp`;
#`rm output_1`;
#`rm output_5`;
#`rm output_m`;

