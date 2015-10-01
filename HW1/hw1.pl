#!user/bin/perl
# HW1 comp 135
# Xu Liu

@array;
$index;
$train = "_train_norm.arff";
$test = "_test_norm.arff";


open(out, ">>temp");

#J48 from weka
for($index = 14; $index <= 94; $index += 10)
{
   print out `java -classpath $CLASSPATH:/r/aiml/ml-software/weka-3-6-11/weka.jar  weka.classifiers.trees.J48  -t ./$index$train -T ./$index$test | grep Correctly | tail -1`;

}
close out;

#3 kinds of knn with k = 5 m = 10000
for($index = 14; $index <= 94; $index += 10)
{
    `python knn.py  -t ./$index$train -T ./$index$test -k 5 -o output_5 -rt 10000 -rk a`;
}

#3 kinds of knn with k = 1 m = 10000
for($index = 14; $index <= 94; $index += 10)
{
    `python knn.py  -t ./$index$train -T ./$index$test -k 1 -o output_1 -rt 10000 -rk a`;
}

#m effects for 94 features
for($index = 100; $index <= 1000 ; $index += 100)
{
   `python knn.py  -t ./94_train_norm.arff -T ./94_test_norm.arff -k 5 -o output_m -rt $index -rk w`;
}

#plotting
open(my $GP,'| gnuplot');

print {$GP} << "__GNUPLOT__";


set ylabel "Accuracy (%)";
set xlabel "Number of features";
set key off;
set xrang[0:];
set xtics ("14" 0, "24" 1, "34" 2, "44" 3, "54" 4, "64" 5, "74" 6, "84" 7, "94" 8);
set terminal png;

set output 'J48.png';
plot "temp" u 5 w lp title 'J48'; 

set ylabel "Accuracy";
set xlabel "Number of features";
set output 'k5.png';
plot "output_5" u 2  w lp title 'origin', "output_5" u 3 w lp title '14 features', "output_5" u 4 w lp title 'all features';
set output 'k1.png';
plot "output_1" u 2  w lp title 'origin', 'output_1' u 3 w lp title '14 features', 'output_1' u 4 w lp title 'all features';

set ylabel "Accuracy";
set xlabel "Times of relief";
set key off;
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

