from dataclasses import field
import pandas as pd
import math
import os
import csv
import sys
sys.path.append("../Sorting_Algorithms")
#from sorting_algos import merge_sort


column_names= ['tconst', 'primaryTitle', 'originalTitle', 'startYear',
               'runtimeMinutes', 'genres', 'averageRating', 'numVotes', 'ordering',
               'category', 'job', 'seasonNumber', 'episodeNumber', 'primaryName', 'birthYear',
               'deathYear', 'primaryProfession']

####################################################################################
# Donot Modify this Code
####################################################################################
class FixedSizeList(list):
    def __init__(self, size):
        self.max_size = size

    def append(self, item):
        if len(self) >= self.max_size:
            raise Exception("Cannot add item. List is full.")
        else:
            super().append(item)
###################


#code for comparasins and parsing
def compLessThan(item1, item2, columns):
    compare = 1
    index = columns[compare]

    while item1[index] == item2[index] and compare < len(columns)-1:
        compare = compare + 1
        index = columns[compare]

    if item1[index] < item2[index]:
        return True
    else:
        return False

def compGreaterThan(item1, item2, columns):
    compare = 1
    index = columns[compare]

    while parse(item1[index]) == parse(item2[index]) and compare < len(columns)-1:
        compare = compare + 1
        index = columns[compare]
    
    if parse(item1[index]) > parse(item2[index]):
        return True
    else:
        return False
    
def parse(x, index):
    if isinstance(x, str):
        if x.isdigit() and index != 1:
            return int(x)
        else:
            return x
    
    else:
        return x
#########



#merge sort code
def merge(left, right, columns):
    sol = []
    
    while len(left) != 0 and len(right) != 0:
        if compLessThan(left[0], right[0], columns):
            x = left[0]
            left = left[1:]
            sol.append(x)
        else:
            x = right[0]
            right = right[1:]
            sol.append(x)
    
    while len(left) > 0:
        x = left[0]
        left = left[1:]
        sol.append(x)
    
    while len(right) > 0:
        x = right[0]
        right = right[1:]
        sol.append(x)
    
    return sol

def mergeSort(arr, columns):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    
    left = mergeSort(left, columns)
    right = mergeSort(right, columns)
    
    return merge(left, right, columns)





def file_min_index(filepath, num_files, column_vals, data_tracker):
    min_index = 1
    min_item = []

    data_remaining = False
    #for each file
    for i in range(1, num_files):
        df = pd.read_csv(filepath + "/Sorted_" + str(i) + ".csv")
        
        #if file is empty do nothing
        if data_tracker[i-1] >= len(df.index)-1:
            continue
        else:
            data_remaining = True

        #get the top(smallest) value in file
        df_top = df.values[:][data_tracker[i-1]]

        #check if this is the first file looked at or this item is smaller than the current min
        if len(min_item)==0 or compLessThan(df_top, min_item, column_vals):
            min_item = df_top
            min_index = i
    
    if data_remaining == False:
        return -1
    
    #return the min index
    return min_index, min_item
        
        





####################################################################################
# Mystery_Function
####################################################################################
def Mystery_Function(file_path, memory_limitation, columns):
    
    #setup

    #generate column_vals list
    columns.insert(0, "tconst")
    column_vals = [i for i in range(len(columns))]


    #find number of files
    num_files = 1
    while os.path.isfile(file_path + "/Sorted_" + str(num_files) + ".csv"):
        num_files = num_files + 1
    print(str(num_files-1) + " files detected")

    #list with memory limitation
    chuncks_2000=FixedSizeList(memory_limitation)

    #create an array of size numfiles all zeros
    data_tracker = [0] * (num_files-1)


    #computation
    file_index = 1
    data_remaining = True
    while data_remaining:

        #find file with min
        min_index, min_item = file_min_index(file_path, num_files, column_vals, data_tracker)
        #print("Min Index Found: " + str(min_index))
        if min_index == -1:
            data_remaining = False
            continue

        #take top of that file and put into chunks2k
        #df = pd.read_csv(file_path + "/Sorted_" + str(min_index) + ".csv")
        #df_top = df.values[:][data_tracker[min_index-1]]
        data_tracker[min_index-1] = data_tracker[min_index-1] + 1

        #print("Adding value #: " + str(len(chuncks_2000)))
        chuncks_2000.append(min_item)

        #save file without that index in it
        #df = df.iloc[1:, :]
        #df.reset_index(drop=True).to_csv("Individual/Sorted_"+str(min_index)+".csv", index=False)


        #when chunks 2k is full output into file
        if(len(chuncks_2000) == memory_limitation):
            tmp = pd.DataFrame(chuncks_2000)
            print("Creating file: " + "Final/Sorted_"+str(file_index)+".csv")
            tmp.reset_index(drop=True).to_csv("Final/Sorted_"+str(file_index)+".csv", index=False)
            file_index = file_index + 1
            chuncks_2000.clear()








####################################################################################
# Data Chuncks
####################################################################################
def data_chuncks(file_path, columns, memory_limitation):
        """
        # file_path : dataset file_path for imdb_dataset.csv (datatype : String)
        # columns : the columns on which dataset needs to be sorted (datatype : list of strings)
        # memory_limitation : At each time how many records from the dataframe can be loaded (datatype : integer)
        # Load the 2000 chunck of data every time into Data Structure called List of Sublists which is named as "chuncks_2000"
        # NOTE : This data_chuncks function uses the records from imdb_dataset. Only 2000 records needs to be loaded at a
                # Time in order to process for sorting using merge sort algorithm. After sorting 2000 records immediately
                # Store those 2000 sorted records into Floder named Individual by following Naming pattern given below.
        #Store all the output files in Folder named "Individual".
        #Output csv files must be named in the format Sorted_1, Sorted_2,...., Sorted_93
        #The below Syntax will help you to store the sorted files :
                    # name_of_csv = "Individual/Sorted_" + str(i + 1)
                    # sorted_df.reset_index(drop=True).to_csv(name_of_csv, index=False)

        # ***NOTE : Every output csv file must have 2000 sorted records except for the last ouput csv file which
                    might have less than 2000 records.

        Description:
        This code reads a CSV file, separates the data into chunks of data defined by the memory_limitation parameter,
        sorts each chunk of data by the specified columns using the merge_sort algorithm, and saves each sorted chunk
        as a separate CSV file. The chunk sets are determined by the number of rows in the file divided by the
        memory_limitation. The names of the sorted files are stored as "Individual/Sorted_" followed by a number
        starting from 1.
        """
        column_names = ["tconst", "primaryTitle", "originalTitle", "startYear", "runtimeMinutes", "genres", "averageRating", "numVotes", "ordering", "category", "seasonNumber", "episodeNumber", "primaryName", "birthYear", "deathYear", "primaryProfession"]
        column_vals = []

        #add 0 to column vals for the tconst column
        column_vals.append(0)
                    
        columns.insert(0, "tconst")
        column_vals = []
    
        for name in columns:
            for i in range(len(column_names)):
                if name == column_names[i]:
                    column_vals.append(i)
        
        column_vals = [i for i in range(len(column_vals))]

        #Load the 2000 chunck of data every time into Data Structure called List of Sublists which is named as "chuncks_2000"
        chuncks_2000=FixedSizeList(2000)
        file_index = 1

        #for each block of size "memory_limit"
        for block in pd.read_csv(file_path, chunksize=memory_limitation):
            
            #for each for in the block
            for index, row in block.iterrows():
                temp = []
                for col_name in block.columns:
                    if col_name in columns:
                        temp.append(row[col_name])
                chuncks_2000.append(temp)
            
            #sort chunks 2000 with merge sort
            chuncks_2000 = mergeSort(chuncks_2000, column_vals)
            
            #change chunks 2k into a dataframe
            df = pd.DataFrame(chuncks_2000)

            #save dataframe to a csv file and clear the chunks list

            print("Creating File: Individual/Sorted_" + str(file_index))
            df.reset_index(drop=True).to_csv("Individual/Sorted_"+str(file_index)+".csv", index=False)
            file_index = file_index + 1

            chuncks_2000.clear()
            

        #Write code for Extracting only 2000 records at a time from imdb_dataset.csv

        #Passing the 2000 Extracted Records and Columns indices for sorting the data
        #column_indxes are Extracted from the imdb_dataset indices by mapping the columns need to sort on which are
        #passed from the testcases.
        #arr=merge_sort(arr,column_indxes)


#Enable only one Function each from data_chuncks and Mystery_Function at a time

#Test Case 13
data_chuncks('imdb_dataset.csv', ['startYear'], 2000)

#Test Case 14
#data_chuncks('imdb_dataset.csv', ['primaryTitle'], 2000)

#Test Case 15
#data_chuncks('imdb_dataset.csv', ['startYear','runtimeMinutes' ,'primaryTitle'], 2000)




#Test Case 13
#Mystery_Function("Individual", 2000, ['tconst', 'startYear','runtimeMinutes' ,'primaryTitle'])

#Test Case 14
Mystery_Function("Individual", 2000, ['primaryTitle'])

#Test Case 15
#Mystery_Function(file_path="Individual", 2000, ['startYear','runtimeMinutes' ,'primaryTitle'])
