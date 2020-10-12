import sys

file_list = sys.argv[1:]
od={}

for file in file_list:
    lines = open(file).readlines()
    for line in lines:
        if '\\u' in line:
            index = line.find('\\u')
            od[line[index:index+6]]=1
print(od.keys())
