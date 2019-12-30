import fileinput
import copy
from math import exp, pi

### X is a 10x2 Matrix
### Mu is a 1x2 Matrix
### Cov is a 2x2 matrix


### Matrix Determinant
def det (mat) :
    a = mat[0][0]
    b = mat[0][1]
    c = mat[1][0]
    d = mat[1][1]

    val = a*d - b*c

    return val

### Matrix 2x2 Inversion
def inv ( mat ) :
    a = mat[0][0]
    b = mat[0][1]
    c = mat[1][0]
    d = mat[1][1]

    det = a*d - b*c
    frac = 1/det

    a *= frac
    b *= frac
    c *= frac
    d *= frac

    inv_mat = [ [d,-b], [-c,a] ]

    return inv_mat

### Matrix Transpose
def trans ( mat ) :
    result = []
    counter = 0

    for row in range(len(mat) ) :
        for col in range( len(mat[row]) ) :
            if not counter :
                result.append( [mat[row][col] ] )
            else :
                result[col].append( mat[row][col] )

        counter = 1

    return result

### Matrix Subtraction
### Format needs to be in mat1: [ [], [] ] and mat2: []
def mat_sub( mat1, mat2 ) :

    result = []

    for row in mat1 :
        temp = []

        for index in range( len(row) ) :
            temp.append(row[index] - mat2[index] )
        result.append(temp)

    return result

### Format needs to be in mat1: [ [], [] ] and mat2: [ [], [] ]
def mat_add(mat1, mat2) :
    result = []

    for row in range( len(mat1) ):
        temp = []

        for col in range( len(mat1[row]) ) :
            temp.append( mat1[row][col] + mat2[row][col] )

        result.append(temp)

    return result


### Matrix Multiplication
def mat_mult( mat1, mat2 ) :
    result = []

    for row in range (len(mat1) )  :
        result.append([])

        for col in range ( len(mat1[row]) ) :
            for col2 in range ( len(mat2[col]) ) :

                calc_val = mat1[row][col] * mat2[col][col2]

                if len(result[row]) != len(mat2[col] ):
                    result[row].append(calc_val)
                else :
                    result[row][col2] += calc_val

    return result

def mat_mult_const( mat1, val) :
    result = []

    for row in range (len(mat1) )  :
        temp = []
        for col in range ( len(mat1[row]) ) :
            temp.append( mat1[row][col] * val)

        result.append(temp)

    return result

def gauss2D (X, mu, cov, k  ) :
    ### Numerator Portion
    x_mu_sub = mat_sub(X,mu) ### 1x2
    first_exp = mat_mult_const(x_mu_sub, -0.5)

    # print(first_exp)
    second_exp = inv(cov)
    second_exp = mat_mult(first_exp, second_exp) ### 1x2 2x2 -> 1x2

    third_exp = trans(x_mu_sub) ### 2x1
    third_exp = mat_mult(second_exp, third_exp) ### 1x1

    num = exp(third_exp[0][0])

    ### Denominator Portion
    denom = det(cov)
    denom = ( (2*pi)**k * denom)**0.5

    ### Combined Expression


    return num/denom


### Must be Same Size
def sum_list( list ) :
    result = []

    for label in range( len(list) ) :
        if result == [] :
            result = copy.deepcopy(list[label])

        else :
            list1 = []

            for i in range( len(result) ) :
                list1.append(result[i])

            list2 = copy.deepcopy(list[label])

            for i in range( len(list1) ):
                result[i] = list1[i] + list2[i]

    return result


### Must be [] and []
def sub_list(list1, list2) :
    result = []

    for i in range(len(list1) ) :
        result.append(list1[i] - list2[i] )

    return result


def div_list( num, denom) :
    result = []
    # print(num)
    # print(denom)
    for i in range( len(num) ) :
        result.append( num[i]/denom[i] )

    return result

def mult_list( list, val ) :
    result = []

    for i in range( len(list) ) :
        result.append( list[i] * val)

    return result

### Initializing Values
first_line = 1
N = 0
K = 0
point_count = 0

points_coor = []
clust_coor = []
cov = [ [1,0], [0,1] ]

### Reading from Input
for line in fileinput.input('input.txt'):
    content = line.split()

    ### Reading N and K and storing in coordinates for example/cluster
    if first_line :
        first_line = 0
        N = int(content[0])
        K = int(content[1].split("\n")[0] )
        # print(N)
        # print(K)
    else :
        coor = []

        for val in content :
            coor.append( float(val.split("\n")[0]) )

        if point_count != N :
            points_coor.append(coor)
            point_count += 1

        else :
            clust_coor.append(coor)




### Next Steps
### Initializing Prior to be 1/N and Cov to be Identity Matrix
w_j = []
full_cov = []
prev_pred = []
prev_pred_prob = []
iter = 0

for i in range(K) :
    w_j.append(1/N)
    full_cov.append([ [1,0], [0,1] ])



### Run for 50 iterations or until values converges
for iter in range(50) :
    full_gauss = []
    total = []
    label_num = 0

    curr_pred = []
    curr_pred_prob = []

    ### Go through each of the Clusters and make a Gaussian 2D Prediction
    for j in range(K) :
        label = []
        mu = clust_coor[j]
        prior = w_j[j]
        cov = full_cov[j]

        for i in range(N) :
            ### Evaluating Gaussian 2D
            result = gauss2D([points_coor[i]], mu, cov, i+1)
            label.append(prior * result)


            ### Making Prediction. If current prediction has higher probability, replace it
            if len(curr_pred) != N :
                curr_pred.append(j)
                curr_pred_prob.append(prior*result)

            else :
                if prior*result > curr_pred_prob[i] :
                    curr_pred[i] = j
                    curr_pred_prob[i] = prior*result

        full_gauss.append(label)


    if curr_pred == prev_pred :
        break
    else :

        prev_pred = curr_pred


    ### Updating mu, cov, prior for each label
    bayes_denom = sum_list(full_gauss)

    for j in range(K) :
        label = full_gauss[j]

        w_i_j = div_list(label, bayes_denom)
        old_mu = clust_coor[j]
        total_mu = []

        ### Update Mu and Prior
        for i in range(N) :
            total_mu.append( mult_list(points_coor[i], w_i_j[i]) )

        new_mu = []

        for coor in sum_list(total_mu) :
            new_mu.append( coor / sum(w_i_j) )

        clust_coor[j] = new_mu
        w_j[j] = sum(w_i_j) / N


        ### Update Covariance
        prev_mat = 0

        for i in range(N) :
            exp1 = sub_list( points_coor[i], new_mu )
            exp2 = trans([exp1])

            exp1 = mult_list(exp1, w_i_j[i] )
            exp1 = mult_list(exp1, 1/sum(w_i_j) )
            exp3 = mat_mult(exp2, [exp1] )

            if not prev_mat :
                prev_mat = exp3
            else :
                prev_mat = mat_add(prev_mat, exp3)

        full_cov[j] = prev_mat


for label in prev_pred :
    print(label)
