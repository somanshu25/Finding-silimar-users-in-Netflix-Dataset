import pandas as pd
import numpy as np
import datetime
import time
import random
from scipy.sparse import find
from scipy.sparse import dok_matrix
from scipy.sparse import csr_matrix
import csv
import itertools
import matplotlib.pyplot as plot
import seaborn as sns

#************************ Part a***********************#
#time_part_1 = time.time()
df1=pd.read_csv('Netflix_data.txt',names=['movie_id','rating','date'])
df1=df1.drop(df1.columns[2],axis=1)
#print(df.head)

df1.fillna(9999,inplace=True)
df1 = df1[df1['rating']>=3]

#df1=df.copy()
#df3=df.copy()


#k=df3['movie_id'].value_counts()
df1['freq'] = df1.groupby('movie_id')['movie_id'].transform('count')
df1=df1[df1['freq']<=20]
df1 = df1.reset_index();
#print(df1)
#print(df3.shape)

#df1=df1[df['rating']!=0]

#df0 = df3.copy()
index1=df1[df1['rating']==9999].index.tolist()
tp = df1.shape[0]
index1.append(tp)

mv_ini= np.array(index1)

#arr_ind=np.arange(1,len(mvlist_orig)+2)
#print(arr_ind[-3:])

#print(mv_ini)
mv_A = np.pad(mv_ini,(1,0),'constant')
mv_B = np.pad(mv_ini,(0,1), 'constant')
#print(mv_A[0:10])
#print(mv_B[0:10])
mv_C = mv_B - mv_A
mv_C=mv_C[:-1]
#print(mv_ini[-1])
mv_final_index= mv_ini[mv_C==1]

#print(mv_final_index)
#df01=df0.copy()
df1=df1.drop(df1.index[mv_final_index.tolist()])

df1=df1.reindex()

#print(df1)
mv_index_fn=df1[df1['rating']==9999].index.tolist()
tp = df1.shape[0]
mv_index_fn.append(tp)
#df1=df1.loc[df1['rating']==9999]
#mvlist_orig=df1['movie_id'].tolist()
#print(mvlist_orig)
df1=df1[df1['rating']!=9999]

user_id1 = df1['movie_id'].tolist()
mv_id_l=df1.movie_id.unique()
#print(len(mv_id_l))
#print(len(user_id1))
j=0
#l = []
l1=[]
for i in range(len(mv_index_fn)-1):
    head=mv_index_fn[i]
    tail=mv_index_fn[i+1]-1
    l= (j*np.ones(tail-head)).tolist()
    l1.extend(l)
    j=j+1
    
#print(len(l1))
data = np.ones(len(l1)).tolist()

keyMap = {}
newList = []
v = -1
for idv in user_id1:
    try:
        index = keyMap[idv]
        newList.append(index)
    except:
        v = v+1
        keyMap[idv] = v
        newList.append(v)



data = np.array(data,dtype=int)
l1 = np.array(l1,dtype=int) 
#mtx = csr_matrix((data, (l1, newList)),shape=(len(mv_index_fn),len(l1))).toarray()
mtx = csr_matrix((data, (l1, newList)))
#tmp = mtx[mtx!=0]
print(mtx.shape)
   

#******** *************************** Part 2 *****************************

#time_part_2= time.time()

list1=[]
[D,E,data_one] = find(mtx)
F = np.unique(E,return_counts=True)
k=0
user_key_index={}
j=0
for k in range(mtx.shape[1]):
    user_key_index[k]= (D[j: j + F[1][k]]).tolist()
    j=j+F[1][k]

def jacc_distance_new(num1,num2):
    #print("Time 1:", (time.time()-start_time6))
    user1 = user_key_index[num1]
    #print("Time 2:", (time.time()-start_time6))
    user2 = user_key_index[num2]
    #print("Time 3:", (time.time()-start_time6))
    m11 = len(set(user1) & set(user2))
    #print("Time 4:", (time.time()-start_time6))
    
    
    m1 = len(set(user1+user2))
    
    jd = 1 - (m11/m1)
    #print(jd)
    #print("Time 6:", (time.time()-start_time6))
    return jd

for i in range(10000):
    number = random.randint(0,mtx.shape[1])
    number2 = random.randint(0,mtx.shape[1])

    jd= jacc_distance_new(number,number2)
    list1.append(jd)


sns.set()
plot.hist(list1, bins = 20)
print("Average value of Jaccard Distance: ",sum(list1)/len(list1))
print("Minimum value of Jaccard Distance: ",min(list1))

#plot.axis([0,1.3,0,9000]) 
#axis([xmin,xmax,ymin,ymax])

#plot.xlabel('Jaccard Distance')
#plot.ylabel('Number of pairs')
#plot.show()


#****************************** Part 3 & 4 *****************************

#time_part_3 = time.time()
nearest_prime = 4493
no_of_hashes = 100
mtx2 = csr_matrix((data, (l1, newList)),shape=(nearest_prime,mtx.shape[1]))
signature_matrix = np.empty([no_of_hashes,mtx2.shape[1]],dtype=int)
ts=time.time()
R1= mtx2.shape[0]

l_a=[]
l_b=[]


#mtk = dok_matrix((mtx2.shape[1],20),dtype=int)
ts = time.time()
for i in range(no_of_hashes):
    
    a = np.random.randint(R1)
    b = np.random.randint(R1)
    l_a.append(a)
    l_b.append(b)
    
    permute = (a*D + b)%R1
    
    k=0
    j=0
    while(k < mtx2.shape[1]):
        h= np.min(permute[j: j + F[1][k]])
        j= j + F[1][k]
        signature_matrix[i,k] = h
        k = k+1
    
#print(user_key_index)
#print("Time:", time.time()-ts)

B=20
r=5


s_a=[]
s_b=[]
R2 = 982451653
m = 0
sum_bands =np.empty([B,mtx2.shape[1]],dtype=int)
sig_mat2= signature_matrix.copy()
for k in range(B):
    #sig_mat2 = signature_matrix[m:m+r,:]
    for i in range(r):
        a = np.random.randint(R2)
        b = np.random.randint(R2)
        s_a.append(a)
        s_b.append(b)
        sig_mat2[m+i,:] = (a*(sig_mat2[m+i,:]) + b)%R2
    sum_row= np.sum(sig_mat2[m:m+r,:],axis=0)
    sum_bands[k,:] = sum_row
    m=m+r



#time_after_4=time.time()
#B = 5;
#Finding Similar Pairs


nested_list = list()

for k in range(B):
	list_temp = ([(np.where(sum_bands[k] == element)[0]).tolist() for element in np.unique(sum_bands[k])])
	# print(list_temp)

	for l in list_temp:
		if(len(l) >=2):
			nested_list.extend(list(itertools.combinations(l, 2)))

	# for i in range(cols):
	# 	for j in range(i+1, cols):
	# 		if(band_matrix[k][i] == band_matrix[k][j]):
	# 			nested_list.extend({i, j})

unique_pairs = nested_list
# print(uni_pairs)
unique_pairs.sort()
unique_pairs = list(unique_pairs for unique_pairs,_ in itertools.groupby(unique_pairs))
# print(uni_pairs)

inv_map = {v: k for k, v in keyMap.items()}

#Removing False positives
finalPairs = []
time_after_5 = time.time()
for k in range(len(unique_pairs)):
    #if (k%10000 == 0):
    #    print("Done ",k, " iterations : Time :", (time.time()-start_time6))
        
    if(jacc_distance_new(unique_pairs[k][0], unique_pairs[k][1]) < 0.35):
        #print("Hello")
        pairlist=[]
        pairlist=[inv_map[unique_pairs[k][0]],inv_map[unique_pairs[k][1]]]
        finalPairs.append(pairlist)



time_after_6 = time.time()
listPairs = []

with open('similarPairs_new.csv','w') as writeFile:
  similarWriter = csv.writer(writeFile, delimiter=',')

  for i in range(len(finalPairs)):
    similarWriter.writerow([finalPairs[i][0], finalPairs[i][1]])


#with open('similarPairs_new.csv','w') as writeFile:
#  similarWriter = csv.writer(writeFile, delimiter=',')

#  for i in range(len(finalPairs)):
#    listPairs = list(finalPairs[i])
        
#    for j in range(len(listPairs)):
#      similarWriter.writerow([i, listPairs])




#*********************************** Part-5 *************************

#time_after_7 = time.time()
    
    
def check_test():
    user_new_check = np.zeros(4493)
    user_new_check[0] = 1
    user_new_check[189] = 1
    user_new_check[455] = 1
    user_new_check[466] = 1
    user_new_check[561] = 1
    user_new_check[690] = 1
    user_new_check[1103] = 1
    user_new_check[1212] = 1
    user_new_check[1896] = 1
    user_new_check[3948] = 1
    user_new_check[4195] = 1
    user_new_check[4375] = 1
    return user_new_check
    
#user_new = check_test()      * For checking the test case


# Take the input from the user......
user_new = np.random.randint(2, size =  mtx.shape[0])
          
#user_new = mtx2[:,45683]
hash_newUser = np.empty([no_of_hashes,1],dtype=int)


user_new = user_new.reshape(-1,1)

user_new = np.pad(user_new,((0,8),(0,0)),'constant')


r1 = user_new.shape[0]
#print(user_new.shape)
user_index = np.where(user_new == 1)
for i in range(100):
    
    a=l_a[i]
    b=l_b[i]
    
    
    permuted_index_newUser = (a*user_index[0] + b)%r1 
    

    hash_newUser[i,0] = np.min(permuted_index_newUser)
    
    
B = 20
r = 5

R = 982451653
m = 0
counter=0
sum_band_new_user =np.empty([B,1],dtype=int)
sig_mat2 = hash_newUser.copy()
ts=time.time()
for k in range(B):
    #sig_mat2 = hash_newUser[m:m+r,0]
    for i in range(r):
        a = s_a[counter]
        b = s_b[counter]
        counter=counter + 1
        #a = np.random.randint(R)
        #b = np.random.randint(R)
        sig_mat2[m+i, :] = (a*(sig_mat2[m+i, :]) + b)%R
    sum_row= np.sum(sig_mat2[m:m+r, :],axis=0)
    sum_band_new_user[k,:] = sum_row
    m=m+r   

       
similar_sum = sum_bands[:,:] - sum_band_new_user[:]
jacc = []
[X,Y] = np.where(similar_sum==0)
Y = np.unique(Y)
def jacc_distance_check(num1,temp):
    #print("Time 1:", (time.time()-start_time6))
    user1 = user_key_index[num1]
    #print("Time 2:", (time.time()-start_time6))
    #user2 = user_key_index[num2]
    #print("Time 3:", (time.time()-start_time6))
    m11 = len(set(user1) & set(temp))
    #print("Time 4:", (time.time()-start_time6))
    
    
    m1 = len(set(user1+temp))
 
    jd = 1 - (m11/m1)
    #print(jd)
    #print("Time 6:", (time.time()-start_time6))
    return jd


min_jacc = 1;
closest_neighbour = -1;
for i in Y:
    jacc_dist = jacc_distance_check(i,user_index[0].tolist())
    if (jacc_dist < min_jacc):
        min_jacc = jacc_dist
        closest_neighbour = i

if(closest_neighbour==-1):
    print("No close neigbour found")        
    #jacc.append([i, 1-(intersection / union)])
else:      
    print("The closest neighbour is: ",inv_map[closest_neighbour])
#print(min_jacc)
