import fileinput
from math import log2

class Node () :
    def __init__( self ):
        self.depth = 0
        self.feature = 0
        self.children = []
        self.criteria = (0,0)

    def change_depth( self,  val ) :
        self.depth = val

    def change_val( self, val ) :
        self.feature = val

    def add_criteria ( self, crit_val ) :
        self.criteria = crit_val

    def add_child( self, child ) :
        self.children.append(child)



### Input: Dict with Feature Num as Key and Feature value in a list: Ex: 1 : 1.0, 2.0, 3.0
## {0: [1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.5], 2: [1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 3.0, 3.0]}
### Output: Dict with Feature Num as Key and Split points value in a list
def splitPoint( feature_remain ) :
    feat_uniq = {}
    split_points = {}

    ### Go through entire dictionary to find unique feature values
    for label in feature_remain :
        for feature in feature_remain[label] :
            for feat_num_val in feature :

                feat_num = feat_num_val[0]
                feat_val = feat_num_val[1]

                if feat_num not in feat_uniq :
                    feat_uniq[feat_num] = []

                if feat_val not in feat_uniq[feat_num] :
                    feat_uniq[feat_num].append(feat_val)

    ### Go through each Feature Number, Sort the list, and find the split points
    for feat_num in feat_uniq :
        feat_uniq[feat_num] = sorted(feat_uniq[feat_num])
        sorted_list = feat_uniq[feat_num]

        if feat_num not in split_points :
            split_points[feat_num] = []

        for i in range(0, len(sorted_list)-1 ) :
            split_points[feat_num].append( (sorted_list[i] + sorted_list[i+1])/2 )

    return split_points



def countDict( feature_remain, splitDict ) :

    countDict = {}
    label_counter = 0

    for label in feature_remain :
        for feature in feature_remain[label] :
            for feature_num_val in feature :

                feature_num = feature_num_val[0]
                feature_val = feature_num_val[1]


                for point in splitDict[feature_num] :
                    key = (feature_num, point)

                    ### 1st Value will be Feature satisfying constrant
                    if key not in countDict :
                        temp_count_list = []
                        temp_count_list_2 = []

                        for i in range( len(feature_remain) ) :
                            temp_count_list.append(0)
                            temp_count_list_2.append(0)

                        countDict[key] = [0,temp_count_list, 0, temp_count_list_2]

                    if feature_val < point :
                        countDict[key][0] += 1
                        countDict[key][1][label_counter] += 1
                    else :
                        countDict[key][2] += 1
                        countDict[key][3][label_counter] += 1

        label_counter += 1

    return countDict



def entropy( feature_remain, total_example ) :
    entropy = 0
    print(total_example)
    print(feature_remain)

    for label in feature_remain :
        count = len(feature_remain[label])
        entropy += -(count/total_example) * log2 (count/total_example)

    return entropy


def infoEntropy( countDict, infoData) :
    ### 1) Go through each label in splitDict and splitPoints corresponding to Label
    ### 2) Go through each feature listed in Feature Remain
    max_entropy = 0
    curr_split = (0,0)
    print("Current Count: ", countDict )
    print("Info Data: ", infoData )
    print()

    for key in countDict :
        indiv_total_example = countDict[key][0]
        indiv_choice = countDict[key][1]

        indiv_total_example_2 = countDict[key][2]
        indiv_choice_2 = countDict[key][3]

        curr_entropy = 0
        total_entropy = 0
        indiv_count = 0
        total_example = indiv_total_example + indiv_total_example_2


        ### Left Side Entropy
        for i in indiv_choice :

            if indiv_total_example != 0 :
                temp = i/indiv_total_example

                if temp != 1.0 and temp != 0.0 :
                    curr_entropy += -temp * log2(temp)
                else :
                    curr_entropy += 0

        temp3 = indiv_total_example / total_example
        total_entropy += temp3 * curr_entropy

        print("Left Entropy: ", total_entropy )

        ### Right Side Entropy
        curr_entropy = 0
        for i in indiv_choice_2 :

            if indiv_total_example_2 != 0 :
                temp = i/indiv_total_example_2

                if temp != 1.0 and temp != 0.0 :
                    curr_entropy += -temp * log2(temp)
                else :
                    curr_entropy += 0

        temp3 = indiv_total_example_2 / total_example
        total_entropy += temp3 * curr_entropy
        print("Right Entropy: ", temp3 * curr_entropy )
        print()

        total_entropy = infoData - total_entropy
        #print(total_entropy)
        ### Deciding if Entropy Exceeds current max
        if total_entropy > max_entropy :
            max_entropy = total_entropy
            curr_split = key

        elif total_entropy == max_entropy :
            if key[0] < curr_split[0] :
                curr_split = key

    return curr_split


def createTree( currNode, train_dict, total_example, depth ) :
    # print("Depth Number: ", depth)
    ### 1) Check if curr_depth = 2, if yes create Leaf Node Label
    if depth == 2 :
        max_length = -2
        curr_label = -2

        for label in train_dict :
            curr_len = len(train_dict[label])
            if (curr_len > max_length) or (curr_len == max_length and label < curr_label) :
                max_length = curr_len
                curr_label = label

                currNode.change_val(curr_label)

        return


    ### 3) Calculate Entropy/Info Entropy on each Split Point and Check which split point has highest entropy
    infoData = entropy(train_dict, total_example)
    splitDict = splitPoint( train_dict )
    countDictOut = countDict(train_dict, splitDict )
    split = infoEntropy(countDictOut, infoData)

    ### Need a Label, Split_point -> Num of Satisfied
    right_side_dict = {}
    right_example = 0
    left_side_dict = {}
    left_example = 0

    for label in train_dict :
        for feature in train_dict[label] :
            detect = 0

            for indiv_feature in feature :
                feature_num = indiv_feature[0]
                feature_val = indiv_feature[1]

                if feature_num == split[0] :
                    if feature_val > split[1] :
                        detect = 1

                        if label not in right_side_dict :
                            right_side_dict[label] = []
            if detect != 1 :
                if label not in left_side_dict :
                    left_side_dict[label] = []
                left_side_dict[label].append(feature)
                left_example += 1
            else :
                if label not in right_side_dict :
                    right_side_dict[label] = []
                right_side_dict[label].append(feature)
                right_example += 1


    left = Node()
    right = Node()


    if split == (0,0) :
        for label in train_dict :
            currNode.change_val(label)

    else :

        createTree( left, left_side_dict, left_example, depth+1)
        createTree( right, right_side_dict, right_example, depth+1)

        currNode.depth = depth
        currNode.add_criteria(split)
        currNode.add_child(left)
        currNode.add_child(right)





### Step 1: Parse the Files accordingly
### [label] [attribute 1]:[value 1] [attribute 2]:[value 2]

train_dict = {}
test_set = []

feat_val_count = {}
total_example = 0


for line in fileinput.input('input1.txt'):

    ### Delimit line by space, obtain label from 1st element, then remove label for further processing
    split_line = line.split()
    label = int(split_line[0])
    split_line.pop(0)

    ### For each feature, obtain the feature number and val, put them as a tuple and append to list in dictionary
    input_feature = []

    for feature in split_line :
        feat_num_val = feature.split(":")
        feat_num = int(feat_num_val[0])
        feat_val = float(feat_num_val[1])

        feat_tup = (feat_num, feat_val)
        input_feature.append(feat_tup)


    if label != -1 :
        if label not in train_dict :
            train_dict[label] = []

        train_dict[label].append(input_feature)
        total_example += 1

    else :
        test_set.append(input_feature)

root = Node()

### 2) Find Split Points given remaining feature
createTree(root, train_dict, total_example, 0 )

# print(test_set)
print("Tree")
print("Root: ", root.criteria)
for child in root.children :
    print("Child: ", child.criteria)
    print("Child Label: ", child.feature )
    for child2 in child.children :
        print("Leaf: ", child2.feature)


for test in test_set :
    node = root
    label = 0

    while( label == 0 ) :
        for feature in test :
            feature_num = feature[0]
            feature_val = feature[1]

            ### Checking for Root Feature
            if node.feature != 0 :
                label = node.feature

            elif feature_num == node.criteria[0] :
                if feature_val < node.criteria[1] :
                    node = node.children[0]
                else :
                    node = node.children[1]
    print(label)
