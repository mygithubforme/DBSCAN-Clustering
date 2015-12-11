from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
import math

NOISE= None

#return true if distance between two points are less than epsilon value
def isNearby(x_index,y_index,x_i,y_i,eps):
   return math.sqrt(pow((x_index - x_i), 2) + pow((y_index - y_i), 2)) <= eps


#get numbers of points around current point
def num_of_points(x,y,index,eps):
    points_nearby=[]
    for i in range(len(x)):
        if isNearby(x[index],y[index],x[i],y[i],eps):
            #print i
            points_nearby.append(i)
    #print "---------------------------------"
    return points_nearby



def getRegion(cluster_set,index,x,y,eps,minPoints,cluster_id):
    points_nearby=num_of_points(x,y,index,eps)
    #Lable as noise if nearby(reachable) points are less than minimum required points 
    if len(points_nearby) < minPoints:
        cluster_set[index]=NOISE
    else:
    #if nearby points are greater than required minimum points then assign that point to current cluster.
        cluster_set[index]=cluster_id
        for i in points_nearby:
            cluster_set[i]=cluster_id
        
        while len(points_nearby) >0:
            nearbyPoints_of_insider=num_of_points(x,y,points_nearby[0],eps)
            if len(nearbyPoints_of_insider) >= minPoints:
                for i in range(len(nearbyPoints_of_insider)):
                    temp=nearbyPoints_of_insider[i]
                    if cluster_set[temp]==False or cluster_set[temp]==NOISE:
                        if cluster_set[temp]==False:
                            points_nearby.append(temp)
                        cluster_set[temp]=cluster_id
            points_nearby=points_nearby[1:]
        return True
                            
                

def dbscan(array_data,eps,minPoints,x,y):
    array_data_len1 = len(array_data)
    cluster_set=[False] * array_data_len1
    cluster_id=1
    
    for index in range(array_data_len1):
        if cluster_set[index]== False:
            #print index
            #get the region around perticular point
            if getRegion(cluster_set,index,x,y,eps,minPoints,cluster_id):
                cluster_id = cluster_id + 1
    
    return cluster_set,cluster_id
    
    
def main():
    #Read the data from the data file
    array_data =genfromtxt("D:\\UTA\\5334\\Proj 2\\att.csv",delimiter=",")
    U,s,Vt = linalg.svd(array_data,full_matrices=False)
    x=[]
    y=[]
    data_class=[]
    final_cluster_set=[]
    count=0
    array_data_len=len(array_data)
    eps=0.05 #epsilon value
    minPoints = 4 #Minimum points required to for a cluster
    for i in range(array_data_len):
        data_class.append(array_data[i][644])
        x.append(U[i][0])
        y.append(U[i][1])
    
    #call DBSCAN
    final_cluster_set,total_num_cluster = dbscan(U,eps,minPoints,x,y)  
    #print array of cluster
    print "Following is the array represent the cluster assigned from 1 to 30 point:"
    print final_cluster_set
    print "None indicates outlier in the graph"
    #plot data having class 1 with RED "+" sign, class 2 with BLUE "*" sign, class 3 with BLUE ".", NOISE with YELLOW PENTAGON.
    for i in range(array_data_len):
        if final_cluster_set[i]==1:
            plt.scatter(x[i], y[i], marker='+',c='r')
            if data_class[i]==1:
                count+=1
        elif final_cluster_set[i]==2:
            plt.scatter(x[i], y[i], marker='*',c='b')
            if data_class[i]==2:
                count+=1
        elif final_cluster_set[i]==3:
            plt.scatter(x[i], y[i], marker='.',c='b')
            if data_class[i]==3:
                count+=1
        else:
            plt.scatter(x[i], y[i], marker='p',c='y')
    
    print "Accuracy = " +str((count/float(len(array_data))*100.0))+"%"
            
    plt.axis([-0.23, -0.14, -0.32, 0.18])
    plt.show()
        
main()
    #for i in range(len(array_data)):
    #    if data_class[i]==1:
    #        plt.scatter(x[i], y[i], marker='+',c='r')
    #    elif data_class[i]==2:
    #        plt.scatter(x[i], y[i], marker='*',c='b')
    #    else:
    #        plt.scatter(x[i], y[i], marker='.',c='y')
    #        
    #plt.axis([0, 8.5, 0, 5])
    #plt.show()
    #cluster = []
    
    
