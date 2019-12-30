import fileinput
import operator
import collections

## Step 1: Reading Information from File
counter = 0
support = 0
unique_item = []
indiv_trans = []
miscellaneous = ['\n', ' ']

for line in fileinput.input('input.txt'):

    ### Determine Min Support
    if counter == 0 :
        support = int(line)

    ### Transaction Extraction
    else :
        indiv_trans.append('')

        ### Get all of unique items/transactions
        for item in line :
            if item not in unique_item and item not in miscellaneous :
                unique_item.append(item)

            if item not in miscellaneous :
                indiv_trans[counter-1] += item

    counter += 1
    pass

## Step 2: Scan for Support - Determine Items that has Min Support - Find Union of 1 Element More - Repeat
tracker_dict = {}
item_max = 2

for i in range( len(indiv_trans) + 1) :
    tracker_dict[i] = []

while unique_item != []  :

    remain_item = []

    ### 1) Get the item to check: i.e A,B,AB,BC, etc
    for item in unique_item :
        item_count = 0

        ### 2) Obtain the corresponding transactions: i.e ABC, BCD, BC, etc
        for trans in indiv_trans :
            letter_count = 0

            ### 3) Detect if letter is in transaction: i.e if item is AB, check if A is in ... and B is in ...
            for letter in item :
                letter_count += trans.count(letter)

            ### 4) Check if item exists in transaction
            if letter_count >= len(item) :
                item_count += 1

        ### 5) Check if Item Count is greater or equal than support
        if item_count >= support :
            tracker_dict[item_count].append(item)
            remain_item.append(item)


    ### 6) Create a new set of items based on satisfactory support items
    unique_item = []
    length = len(remain_item)

    for i in remain_item[0:length-1] :

        ### 7) Obtain unique set of letters -> Sort them alphabetically -> See if its within item_max and not existing already
        for j in remain_item[1:length] :
            unique_trans = set(i+j)
            unique_trans = sorted(unique_trans)

            test_union = ''.join(unique_trans)

            if len(test_union) == item_max and test_union not in unique_item :
                unique_item.append( test_union )

    item_max += 1



### Step 3: Print out Frequent Item List
max_support = len(indiv_trans)

for i in range(max_support + 1) :
    key = max_support - i
    total_item = tracker_dict[key]

    if total_item != [] :
        sorted_list = sorted( total_item )

        for item in sorted_list :
            print("%d: %s" %(key, " ".join(item) ) )

print()

### Step 4: Print out Closed Item List
closed_item = []
pot_maximal_item = []

### 1) Go through the Dictionary
for i in range(max_support + 1) :
    key = max_support - i
    total_item = tracker_dict[key]


    if total_item != [] :
        if len(total_item) == 1 :
            closed_item.append("%d: %s" %(key, " ".join(tracker_dict[key]) ) )
            pot_maximal_item.append( (key, tracker_dict[key][0]) )

        else :
            sorted_list = sorted( total_item )

            check_item = list(sorted_list[0])
            num_common =  len(sorted_list)

            for j in range(1, num_common )  :
                test_subset = [ letter for letter in check_item if letter in sorted_list[j] ]

                ### Check for 2 Conditions: If length matched, that means we found a subset
                if len(test_subset) == len(check_item) :
                    check_item = sorted_list[j]

                elif test_subset == [] or j == num_common - 1:
                    closed_item.append("%d: %s" %(key, " ".join(check_item) ) )
                    pot_maximal_item.append( (key, check_item) )

                    check_item = sorted_list[j]


for item in closed_item :
    print(item)

print()

### Step 5: Print out Maximal Item List
maximal_item = []
pot_max = len(pot_maximal_item)

#print(pot_maximal_item)

for i in range(pot_max ) :
    detect = 0
    item_check = pot_maximal_item[i][1]

    #print( pot_maximal_item[i] )

    for j in range(i+1, pot_max) :
        test_subset = [ letter for letter in item_check if letter in pot_maximal_item[j][1] ]

        if len(test_subset) >= len(item_check):
            detect = 1
            break ;

    if not detect :
        maximal_item.append("%d: %s" %(pot_maximal_item[i][0], " ".join(item_check) ) )


for item in maximal_item :
    print(item)

# for item in maximal_item :
#     print(item)

#print(closed_item)
# print(tracker_dict)
# print(satisfied_closed)
