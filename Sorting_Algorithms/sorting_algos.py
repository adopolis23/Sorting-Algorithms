import csv
import time
import json

import math
import pandas as pd
import sys


column_names= ['tconst', 'primaryTitle', 'originalTitle', 'startYear',
               'runtimeMinutes', 'genres', 'averageRating', 'numVotes', 'ordering',
               'category', 'job', 'seasonNumber', 'episodeNumber', 'primaryName', 'birthYear',
               'deathYear', 'primaryProfession']


#############################################################################################################
# Data Filtering
#############################################################################################################
def data_filtering(filelocation, num):

    #read the csv file into a dataframe
    df= pd.read_csv(filelocation)

    if(num==1):

        df_year = df[(df["startYear"] >= 1941) & (df["startYear"] <= 1955)]
        df_year.reset_index(drop=True).to_csv("imdb_years_df.csv", index=False)

    if(num==2):
        df_genres = df[(df["genres"] == "Adventure") | (df["genres"] == "Drama")]
        df_genres.reset_index(drop=True).to_csv("imdb_genres_df.csv", index=False)
    if(num==3):

        df_professions = df[df["primaryProfession"].str.contains("assistant_director") | df["primaryProfession"].str.contains("casting_director") | df["primaryProfession"].str.contains("art_director") | df["primaryProfession"].str.contains("cinematographer")]

        df_professions.reset_index(drop=True).to_csv("imdb_professions_df.csv", index=False)
    if(num==4):
 
        df_vowels = df[(df["primaryName"].str[0] == 'A') | (df["primaryName"].str[0] == 'E') | (df["primaryName"].str[0] == 'I') | (df["primaryName"].str[0] == 'O') | (df["primaryName"].str[0] == 'U')]

        print(df_vowels.head)
        df_vowels.reset_index(drop=True).to_csv("imdb_vowel_names_df.csv", index=False)





def less_than(x, pivot, columns):
    for col in columns:
        if x[col] < pivot[col]:
            return True
        elif x[col] > pivot[col]:
            return False
    return False 

def equal(x, pivot, columns):
    for col in columns:
        if x[col] != pivot[col]:
            return False
    return True

def greater_than(x, pivot, columns):
    for col in columns:
        if x[col] > pivot[col]:
            return True
        elif x[col] < pivot[col]:
            return False
    return False





#############################################################################################################
#Quick Sort
#############################################################################################################
def quicksort(arr, columns):
    """
    The function performs the QuickSort algorithm on a 2D array (list of lists), where
    the sorting is based on specific columns of the 2D array. The function takes two parameters:

    arr: a list of lists representing the 2D array to be sorted
    columns: a list of integers representing the columns to sort the 2D array on

    The function first checks if the length of the input array is less than or equal to 1,
    in which case it returns the array as is. Otherwise, it selects the middle element of
    the array as the pivot, and splits the array into three parts: left, middle, right.

    Finally, the function calls itself recursively on the left and right sub-arrays, concatenates
    the result of the recursive calls with the middle sub-array, and returns the final sorted 2D array.
    """
    #if the array size is less than or equal to 1 we return the array
    if len(arr) <= 1:
        return arr
    
    #choose the pivot as the element in the middle of the array
    pivot = arr[len(arr) // 2]

    #list comp to find the left right and middle of the array
    left = [x for x in arr if less_than(x, pivot, columns[1:])]
    middle = [x for x in arr if equal(x, pivot, columns[1:])]
    right = [x for x in arr if greater_than(x, pivot, columns[1:])]

    #return quicksort of the left plus the middle element plus the right elem
    return quicksort(left, columns) + middle + quicksort(right, columns)

#############################################################################################################
#Selection Sort
#############################################################################################################
def selection_sort(arr, columns):
    """
    arr: a list of lists representing the 2D array to be sorted
    columns: a list of integers representing the columns to sort the 2D array on
    Finally, returns the final sorted 2D array.
    """


    #for each item in the array
    for i in range(len(arr)):
        #min index is the index of the current item
        minIndex = i

        #for each element from i to end of array
        for j in range(i+1, len(arr)):
            if compLessThan(arr[j], arr[minIndex], columns):
                minIndex = j
        
        #if another element is the minimum then swap the elements
        if i != minIndex:
            tmp = arr[minIndex]
            arr[minIndex] = arr[i]
            arr[i] = tmp


    return arr
    #Output Returning array  [['tconst','col1','col2'], ['tconst','col1','col2'], ['tconst','col1','col2'],.....]

#############################################################################################################
#Heap Sort
#############################################################################################################
def max_heapify(arr, n, i, columns):
    """
    arr: the input array that represents the binary heap
    n: The number of elements in the array
    i: i is the index of the node to be processed
    columns: The columns to be used for comparison

    The max_heapify function is used to maintain the max heap property
    in a binary heap. It takes as input a binary heap stored in an array,
    and an index i in the array, and ensures that the subtree rooted at
    index i is a max heap.
    """
    #max value is the node being proccessed
    maxVal = i

    #find index of left and right child
    leftChild = i*2 + 1
    rightChild = i*2 + 2



    #if left child exists and is greater than the current max then max is now left child
    if leftChild < n and compGreaterThan(arr[leftChild], arr[maxVal], columns):
        maxVal = leftChild

    #if right child exists and is greater than the current max then max is now right child
    if rightChild < n and compGreaterThan(arr[rightChild], arr[maxVal], columns):
        maxVal = rightChild

    #maxVal is now the max value of the node to be processed and its children

    #if the largest value is not the node being processed then swap them
    if maxVal != i:
        arr[i], arr[maxVal] = arr[maxVal], arr[i]

        #now that we have swapped we need to call heapify again on the old place of largest
        max_heapify(arr, n, maxVal, columns)


def build_max_heap(arr, n, i, columns):
    """
    arr: The input array to be transformed into a max heap
    n: The number of elements in the array
    i: The current index in the array being processed
    columns: The columns to be used for comparison

    The build_max_heap function is used to construct a max heap
    from an input array.
    """
    #NEED TO CODE
    #Implement heapify algorithm here

    #for each element in array starting at n//2-1 going to 0
    #do a max heapify on the node
    for j in range(n//2 -1, -1, -1):
        max_heapify(arr, n, j, columns)

def heap_sort(arr, columns):
    """
    # arr: list of sublists which consists of records from the dataset in every sublists.
    # columns: store the column indices from the dataframe.
    Finally, returns the final sorted 2D array.
    """

    #creates the max heap from the data
    build_max_heap(arr, len(arr), 0, columns)

    #from the last element down to the first
    for i in range(len(arr)-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        max_heapify(arr, i, 0, columns)

    return arr
    #Output Returning array  [['tconst','col1','col2'], ['tconst','col1','col2'], ['tconst','col1','col2'],.....]

#############################################################################################################
#Shell Sort
#############################################################################################################
def shell_sort(arr, columns):
    """
    arr: a list of lists representing the 2D array to be sorted
    columns: a list of integers representing the columns to sort the 2D array on
    Finally, returns the final sorted 2D array.
    """


    #chose a starting gap in this case we will use len of array / 2
    gap = len(arr) // 2

    while gap > 0:

        #for each element from the gap to the end of array
        for i in range(gap, len(arr)):

            #arr[i][index] < arr[i-gap][index]

            #compare to element one gap to the left
            if compLessThan(arr[i], arr[i-gap], columns):
            #if arr[i][index] < arr[i-gap][index]:
                #if in incorrect place in array swap them
                arr[i], arr[i-gap] = arr[i-gap], arr[i]

                
                #then must go to eleemnt swapped and compare with elemenet onbe gap to left of it
                j = i - gap
                while j-gap >= 0:

                    #swap if in incorrect place
                    if compLessThan(arr[j], arr[j-gap], columns):
                    #if arr[j][index] < arr[j-gap][index]:
                        arr[j], arr[j-gap] = arr[j-gap], arr[j]
                    j = j - gap
        
        #once we have checked all elements reduce gap by 2
        gap = gap // 2



    return arr
    #Output Returning array should look like [['tconst','col1','col2'], ['tconst','col1','col2'], ['tconst','col1','col2'],.....]
    #column values in sublist must be according to the columns passed from the testcases.

#############################################################################################################
#Merge Sort
#############################################################################################################
def merge(left, right, columns):
    """
    left: a list of lists representing the left sub-array to be merged
    right: a list of lists representing the right sub-array to be merged
    columns: a list of integers representing the columns to sort the 2D array on

    Finally, after one of the sub-arrays is fully merged, the function extends the result
    with the remaining elements of the other sub-array and returns the result as the final
    sorted 2D array.
    """
    sol = []

    #while there are still elements left in both arrays
    while len(left)>0 and len(right)>0:

        #if the front of left array is smaller remove and add to sol
        if not compGreaterThan(left[0], right[0], columns):
            x = left[0]
            left = left[1:]
            sol.append(x)
        #else take front of right and add it
        else:
            x = right[0]
            right = right[1:]
            sol.append(x)

    #add the remaining elements to sol
    while len(left)>0:
        x = left[0]
        left = left[1:]
        sol.append(x)

    while len(right)>0:
        x = right[0]
        right = right[1:]
        sol.append(x)
    
    return sol





def merge_sort(data, columns):
    """
    data: a list of lists representing the 2D array to be sorted
    columns: a list of integers representing the columns to sort the 2D array on
    Finally, the function returns the result of the merge operation as the final sorted 2D array.
    """
    if len(data) <= 1:
        return data

    #mid is initialized to be the middle of the array
    mid = len(data) // 2

    #l and r are each side of mid respectivly
    l = data[:mid]
    r = data[mid:]

    #apply merge sort on each side
    l = merge_sort(l, columns)
    r = merge_sort(r, columns)

    #return Sorted array
    return merge(l, r, columns)

    #Output Returning array should look like [['tconst','col1','col2'], ['tconst','col1','col2'], ['tconst','col1','col2'],.....]
    #column values in sublist must be according to the columns passed from the testcases.

#############################################################################################################
#Insertion Sort
#############################################################################################################
def insertion_sort(arr, columns):
    """
    # arr: list of sublists which consists of records from the dataset in every sublists.
    # columns: store the column indices from the dataframe.
    Finally, returns the final sorted 2D array.
    """
    b = list(arr)


    #for each element in array
    for i in range(1, len(arr)):
        

        
        j = i-1
        #min starts at that element
        minIndex = b[i]


        #go through all of the rest of the elements
        while j >= 0 and compLessThan(minIndex, b[j], columns):
            b[j+1] = b[j]
            j -= 1

        b[j+1] = minIndex
    
    #NEED TO CODE
    #Insertion Sort Implementation
    #Return : List of tconst values which are obtained after sorting the dataset
    return b
    #Output Returning array should look like [['tconst','col1','col2'], ['tconst','col1','col2'], ['tconst','col1','col2'],.....]
    #column values in sublist must be according to the columns passed from the testcases.



#function that takes in two lists and compares them based on columns
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





#function that takes in two lists and compares them based on columns
def compGreaterThan(item1, item2, columns):
    compare = 1
    index = columns[compare]

    while item1[index] == item2[index] and compare < len(columns)-1:
        compare = compare + 1
        index = columns[compare]
    
    if item1[index] > item2[index]:
        return True
    else:
        return False
    
#function takes an input and returns it as an int if its a string that can be changed to an int for compare functions
def parse(x, index):
    if isinstance(x, str):
        if x.isdigit() and index != 1:
            return int(x)
        else:
            return x
    
    else:
        return x


#############################################################################################################
# Sorting Algorithms Function Calls
#############################################################################################################
def sorting_algorithms(file_path, columns, select):
    """
    # file_path: a string representing the path to the CSV file
    # columns: a list of strings representing the columns to sort the 2D array on
    # select: an integer representing the sorting algorithm to be used

    # colum_vals: is a list of integers representing the indices of the specified columns to be sorted.

    # data: is a 2D array of values representing the contents of the CSV file, with each row in
    the array corresponding to a row in the CSV file and each element in a row corresponding to a value
    in a specific column.

    """

    #Read imdb_dataset.csv
    #write code here Inorder to read imdb_dataset
    df= pd.read_csv(file_path)
    columns.insert(0, "tconst")
    column_vals = []
    

    
    for name in columns:
        for i in range(len(df.columns)):
            if name == df.columns[i]:
                column_vals.append(i)
    

                

    

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data=[]
        for row in reader:
            lst=[]
            for i in column_vals:
                if(i==6):
                    lst.append(float(list(row.values())[i]))
                elif(i in [3, 4, 7, 8, 11, 12, 14, 15]):
                    lst.append(float(list(row.values())[i]))
                else:
                    lst.append(str(list(row.values())[i]).strip())
            data.append(lst)
    l = len(column_vals)
    column_vals = [i for i in range(l)]
    
    if(select==1):
        start_time = time.time()
        output_list = insertion_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    
    if(select==2):
        start_time = time.time()
        output_list = selection_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==3):
        start_time = time.time()
        output_list = quicksort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==4):
        start_time = time.time()
        output_list = heap_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==5):
        start_time = time.time()
        output_list = shell_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
    if(select==6):
        start_time = time.time()
        output_list = merge_sort(data, column_vals)
        end_time = time.time()
        time_in_seconds = end_time - start_time
        return [time_in_seconds, list(map(lambda x: x[0], output_list))]
