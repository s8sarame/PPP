import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import NearestCentroid
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
'''
Objective of this class is to cluster the AA Index database based on the AA Indices. 
The final output is 6 different clusters and the names of headers belonging to each cluster
    '''
class cluster():

    def make_dict(self,index_id,lines): #parses AA Indices from database

        for i in range(0, len(lines)):
            line = lines[i]
            if len(line) > 0 and line[0] == 'H':
                header = line[2:].strip('\n')
                if header == index_id:
                    i += 1
                    line = lines[i]
                    while line[0] != '/' and line[1] != '/':
                        if line[0] == 'D':
                            description = line[2:].strip('\n')
                        elif line[0] == 'A':
                            authors = line[2:].strip('\n')
                        elif line[0] == 'T':
                            title = line[2:].strip('\n')
                        elif line[0] == 'J':
                            journal = line[2:].strip('\n')
                        elif line[0] == 'C':
                            while line[0] != 'I':
                                i += 1
                                line = lines[i]
                                # correlations = None
                            if line[0] == 'I':
                                names = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', \
                                         'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', \
                                         'T', 'W', 'Y', 'V']
                                i += 1
                                line = lines[i:i + 2]
                                num = [l.split() for l in line]
                                index = [(j) for l in num for j in l]
                                mapping = dict(zip(names, index))

                                zipdict = {}
                                zipdict[header] = mapping #dictionary containing Header as the key and AA Indices as values

                        i += 1
                        line = lines[i]
                    return zipdict

    def gen_rawdata(self, file):
        file_id = open(file, 'r')
        lines = file_id.readlines()
        aaindex_dict = {}
        d2l = []
        id_list = []
        for i in range(0, len(lines)):
            line = lines[i]
            if len(line) > 0 and line[0] == 'H':
                header = line[2:].strip('\n')
                user_ID = header
                dicts = self.make_dict(user_ID, lines)
                aaindex_dict.update(dicts)  # Compiles 566 Indices into one dictionary
                x = []

                for k, v in dicts.items():
                    id_list.append(k)
                    current_list = []
                    for current_val in v.values():  # Replaces NA values with 0
                        if current_val != 'NA':
                            current_list.append(current_val)
                        else:
                            current_list.append(0)
                    x.extend(current_list)
                    x = np.array(x).astype(np.float)

                    d2l.append(x)  # creates a 2d ND array from the dictionary values for clustering

        data = np.array(d2l)
        file_id.close()
        return data,id_list
    def find_nearest(self,list1,index,master_list1):
        dist_list = []
        for i in master_list1:
            if index == i[2]:
                diff = (list(list1 - i[1]))

                avg_diff = np.mean(diff)
                dist_list.append(avg_diff)
            else:
                dist_list.append(0)

        min_dist = min(dist_list)

        min_dist_index = dist_list.index(min_dist)

        return master_list1[min_dist_index][0]

    def centroid_fun(self,label, ndarr):
        centroid_dict = dict ()
        centroid_dict[label] = [np.mean(ndarr, axis=0)]
        return centroid_dict


    def __init__(self):



        '''Z = linkage(data, method='ward', metric='euclidean')

        fig = plt.figure(figsize=(25, 10))
        plt.title("AA Index Cluster Dendrogram( Euclidean )")
        plt.xlabel("Indices")
        dn = dendrogram(Z)
        plt.show()'''
        raw_ndarr = self.gen_rawdata("aaindex1.txt")[0]
        id_list = self.gen_rawdata("aaindex1.txt")[1]
        clustering = AgglomerativeClustering(n_clusters=5, affinity='cosine',linkage='complete').fit(raw_ndarr) #Clusters Indices based on their Manhattan distance
        label_list = clustering.labels_ #stores the headers into a separate list





        cluster_list = list()
        for i in range(0,len(id_list)): # creates a list of AAIndices in each cluster
            cluster_list.append((id_list[i],raw_ndarr[i],label_list[i]))

        call_dict = dict()
        for (prop_name, ndarr, label) in cluster_list:
            if label not in call_dict.keys():
                call_dict[label] = [ndarr]
            else:
                call_dict[label].append(ndarr)

        centroid_list = list()
        for k,v in call_dict.items():
            centroid_list.append(self.centroid_fun(k,v))

        prop_list = dict()
        for i in centroid_list:
            for k,v in i.items():

                prop_set = self.find_nearest(list(v), k, cluster_list)
                prop_list[k] = prop_set
        print(prop_list)



        '''plt.figure(figsize=(15,12))
        plt.scatter(data[:,0],data[:,1], c = label_list, cmap='rainbow')
        plt.show()'''

a = cluster()