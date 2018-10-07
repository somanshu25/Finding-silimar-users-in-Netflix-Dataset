# Finding-silimar-users-in-Netflix-Dataset

The motive is to find the similar users who have rated highly almost same movies. The given databse is a Netflix userbase with movies , user_id, the rating of the movie and the date when the user rated.   

In this project, we are cleaning up the Netflix database to process the data easily according to the movies rated by the suers and then find the similar users who have rated the similar movies and list all those pairs. The project is further extended to identify the closest neighbor for a new user entered as recommendation.

>>>>
Problem 1:

Statement: Clean the Data according to the given constraints and rearrange the data into ‘M’ movie
rows and ‘N’ user columns.
Approach:
1. Drop the unnecessary columns such as date from the data
2. Remove users with ratings less than 3 and who have rated more than 20 movies
3. Extract the movie_id values and movie_id indixes using the value of 9999 in rating as a reference
4. Re-index the data after extracting the movie_id and extract the unique user id from the data
5. Remove the movies with no users
6. Generate row, column, data values to generate the sparse matrix
7. Create the sparse matrix using the row index, column index and data
Results:
Sparse Matrix dimensions: [4485, 231424]

Problem 2:

Statement: To analyze random pairs of 10,000 users and calculate the average Jaccard distance,
similarity and plot the histogram of pairwise Jaccard distances
Approach:
1. Pad the matrix with zeros to increase the row size to the nearest prime number i:e 4493
2. Randomly choose 10,000 pairs from the data set following the discreet uniform distribution
3. Calculate the Jaccard distance and similarity of each pair
4. Jaccard Distance = 1 – intersection(Pair1, Pair2) / union(Pair1, Pair2)
5. Jaccard Similarity = intersection(Pair1, Pair2) / union(Pair1, Pair2)
6. Plot the histogram of the values for each pair
Results:
Average value of Jaccard Distance: 0.9804398083185061 Minimum value of Jaccard Distance: 0.33333333333333337

![histogram_plot](https://user-images.githubusercontent.com/43916672/46586957-80650300-ca53-11e8-82c8-414288cee932.png)
 
Problem 3:

Statement: Find the nearest neighbor pairs for each queried user
Approach:
We use the method of Min Hashing and Locality Sensitive Hashing to reduce the computational and spatial limits while computing the nearest neighbors

Min Hashing:
1. Permute the indexes of each row to new index with respect to the function: permuted_index = (a*x + b) % r
a = random value in range(0 to (Rows of Padded _Sparse Matrix – 1))
b = random value in range(0 to (Rows of Padded _Sparse Matrix – 1))
r = number of rows of Padded _Sparse Matrix
x = vector of index value of 1’s in each column
2. Hash Value of each column is the minimum index of 1’s in that column
3. Hence, we get one Hash value for each column of the Sparse Matrix
4. Repeat the Min Hash process for 100 iterations to obtain a table of Hash values of size
[1000, 231424]

Local Sensitivity Hashing:
1. Split the Hash Table into ‘B’ bands each consisting of r1 rows.
2. Each band is mapped to a single value according to the function:
(a1*x + b1) % r1
a1 = random value in range(0 to (Rows of Padded _Sparse Matrix – 1)) b1 = random value in range(0 to (Rows of Padded _Sparse Matrix – 1)) r1 = Huge integer value
x = vector of the elements in each band across the columns
3. The sum of each vector band is taken and the size of the Hash table is reduced to the size of [B, 231424]

Results:

Original Dataset Sample:

array([[1, 1, 1, ..., 0, 0, 0],
[0, 0, 0, ..., 0, 0, 0], 
[0, 0, 0, ..., 0, 0, 0], 
...,
[0, 0, 0, ..., 0, 0, 1], 
[0, 0, 0, ..., 0, 0, 0], 
[0, 0, 0, ..., 0, 0, 0]],
dtype=int64)
 
Hash Table Sample:
 
 array([[20,74, 1795, ..., 2577, 2577, 3709], 
[302, 1084, 2618, ..., 4174, 4174, 1830],
[ 16, 180, 2530, ..., 1015, 1015, 18],
...,
[ 705, 150, 1742, ..., 4393, 4393, 2300], 
[ 471, 18, 12, ..., 675, 675, 658],
[ 76, 76, 76, ..., 732, 732, 2175]])

Band Matrix Sample: 

array([[1236891226, 2854582886, 2192001821, ..., 2254508321, 2254508321,1696931309], 
[2513191099, 1689525747,2544410733, ..., 1905784720, 1905784720,1286734634],
.....


Problem 4:

Statement: To detect the pairs of similar users Approach:
1. Each column of the Band matrix is checked with other columns (each user with the rest) and a user is similar if any one of the band values matches at that position.
2. Similar pairs are matched to each other and they are mapped to the same list if they have Jaccard distance of less than 0.35
3. The Jaccard distance of similar pairs are calculated using the sparse matrix and not the Band Matrix
Results:
The value of Band(b1) = 20 and rows per band r1 = 5 give better results as we get less false negatives The probability of finding similar pairs is given by
P = 1 – (1 – (S ^ r1)) ^ b1
S = similarity > = 0.65
The values of r1 and b give better results with probability 0.91513
This can also be viewed in the graph. The specific values of r1 and b1 give a smaller number of false negative as compared to the other values.

![imgae_analysis](https://user-images.githubusercontent.com/43916672/46586930-27956a80-ca53-11e8-89e6-6b4e6ce96d13.png)
  
Problem 5:

Statement: Given a new user find the similar user in the dataset Approach:
1. The new user dataset is assumed to be in the following format of ‘ratings’ of size [4485, 1]
2. If the movie was rated by the user, 1 is placed at the location of the movie_id or else a 0 is in
that position.

                 movie_id1[0 or 1] | movie_id2[0 or 1] | movie_id3[0 or 1] |.... |....|movie_idn 

3. We also assume that the user has rated all is movies as 3 or above and only rated movies less
than 20
4. Min hashing and local sensitivity hashing are applied to the new user data and the Band matrix is obtained.
5. The values of a, b, r, a1, b1, r1 used are the same as the signature matrix and the band matrix of the data
6. The band values are checked against the users in the data set and if at least one bad match, the new user and the user in that column of the data set are similar
7. Then we determine the Jaccard distance to determine if the distance between them is less than 0.35
8. If the distance is less than 0.35 then the new user and the user in the dataset are similar.

Results:

Input of new user
user_new_check[0] = 1, user_new_check[189] = 1, user_new_check[455] = 1, user_new_check[466] = 1, user_new_check[561] = 1, user_new_check[690] = 1, user_new_check[1103] = 1, user_new_check[1212] = 1, user_new_check[1896] = 1, user_new_check[3948] = 1, user_new_check[4195] = 1, user_new_check[4375] = 1

Output:
The closest neighbour is: 124105
