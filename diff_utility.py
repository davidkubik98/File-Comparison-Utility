# CISC 365 - Assignment 4
# Created by David Kubik
# Credit: https://www.geeksforgeeks.org/python-program-for-longest-common-subsequence/
# Credit for parts of the LCS algorithm

def fillDynamicMatrix(file1lines,file2lines,file1lines_encoded, file2lines_encoded):
    # This function returns a matrix of matches / mismatches
    matrix = [[0]*(len(file2lines_encoded)+1) for _ in range(len(file1lines_encoded)+1)]
    #Iterates through the enumerated, encoded lines and compares elements 
    for x_i,x_element in enumerate(file1lines_encoded):
        for y_i,y_element in enumerate(file2lines_encoded):
            if x_element == y_element: #If the ith in file1lines_encoded equals jth element, 
                if file1lines[x_i] == file2lines[y_i]: # If the i-th element equals the j-th element, the value in the cell (i,j) is the value of the cell (i-1,j-1) plus 1.
                    matrix[x_i][y_i] = matrix[x_i-1][y_i-1] + 1
                else: # Otherwise, the max of the values (i-1,j) and (i, j-1) is placed in cell (i,j)
                    matrix[x_i][y_i] = max((matrix[x_i][y_i-1],matrix[x_i-1][y_i]))
            else:
                matrix[x_i][y_i] = max((matrix[x_i][y_i-1],matrix[x_i-1][y_i]))
    return matrix 

def findLCS(file1lines, file2lines, file1lines_encoded, file2lines_encoded):
    # findLCS takes two sequences of numbers (encoded and initial strings) and returns the Longest Common Subsequence.
    
    L = fillDynamicMatrix(file1lines, file2lines, file1lines_encoded, file2lines_encoded)
    LCS = []
    x_i,y_i = len(file1lines)-1,len(file2lines)-1
    while x_i >= 0 and y_i >= 0:
        # Compares the integer representations of the lines before comparing the strings.
        if file1lines_encoded[x_i] == file2lines_encoded[y_i]:
            #Traces back the matrix from the max indices and adds the current element to the Longest Common Subsequence.
            if file1lines[x_i] == file2lines[y_i]:
                LCS.append(file1lines_encoded[x_i])
                x_i, y_i = x_i-1, y_i-1
            #If not, depending on the larger val, move up or to the left
            elif L[x_i-1][y_i] > L[x_i][y_i-1]: 
                x_i -= 1
            else:
                y_i -= 1
        elif L[x_i-1][y_i] > L[x_i][y_i-1]:   
            x_i -= 1
        else:
            y_i -= 1
    LCS.reverse()
    return LCS

def f2mod(s):
    # This function is from the previous lab, it maps strings to integers.
    a = 7
    b = 100000
    result = 0
    for c in s:
        result = (a*result + ord(c))%b
    return result

def compare(file1lines, file2lines):
    # compare takes in two files contents and returns a dictionary for blocks of matching lines.
    # the keys are tuples of the starting and ending numbers of the matching lines
    x = [f2mod(line) for line in file1lines]
    y = [f2mod(line) for line in file2lines]
    LCS = findLCS(file1lines, file2lines, x, y) # Finds the Longest Common Subsequence and stores it in LCS

    matchCount= 0  #Holds the length of the amount of lines that form part of the LCS
    output = {}    # Dictionary that outputs the matches / mismatches
    
    for i in range(len(x)): #Iterates through each line in the initial file and check what the LCS cotains
        # The common lines are added to the output dictionary
        if x[i] in LCS:
            matchCount += 1
            matchIndex = y.index(x[i])
            
            if matchIndex != len(y)-1: 
                
                if (y[matchIndex] in LCS) and (y[matchIndex+1] not in LCS):
                    
                    output[(i-matchCount+1, i)] = (matchIndex-matchCount+1,matchIndex) 
                    match_count = 0
            else:
                
                output[(i-matchCount+1, i)] = (matchIndex-matchCount+1,matchIndex) 
                
        elif (matchCount != 0):
            
            matchIndex = y.index(x[i-1])
            output[(i-matchCount, i-1)] = (matchIndex-matchCount+1,matchIndex)
            matchCount = 0
    return output

def show_matches(output, file1lines, file2lines):
    #This function prints the matches of the two files.
    key =list(output.keys())
    value = list(output.values())
    for i in range(len(output)-1):

        if i==0: # This case is when the beginning of one or two files don't match.
            if key[i][0]<=value[i][0] and value[i][0] != 0:
                print("Mismatch:  File1: None      File2: <{}..{}>\n".format(i,value[i][0]-1))
            elif value[i][0]<=key[i][0] and key[i][0] != 0:
                print("Mismatch:  File1: <{}..{}>    File2: None\n".format(i,key[i][0]-1))
            print("Match:     File1: <{}..{}>    File2: <{}..{}>\n".format(*key[i],*value[i]))
            
        if key[i][1] != key[i+1][0]-1: # This case is when the middle of some lines in one file don't match with anything in the second file
            print("Mismatch:  File1: <{}..{}>      File2: None\n".format(key[i][1]+1,key[i+1][0]-1))
        if value[i][1] != value[i+1][0]-1:
            print("Mismatch:  File1: None    File2: <{}..{}>\n".format(value[i][1]+1,value[i+1][0]-1))
        print("Match:     File1: <{}..{}>    File2: <{}..{}>\n".format(*key[i+1],*value[i+1]))
        
    if key[-1][1] < len(file1lines)-1 and  value[-1][1] == len(file2lines)-1:  #Last matching line to the end of the file.
        print("Mismatch:  File1: <{}..{}>    File2: None\n".format(key[-1][1]+1,len(file1lines)-1))
    elif value[-1][1] < len(file2lines)-1 and  key[-1][1] == len(file1lines)-1:
        print("Mismatch:  File1: None      File2: <{}..{}>\n".format(value[-1][1]+1,len(file2lines)-1))
    elif key[-1][1] < len(file1lines)-1 and  value[-1][1] < len(file2lines)-1:
        print("Mismatch:     File1: <{}..{}>    File2: <{}..{}>\n".format(key\[-1][1]+1, len(file1lines)-1,value[-1][1]+1,len(file2lines)-1))
    return True

def main():
    print ("Welcome! Please enter the names of the two files you'd like to compare.")
    while True:
        file1 = input("Please enter the name of the first file: ")
        file2 = input("Please enter the name of the second file: ")
        
        try:
            f1 = open(file1, "r")
            f2 = open(file2, "r")
            file1lines = list(filter(lambda a: a != "\n", f1.readlines()))
            file2lines = list(filter(lambda a: a != "\n", f2.readlines()))
            f1.close()
            f2.close()
            out = compare(file1lines, file2lines)
            show_matches(out, file1lines, file2lines)
        except FileNotFoundError:
            print("One of your files do not exist.")

        decision = input("Would you like to continue? (Y/N):")
        if str.lower(decision) == "n":
            print ("Have a good day!")
            break
        elif str.lower(decision) == "y":
            print()
        else:
            print ("Incorrect input. Exiting Program.")
            break
    
main()






