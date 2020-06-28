
import csv
from statistics import mean
from InputSequence import Input
#from backgroundata import parse_background_data
from scipy import stats
from Output import output
from numpy import std
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class SearchAA():
    '''The objective of this class is use AA Index property specified by user OR use property file uploaded by user
        and apply it to the set of sequences and compare to background data'''
    def __init__(self, inputfile, property,background):
        self.inputfile = inputfile
        self.property = property
        self.background = background



    @staticmethod
    def retrive_dict(index_id, lines): #parses required Index information from AAIndex file according to the property required
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
                                index = [str(j) for l in num for j in l]
                                mapping = dict(zip(names, index))
                        i += 1
                        line = lines[i]

                    return mapping
    @staticmethod
    def Map(dict1,sequence):



        new = ' '.join(dict1.get(l, l) for l in sequence)

        listu = [float(x) for x in new.split()]
        avg = mean(listu)
        avg_2 = round(avg,2)
        return(avg_2)

    @staticmethod
    def calculatecharge(li): #to calculate charge on peptide sequence

        charge = 0
        for aa in li:
            if aa in ('R', 'K', 'H'): #checks if sequence contains Arginine, Histidine or Lysine
                charge += 1           #increment the charge
            elif aa in ('D', 'E'): #checks if sequence contains Aspartic acid or Glutamic acid
                    charge -= 1         #decrement the charge
            else:
                charge = charge
        return charge

    @staticmethod
    def functions(list_of_sequences,dict1): #A function which calls property calculator functions to set of sequences and returns the average result
        avg_lst = []

        chargelist = []

        for sequence in list_of_sequences:

            ave = SearchAA.Map(dict1,sequence)

            avg_lst.append(ave)


        return avg_lst, chargelist

    @staticmethod
    def length(list): # Calculates the length of every sequence in set and finds it mean and standard deviation
        lengths = []
        for i in list:
            length = len(i)
            lengths.append(length)

        avg_length = mean(lengths)
        sd_ = std(lengths)
        return lengths,avg_length,sd_

    @staticmethod
    def output_(dict1,inp,bkg):
        sequences = Input.Sequence_file(inp)

        background = Input.Sequence_file(bkg)
        length1 = SearchAA.length(sequences)[0]
        mean_1 = SearchAA.length(sequences)[1]
        stdev1 = SearchAA.length(sequences)[2]

        length2 = SearchAA.length(background)[0]
        mean_2 = SearchAA.length(background)[1]
        stdev2 = SearchAA.length(background)[2]

        avg_lst1 = SearchAA.functions(sequences, dict1)[0]

        avg_background = SearchAA.functions(background, dict1)[0]

        pval = stats.ttest_ind(avg_lst1,avg_background, equal_var= False)[1]
        figure1 = output.plot_for_aa(length1, length2, "Average Length")
        figure2 = output.plot_for_aa(avg_lst1,avg_background,"Average Property")

        top = tk.Toplevel()
        top.title("Results")
        frame = tk.Frame(top)
        canvas = FigureCanvasTkAgg(figure2, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


        canvas2 = FigureCanvasTkAgg(figure1,master=frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        tk.Frame(frame, height=2, relief=tk.GROOVE, bg="black").pack(side=tk.TOP, fill=
        tk.BOTH, pady=5)

        frame.pack(side=tk.TOP, padx=10)
        msg = tk.Label(top, text="p-value for property is: {}".format(pval))
        msg.pack(side=tk.TOP)
        mean1 = tk.Label(top, text="Mean length of sequences is: {}".format(mean_1)).pack(side=tk.BOTTOM)
        mean2 = tk.Label(top, text="Mean length of background sequences is: {}".format(mean_2)).pack(side=tk.BOTTOM)
        std1 = tk.Label(top, text="Standard deviation of length of sequences is: {}".format(stdev1)).pack(
            side=tk.BOTTOM)
        std2 = tk.Label(top, text="Standard deviation of length of background sequences is: {}".format(stdev2)).pack(
            side=tk.BOTTOM)

    @staticmethod
    def AAindex_property(inputfile,propertyf, property,background): # Applies AA index property to set of sequences

        file_id = open(propertyf, 'r')
        lines = file_id.readlines()
        user_ID = property

        dict1 = SearchAA.retrive_dict(user_ID,lines)

        file_id.close()
        SearchAA.output_(dict1,inputfile,background)


    @staticmethod
    def user_property(inputfile, property,background): # Applies user property to set of sequences
        reader = csv.reader(open(property, 'r'))
        dict1 = {}
        for k,v in reader:
            dict1[k] = v

        SearchAA.output_(dict1,inputfile,background)













