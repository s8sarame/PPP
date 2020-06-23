

import collections
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns

class output:
     def __init__(self,l1,l2,xlabel):
        self.l1 = l1
        self.l2 = l2
        self.xlabel = xlabel

     def plot_for_aa(self,l1,l2,x_label): #to plot the frequency against the required property in both the sets of sequences
        counter = collections.Counter(l1)
        counter2 = collections.Counter(l2)


        df = pd.DataFrame.from_dict(counter,orient='index').reset_index()
        df2 = pd.DataFrame.from_dict(counter2, orient= 'index'). reset_index()

        figure = plt.figure()
        ax = figure.subplots()
        sns.distplot(df, rug= True, hist=False, kde_kws={"label":"query sequence set"})
        sns.distplot(df2,rug=True, hist=False, kde_kws={"label":"background dataset"})
        ax.set(xlabel=x_label,ylabel='Frequency')

        return figure













