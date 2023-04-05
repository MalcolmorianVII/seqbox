# 1. Read in script
# 2. Take in pattern
# 3. Magic.... i.e search file for pattern & take out the function defn in that pattern
import os,sys,re

source_file = sys.argv[1]
# pattern = sys.argv[2]

def read_in_source_file(file):
    with open(file,"r") as source_file:
        code = source_file.read()
        return code

def extract_func(pattern,code):
    # Find line # & extract up to either return or blank space/ next def
    search = re.search(pattern, code)
    match = search.group()[0]
    func = ""
    for line in match:
        func += line
    
    return func



def start():
    """Determine the start of code match"""
    return 1

def end():
    """Determine the end"""
    return 2

