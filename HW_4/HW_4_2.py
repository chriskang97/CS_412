import fileinput
from math import log10

train_animal = {}
test_animal = []
total_feature = 16
num_class = 7
total_examples = 0
counter = 0

### Initialize Train Dict
for label in range (1,num_class+1) :
    train_animal[label] = [0,0,0,0,0,0,0,0,0,0,0,0,{0:0, 2:0, 4:0, 5:0, 6:0, 8:0},0,0,0,0]


for line in fileinput.input('input2.txt'):

    ### Ignore first line with strings
    if not counter :
        counter += 1
        continue

    ### Split comma, get rid of the new line char and animal name
    split_line = line.split(",")
    split_line[-1] = split_line[-1].replace("\n", "")
    split_line.pop(0)

    split_line = list( map(int, split_line) )


    ### Use a dictionary to keep track how many features have been counted for each label
    if split_line[-1] != -1 :
        total_examples += 1
        label = split_line[-1]

        ### Check if label exists in dict
        ### Go through all features and count how many features are seen
        for feat_num in range( total_feature ) :
            det_feat = split_line[feat_num]

            if feat_num == 12 :
                train_animal[label][feat_num][det_feat] += 1

            else :
                train_animal[label][feat_num] += det_feat

        ### Count 1 for label class
        train_animal[label][-1] += 1

    else :
        test_animal.append(split_line)


final_pred_class = []

### Predict each item in the Test Set
for test in test_animal :
    p_max = -999
    pred_class = 0
    print()
    ### Go through each Class Label
    for class_num in range(1, num_class+1) :

        ### 1) Calculate P(y=c)
        num_exam_with_class = train_animal[class_num][-1]
        p_y =  ( (num_exam_with_class + 0.1) / ( total_examples + 0.1 * num_class ) )
        #
        # print("Label: ", class_num, )
        # print(num_exam_with_class)
        # print(total_examples)


        ### 2) Calculate P(x=f | y=c )
        ### Assume indepdencies so can multiply all of features at end
        p_x_y = 1

        for feat_num in range ( total_feature ) :

            ### Legs exceptions
            if feat_num == 12 :
                unique_feature = 6
                num_exam_with_class_f = train_animal[class_num][feat_num][test[feat_num] ]

            ### Check what value Test feature has and determine how many other training set has that value
            else :
                unique_feature = 2

                if test[feat_num] == 1 :
                    num_exam_with_class_f = train_animal[class_num][feat_num]
                else :
                    num_exam_with_class_f = num_exam_with_class - train_animal[class_num][feat_num]


            ## Testing if summation is correct
            p_x_y *= ( ( num_exam_with_class_f + 0.1 ) / ( num_exam_with_class + 0.1 * unique_feature ) )

            # print("Label: ", class_num)
            # print("Feature Num: ", feat_num )
            # print(num_exam_with_class_f)
            # print(num_exam_with_class)


        ### Ignore division of P_X since we just need to the numerator to check for highest probability
        P_Y_X = p_x_y * p_y

        print(P_Y_X)
        if P_Y_X > p_max :
            p_max = P_Y_X
            pred_class = class_num


    final_pred_class.append(pred_class)

for pred_class in final_pred_class :
    print(pred_class)
