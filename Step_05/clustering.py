from sklearn.cluster import KMeans

'''def cluster_pixels (matrix : list) -> list :

    x, y, data_size = matrix.shape
    tmp = matrix.reshape((x*y,data_size))
    kmeans = KMeans(n_clusters=5,random_state=0).fit(tmp)  
    print( "CLUSTERING : DONE")
    for i,value in enumerate(tmp):
        group = kmeans.labels_[i]
        val = kmeans.cluster_centers_[group]
        #print(group , "   ", val)
        tmp[i] = val
        
    
    tmp = tmp.reshape((x,y,data_size))
    return tmp'''



def cluster_pixels (matrix : list) :
    y, x, data_size = matrix.shape
    tmp = matrix.reshape((x*y,data_size))
    kmeans = KMeans(n_clusters=5).fit(tmp)  
    print( "CLUSTERING : DONE")
    for i,value in enumerate(tmp):
        group = kmeans.labels_[i]
        val = kmeans.cluster_centers_[group]
        tmp[i] = val
        
    
    tmp = tmp.reshape((y,x,data_size))
    #return tmp
    return kmeans
    






    