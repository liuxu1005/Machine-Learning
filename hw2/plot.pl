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