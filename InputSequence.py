from Bio import SeqIO
from Bio.Alphabet import IUPAC, _verify_alphabet
from Bio.Seq import Seq
import csv
class Input:
    '''The objective of this class is to check the validity of Input sequence'''
    def __init__(self,filename,csvfile):
        self.filename = filename
        self.csvfile = csvfile
        self.Sequence_file(filename)
        self.background(csvfile)

    @staticmethod
    def Sequence_file(filename):
        valid_seq = []
        non_val_seq = []
        with open(filename) as f:
            for record in SeqIO.parse(f, "fasta"):
                li = [str(record.seq)]



                for i in li:
                    myprot = Seq(i, IUPAC.protein)
                    if (_verify_alphabet(myprot)) == True:
                        valid_seq.append(i)



                    elif(_verify_alphabet(myprot)) == False:
                        non_val_seq.append(i)

                    else:
                        print('Not Valid')

        return valid_seq
    def background(self,csv_file):
        f = open(csv_file, 'r')
        next(f)
        csv_f = csv.reader(f)
        li = []
        valid_seq2 = []
        non_val_seq2 = []
        for row in csv_f:
            li.append(row[1])

        for i in li:
            myprot = Seq(i, IUPAC.protein)
            if (_verify_alphabet(myprot)) == True:
                valid_seq2.append(i)



            elif (_verify_alphabet(myprot)) == False:
                non_val_seq2.append(i)


            else:
                print('Not Valid')

        return valid_seq2



