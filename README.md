# PLETSC
Lightweight english text stream compression, with word tokens, ngrams, session dictionaries and Huffmann for unknown words.

# How to use :

git clone and
decompress dics.zip in the current folder.

Syntax for compression :

python3 dicstrv.py -c txt_inputfile compressed_outputfile
Reads txt_inputfile and writes compressed text stream to compressed_outputfile.

python3 dicstrv.py -c txt_inputfile
Reads txt_input file and writes compressed output to stdout

Syntax for decompression :

python3 dicstrv.py -x compressed_inputfile txt_outputfile
Reads compressed_inputfile and writes cleartext to txt_outputfile.

python3 dicstrv.py -x compressed_inputfile

Reads compressed_input file and writes cleartext output to stdout

Syntax to generate a compiled dictionary of ngrams :

python3 dicstrv.py -d cleartext_ngrams_inputfile compressed_ngrams

This is rarely used in normal operation.

NOTE: dictionary file count1_w.txt must be in the same directory as the script.
outngrams.bin must be in the same directory as the script, if ngrams are used (secondpass=True)

# Description :

This script is useful for ASCII English text stream compression.
It's pedantic (P in PLETSC stands for "pedantic") because its final goal is to enforce a minima some English syntactic rules, such as whitespace after "," but not before, Capitalization after a "." etc... (but not grammar).
Spell check will probably be recommended but should probably be done upstream (by another applicative layer),
as it will ensure a better compression ratio - since it is based on words of the english dictionary.

Its compression method is primarily based on a token (words and punctuation) dictionary.
It leverages frequency of modern english words:

- Words of the primary dictionary are sorted from most used to least used.
- The line number is used as an index. (+1) index 0 is reserved for whitespace.

It also uses adaptive length encoding (1-2-3 bytes)
First 128 most used tokens are encoded on 1 byte,
Next 16384 + 128 on 2 bytes.
Next 2097152 + 16384 + 128 on 3 bytes.

The 3 byte address space is split in two :
- First part (when byte0 msb is 1 and byte1 msb is 1 and byte2 msb is 0) is further divided into two subspaces. 
  - The first subspace is for the remainder of the primary dictionary (it has 333 333 tokens).
  - And the second subspace holds an Ngram dictionary (more on that later).
- Second part (when byte0 msb is 1 and byte1 msb is 1 and byte2 msb is 1) is further divided into two subspaces.
  - First part is for a session dictionary. A session dictionary is used to hold repeating unknown tokens. there are 2097152 - 5
  codes available for this use. Initially empty. Kept in ram, it is a SESSION dictionary. This session dictionary should not
  be required to be sent between two parties, as it can be reconstructed entirely from the compressed stream.
  - Second part is only 5 codes, (TODO, for now just 1 code, and switch between Huffmann and no compression is done in a bool parameter) It is an escape sequence meaning that following bytes will be encoded wit the following methods :
    - first code : As a stream of chars (no compression), plus a C style termination (chr(0)).
    - second code : Huffmann encoding, lowercase only.
    - third code : Huffmann, lowercase + uppercase or uppercase only.
    - fourth code : Huffmann, lowercase + uppercase + numbers, or numbers only.
    - fifth code : All printable ASCII space, mainly for passwords.
    Each of these codes tells what Huffmann tree to use.

Currently, Work is being on done on further improving compression by :

- Third stage : Applying a Burrows-Wheeler Transform to the output of the second pass,
- Fourth stage : A byte based RLE, using absent one or two byte sequences from previous stage as separators
- And finally a huffmann encoding pass trained on averaged binary files states from the second pass. 
  (file with the huffmann tree is huffmann_final_pass.bin)

- Creating a preamble containing separators (to use in third and fourth stages) to use for decompression as well as various other informations required to decompress.


# Performance :

It offers a good compression ratio (between 2.6 and 3.0+), That is, Sizes in % of ORIGINAL size of around 33% to 38%, mainly depending on the lexical complexity or lexical archaism of the source text, and presence of unkwnown or misspelled words.

A higher lexical complexity, or archaic texts, that is, if the input text uses less common words – based on current usage – (2023), will yield lower compression ratios.

The compresion ratio is more or less stable : it is quite independent of text length.

This is contrary to block algorithms that suffer from low compression for small files because of a significant overhead.
For larger corpuses, block algorithms usually perform better, and modern methods may use ML methods to provide context and adaptive
encoding based on that, they're usually slower.

This is why this algorithm is intended for stream compression (on the fly). However, its current implementation is based on reading files. and outputting to a file or stdout.

# Compression speed (all options enabled)

  For this test :

- File is call_of_cthulhu.txt, size uncompressed is 69 kB
- Compression speed around 23,3 kB/s on a Intel(R) Core(TM) i5 CPU       M 520  @ 2.40GHz (computer from 2011), + SSD storage

# Footprint (filesystem)

zipped size of count1_w.txt + outngrams.bin is 11 566 806 bytes
unzipped size is : 31 327 633 bytes + 3 157 445 bytes = 34 485 078 bytes.

# Footprint (memory)

To be determined

# Dependecies 

These Python modules are required :

codecs, nltk, re, bitstring, bitarray, struct, time, dahuffman

# Requirements

Input text file must be ASCII (for now) or UTF-8 decodable to ASCII (English). It ignores conversion errors.
Decoded file will be encoded in ASCII.
It should be in English to get adequate conversion.

Both ends (sender and receiver) MUST have the SAME dictionaries and the SAME Huffmann tables, as these are not sent with 
the data.

# Information about the dictionaries

The primary dictionary is based on the "count_1w.txt" english dictionary of 333 333 words, (words ordered by lexical prevalence) tweaked with added special characters also listed by order of prevalence and added english contractions, and with word count number stripped off.

The original primary dictionary file is available on : https://norvig.com/ngrams/

It also features a secondary (optional) compression pass based on a compiled dictionary named outngrams.bin.

It features compression for 4 and 5 word ngrams found in the first compression step stream.
Ngrams of less than 4 words are deemed not interesting as the first pass will usually encode them on 3 bytes, the same sized as a compressed ngram.

Compression and decompression require the primary dictionary to be available, and the secondary if the boolean SecondPass is set to true, (by default).

**The zip "dics.zip" already have a compiled version of these dictionaries.**

# More information

The algorithm is heavily commented in the code.

# Field of application

Main applications could be messaging over low bandwidth links like POCSAG radio text, or JS8Call for HAM radio, and IoT.

However, note that the underlying digital mode should allow binary transmission (not only transmission of printable ASCII characters) for seamless integration.

For HAM Radio, there is also the issue that this compression algorithm REQUIRES the dictionaries to be present at the receiver
end too, which could be interpreted by regulating authorities such as the FCC as encryption, which is forbidden.
On the other hand, it is possible to mitigate this issue if a protocol preamble is added stating that this compression scheme is used, and then installed as a plugin.
If there is no Internet access, and the RX side doesn't have the dictionaries or updated software, no luck...

# TODO and ISSUES :

See comments in the code.

Main issues for now are syntactic rules and spurious whitespaces, absence of whitespaces were they should have been,
problems with hyphenated tokens, spurious newlines, problems with some possessive forms, and special constructs
besides emails and well formed URLs.

# Ngrams Processing from scratch :

Useful if you want to tweak or create your own dictionaries, we'll discuss mainly the outngrams.bin dictionary,
as count_1w.txt tweaking is straightforward.
Note that count1_w.txt should not be modified once outngrams.bin is generated, or you'll have to rebuild outngrams.bin

A preparatory step is required to generate a compressed version of the ngrams files, if you want to do it from scratch :

First create the ngrams CSV using this code repo :
https://github.com/orgtre/google-books-ngram-frequency/tree/main/python

The repo contains scripts that perform the download and concatenation of ngrams according to criterions you specify.
Note that LETSC has limited space in the first subspace of the 3 byte. more or less 2097152 - 333333
I have created an ngram list of 1571125 ngrams. The distribution between the 4grams and 5grams is roughly 50%/50%

The resulting CSV files need to be further processed by our algorithm

The script that create outngrams.bin (the secondary compiled dictionary based on the primary dictionary and the ngrams csv files from google-books-ngram) is called ngrams_format_dic.py
This script is commented for what each line does.

EOF
