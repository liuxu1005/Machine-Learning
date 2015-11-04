

my $k;
my @file=("artdata.arff", "ionosphere.arff", "iris.arff", "seeds.arff");
my @rlt =(0, 0, 0, 0);
my $index;
my $repeat;
`rm nmi_init cs_init cs_k`; 

#cal
open(out, ">>nmi_init"); 
for ($index = 1; $index <= 10; $index +=1) {
    for($k = 0; $k < 4; $k +=1) {
        my $tmpfile = $file[$k];
        $rlt[$k] = `python hw3.py -f $tmpfile -k 0 -r 1`;
    }
    printf out "%d %f  %f  %f  %f\n", $index, @rlt
    
}
close out;

my @rlt =(0, 0, 0, 0);
open(out, ">>cs_init"); 
for ($index = 1; $index <= 10; $index +=1) {
    for($k = 0; $k < 4; $k +=1) {
        my $tmpfile = $file[$k];
        $rlt[$k] = `python hw3.py -f $tmpfile -k 0 -r 0`;
    }
    printf out "%d %f  %f  %f  %f\n", $index, @rlt
    
}
close out;

my @rlt =(100000, 100000, 100000, 100000);

open(out, ">>cs_k"); 
for ($index = 1; $index <= 15; $index +=1) {
    for($k = 0; $k < 4; $k +=1) {
        for($repeat = 1; $repeat <= 10; $repeat += 1) {
            my $tmpf = $file[$k];
            my $tmp = `python hw3.py -f $tmpf -k $index -r 0`;
            if ($tmp < $rlt[$k]) {
                $rlt[$k] = $tmp;
            }
        }
    }
    printf out "%d %f  %f  %f  %f\n", $index, @rlt;
    
}
close out;

#plot result

open(my $GP,'| gnuplot');

print {$GP} << "__GNUPLOT__";


set ylabel "CS";
set xlabel "K";
set title "CS vs K"
set xrang[0:15];
set xtics("1" 0, "2" 1, "3" 2, "4" 3, "5" 4, "6" 5, "7" 6, "8" 7,\\
          "9" 8, "10" 9, "11" 10, "12" 11, "13" 12, "14" 13, "15" 14)
set terminal png;
set output 'cs_k1.png'

plot "cs_k" u 2  w lp title 'art', "cs_k" u 3 w lp title 'iono'

set output 'cs_k2.png'

plot  "cs_k" u 4 w lp title 'iris', "cs_k" u 5 w lp title 'seeds'

set ylabel "CS";
set xlabel "init";
set title "CS vs init";
set xrang[-1:11];
set xtics("1" 0, "2" 1, "3" 2, "4" 3, "5" 4, "6" 5, "7" 6, "8" 7,\\
          "9" 8, "10" 9)
set boxwidth 0.5;
set style data histograms
set style histogram cluster
set style fill solid;

set terminal png;
set output 'cs_init.png';

plot "cs_init" using 2 title 'art', "cs_init" u 3 title 'ion',\\
 "cs_init" u 4 title 'iris', "cs_init" u 5 title 'seeds';



set ylabel "NMI";
set xlabel "init";
set title "NMI vs init"
set xrang[-1:11];
set xtics("1" 0, "2" 1, "3" 2, "4" 3, "5" 4, "6" 5, "7" 6, "8" 7,\\
          "9" 8, "10" 9)
set boxwidth 0.5;
set style data histograms
set style histogram cluster
set style fill solid;
set terminal png;
set output 'nmi_init.png'

plot "nmi_init" using 2 title 'art', "nmi_init" u 3 title 'ion',\\
 "nmi_init" u 4 title 'iris', "nmi_init" u 5 title 'seeds';

__GNUPLOT__
