# Findsing-silimar-users-in-Netflix-Dataset

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

