 set -e 
 
 COLOR_PAGE_COST=0.19
 BW_PAGE_COST=0.19
 BINDING_PRICE=24

 echo "Counting colored pages..."
#/usr/bin/gs -o - -sDEVICE=inkcov Main.pdf > colorPages.txt

numColorPages=`grep -v "^ 0.00000  0.00000  0.00000" colorPages.txt | grep "^ " | wc -l`
numPages=`grep "through [0-9]+" -Poh colorPages.txt | grep "[0-9]+" -Poh`
numBWPages=$(( numPages - numColorPages ))

echo "Coloured Pages: $numColorPages"
echo "BW Pages:       $numBWPages"
echo " " 
echo Rough Cost: £`python3 -c "print(($numColorPages * $COLOR_PAGE_COST) + ($numBWPages * $BW_PAGE_COST) + $BINDING_PRICE)"`
