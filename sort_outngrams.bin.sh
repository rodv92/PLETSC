cat outngrams5.bin | awk '{ print length, bash $0 }' | sort -n -s | cut -d" " -f2-
