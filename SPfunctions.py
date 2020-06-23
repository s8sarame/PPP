from statistics import mean
import csv
from Output import output
from scipy import stats
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class SP_functions:
    ''' The objective of this class is to apply Signal peptide properties to N, H and C regions and compare to background data '''
    def polarity(self, seq):
        polar_propensity_scale = {'A': '0.00', 'R': '52.00', 'D': '49.70', 'N': '3.38', 'C': '1.48',
                              'E': '49.90', 'Q': '3.53', 'G': '0.00','H': '51.60', 'L': '0.13',
                              'I': '0.13', 'K': '49.50', 'M': '1.43', 'F': '0.35', 'P': '1.58',
                              'S': '1.67', 'T': '1.66', 'W': '2.10', 'Y': '1.61', 'V': '0.13'}

        new = ' '.join(polar_propensity_scale.get(l, l) for l in seq)
        listu = [float(x) for x in new.split()]
        avg = mean(listu)
        avg_2 = round(avg, 2)
        return (avg_2)

    def kd_hydrophobicity(self, seq):
        kd = {'A': '1.8', 'R': '-4.5', 'N': '-3.5', 'D': '-3.5', 'C': '2.5',
          'Q': '-3.5', 'E': '-3.5', 'G': '-0.4', 'H': '-3.2', 'I': '4.5',
          'L': '3.8', 'K': '-3.9', 'M': '1.9', 'F': '2.8', 'P': '-1.6',
          'S': '-0.8', 'T': '-0.7', 'W': '-0.9', 'Y': '-1.3', 'V': '4.2'}
        new = ' '.join(kd.get(l, l) for l in seq)
        listu = [float(x) for x in new.split()]
        avg = mean(listu)
        avg_2 = round(avg, 2)
        return (avg_2)



    def calculatecharge(self,li): #to calculate charge on peptide sequence

        charge = 0
        for aa in li:
            if aa in ('R', 'K', 'H'): #checks if sequence contains Arginine, Histine or Lysine
                charge += 1           #increment the charge
            elif aa in ('D', 'E'): #checks if sequence contains Aspartic acid or Glutamic acid
                    charge -= 1         #decrement the charge
            else:
                charge = charge
        return charge

    def functions(self,csv_file):
        f = open(csv_file)
        next(f)
        csv_f = csv.reader(f)
        charges = []
        polarities = []
        hydrophobicities = []
        lengths = []
        for row in csv_f:
            charges.append(self.calculatecharge(row[8]))
            polarities.append(self.polarity(row[10]))
            hydrophobicities.append(self.kd_hydrophobicity(row[9]))
            lengths.append(len(row[9]))
        avgcharge = mean(charges)
        avgpol = mean(polarities)
        avg_hyd= mean(hydrophobicities)
        avg_len = mean(lengths)
        f.close()
        return charges,polarities,hydrophobicities,lengths
    def __init__(self,inputfile,backgroundfile):
        charge1 = self.functions(inputfile)[0]
        pol1 = self.functions(inputfile)[1]
        hyd1 = self.functions(inputfile)[2]
        len1 = self.functions(inputfile)[3]

        charge2 =  self.functions(backgroundfile)[0]
        pol2 = self.functions(backgroundfile)[1]
        hyd2 = self.functions(backgroundfile)[2]
        len2 = self.functions(backgroundfile)[3]


        '''print(stats.ttest_ind(charge1,charge2))
        print(stats.ttest_ind(pol1,pol2))
        print(stats.ttest_ind(hyd1,hyd2))
        print(stats.ttest_ind(len1,len2))'''

        fig1 = output.plot_for_aa(output,len1,len2,"H-region Length")
        fig2 = output.plot_for_aa(output, charge1, charge2, "N-region charge")
        fig3 = output.plot_for_aa(output, pol1, pol2, "C-region Polarity")
        fig4 = output.plot_for_aa(output, hyd1, hyd2, "H-region Hydrophobicity")

        top = tk.Toplevel()

        top.title("Signal Peptide Results")
        frame = tk.Frame(top)


        canvas1 = FigureCanvasTkAgg(fig1, master=frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


        canvas2 = FigureCanvasTkAgg(fig2, master=frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)




        tk.Frame(frame, height=2, relief=tk.GROOVE, bg="black").pack(side=tk.TOP, fill=
        tk.BOTH, pady=5)

        frame.pack(side=tk.TOP, padx=10)

