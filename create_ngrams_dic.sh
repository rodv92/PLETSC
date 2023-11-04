python3 ngrams_format_dic.py 4grams_english-fiction.csv outngrams4.txt
python3 ngrams_format_dic.py 5grams_english-fiction.csv outngrams5.txt

python3 dicstrv4.py -d outngrams4.txt outngrams4.bin.dup
python3 dicstrv4.py -d outngrams5.txt outngrams5.bin.dup
awk '!seen[$0]++' outngrams4.bin.dup > outngrams4.bin
awk '!seen[$0]++' outngrams5.bin.dup > outngrams5.bin
sed -i '786001,$ d' outngrams4.bin
sed -i '786001,$ d' outngrams5.bin

cat outngrams4.bin outngrams5.bin > outngrams.bin
cat outngrams.bin | awk '{ print length, bash $0 }' | sort -n -s | cut -d" " -f2- > sorted.txt


