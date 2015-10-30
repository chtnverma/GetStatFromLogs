
################################################
# Usage: (on python3) 
# python GetStats.py shares.txt 
#
#   shares.txt contains addresses of log files. 
#   One log file per line. 
#
################################################


import sys 
import numpy as np


#Globals: 
g_shares = []


def print_output(f_str,nfiles_peruser, nusers_perfile ): 

    f = open(sys.argv[1] + ".out", "a") 

    print("-------------------------------------------", file = f) 
    print("Processed " + f_str,file = f )
    print("Number of unique files = " + str(len(nusers_perfile)), file = f ) 
    print("Number of users = " + str(len(nfiles_peruser)), file = f )
    print("Mean number of files read by a user = " + str(np.mean(nfiles_peruser)), file = f) 
    print("Median number of files read by a user = " + str(np.median(nfiles_peruser)), file = f) 
    print("Mean number of users who read a file = " + str(np.mean(nusers_perfile)), file = f) 
    print("Median number of users who read a file = " + str(np.median(nusers_perfile)), file = f) 
    print("-------------------------------------------", file = f) 
    f.close()


def parse_line(s): 
    s_p = s.strip().split('\t')  
    if len(s_p) < 3 : 
        return [] 
    return [s_p[2], s_p[3], s_p[4]] 	# Pending: Provide index for fileid, userid, action-type instead of 2, 3, 4 resp.

    # Sample output: : 
    # '\folder\report.doc', 'USER63', 'read'  


def process_1share(f_str): 
    print("Processing " + f_str) 
    file_user_map = {}
    user_file_map = {}    
    f = open(f_str) 

    # Iterating over log file: 
    for line in f:
        temp = parse_line(line) 
        if len(temp)==0 : 
            break 
        [fileid, userid, optype] = temp 
        if not optype == 'read': 	# Pending: modify if an opcode was used instead of 'read'  
            continue

        # Append in dicts:         
        if not userid in user_file_map: 
            user_file_map[userid] = set() 
        user_file_map[userid].add(fileid ) 

        if not fileid in file_user_map: 
            file_user_map[fileid] = set() 
        file_user_map[fileid].add(userid) 
    f.close() 

    # Get numbers: 
    nusers_perfile = [] 
    nfiles_peruser = [] 
    for s in file_user_map.values():
        nusers_perfile.append(len(s)) 

    for s in user_file_map.values():
        nfiles_peruser.append(len(s)) 

    # Printing: 
    print_output(f_str,nfiles_peruser, nusers_perfile ) 


def process_shares(): 
    for share in g_shares: 
        if not share == "": 
            process_1share(share) 


def get_shares_list(): 
    global g_shares 
    with open(sys.argv[1]) as f:
        g_shares = f.readlines() 
    g_shares = [x.strip() for x in g_shares ] 


def main(): 
    get_shares_list()
    process_shares() 

if __name__=='__main__':
    main() 
