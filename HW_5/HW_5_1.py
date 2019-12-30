import numpy as np
import copy

points = np.array([[1., 1.],
       [1., 3.],
       [1., 4.],
       [1., 5.],
       [0., 4.],
       [2., 4.],
       [3., 4.],
       [4., 4.],
       [5., 4.],
       [4., 3.],
       [4., 5.]])

centroid = [ points[0], points[5] ]

file1 = open("Woah.txt", "w")
past_clust = []


for iter in range (100) :
    file1.write("Iter Num: " + str(iter)  + "\n")

    curr_clust = []
    new_clust_0 = []
    new_clust_1 = []
    counter = 1

    for point in points :

        dist1 = np.sum( (point - centroid[0])**2 )**0.5
        dist2 = np.sum( (point - centroid[1])**2 )**0.5

        file1.write("Point " + str(counter) + ": " + str(point) + " " )
        file1.write("Dist1: " + str(dist1) + " " )
        file1.write("Dist2: " + str(dist2) + "\n" )


        if dist1 < dist2 :
            curr_clust.append(0)
            new_clust_0.append(point)
        else :
            curr_clust.append(1)
            new_clust_1.append(point)

        counter += 1

    if curr_clust == past_clust :
        break
    else :
        past_clust = copy.deepcopy(curr_clust)


    new_clust_0 = np.array(new_clust_0)
    new_clust_1 = np.array(new_clust_1)

    centroid[0] = np.sum( new_clust_0, axis=0) / new_clust_0.shape[0]
    centroid[1] = np.sum( new_clust_1, axis=0) / new_clust_1.shape[0]

    file1.write("Curr Classify \n")
    file1.write(str(curr_clust)  + "\n")
    file1.write("Centroids: " + str(centroid) +"\n \n" )

file1.write("\nFinal Results \n")
file1.write( str(curr_clust) + "\n")
file1.write("Centroids: " + str(centroid) )









### Euclidean Distance, assign cluster, then compute new centroid mean. Repeat til convergence
