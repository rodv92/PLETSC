import re
import sys

# we use \' to escape ' (python specific)
contractions = [
    "(ain) (\'t)",
    "(aren) (\'t)",
    "(can) (\'t)",
    "(couldn) (\'t)",
    "(didn) (\'t)",
    "(doesn) (\'t)",
    "(don) (\'t)",
    "(hadn) (\'t)",
    "(hasn) (\'t)",
    "(haven) (\'t)",
    "(isn) (\'t)",
    "(mightn) (\'t)",
    "(mustn) (\'t)",
    "(needn) (\'t)",
    "(shan) (\'t)",
    "(shouldn) (\'t)",
    "(wasn) (\'t)",
    "(weren) (\'t)",
    "(won) (\'t)",
    "(wouldn) (\'t)",
    "(he) (\'d)",
    "(he) (\'ll)",
    "(he) (\'s)",
    "(how) (\'d)",
    "(how) (\'ll)",
    "(how) (\'s)",
    "(i) (\'d)",
    "(i) (\'ll)",
    "(i) (\'m)",
    "(i) (\'ve)",
    "(it) (\'d)",
    "(it) (\'ll)",
    "(it) (\'s)",
    "(let) (\'s)",
    "(ma) (\'am)",
    "(might) (\'ve)",
    "(must) (\'ve)",
    "(o) (\'clock)",
    "(she) (\'d)",
    "(she) (\'ll)",
    "(she) (\'s)",
    "(should) (\'ve)",
    "(somebody) (\'s)",
    "(someone) (\'s)",
    "(something) (\'s)",
    "(that) (\'d)",
    "(that) (\'ll)",
    "(that) (\'s)",
    "(there) (\'d)",
    "(there) (\'ll)",
    "(there) (\'s)",
    "(they) (\'d)",
    "(they) (\'ll)",
    "(they) (\'re)",
    "(they) (\'ve)",
    "(wasn) (\'t)",
    "(we) (\'d)",
    "(we) (\'ll)",
    "(we) (\'re)",
    "(we) (\'ve)",
    "(what) (\'d)",
    "(what) (\'ll)",
    "(what) (\'re)",
    "(what) (\'s)",
    "(when) (\'d)",
    "(when) (\'ll)",
    "(when) (\'s)",
    "(where) (\'d)",
    "(where) (\'ll)",
    "(where) (\'s)",
    "(who) (\'d)",
    "(who) (\'ll)",
    "(who) (\'re)",
    "(who) (\'s)",
    "(who) (\'ve)",
    "(why) (\'d)",
    "(why) (\'ll)",
    "(why) (\'s)",
    "(would) (\'ve)",
    "(you) (\'d)",
    "(you) (\'ll)",
    "(you) (\'re)",
    "(you) (\'ve)"
]

ngramsfile = open(sys.argv[1],"r")
outngramsfile = open(sys.argv[2],"wt")

for line in ngramsfile:

    line = line.lower()
    line = re.sub(',\d+\n', '', line)
    if(re.search('"{2}',line)):
        #print("skip multi whitespace")
        continue

    line = re.sub('"', '', line)
    
    if "'" in line:
        #print("possible contraction")

        for contraction in contractions:
            (newline, subs) = (re.subn(contraction, r'\1\2', line))    
            #print("newline=", end="")
            if(subs):
                line = newline
            #print(newline)

    #print(line)
    outngramsfile.write(line)
    outngramsfile.write("\n")
    
ngramsfile.close()
outngramsfile.close()

