import pandas as pd

from Bio import SeqIO
from SPfunctions import SP_functions
import subprocess
class SignalPeptide:
    ''' The aim of this class is to use the result from Phobius and apply it to our set of sequences
    to find the Signal Peptide regions and its respective N, H and C regions
    function parse_phobius: takes in the result file from Phobius and parses the information to
                            (1) identify whether sequence contains Signal peptides
                            (2) obtain the numeric positions of Signal peptide, N, H and C regions
                            (3) outputs a CSV file with sequence ID, numerical start and end positions of N, H and C regions
                            function find_regions: takes in the parsed Phobius result file and set of sequence in Fasta format and outputs
                            a CSV file containg the sequence ID, sequence, it's Signal Peptide, N, H and C regions '''
    # TODO automatically link to Phobius download result
    def parse_phobius(self,result_file,opfilename):
        sq_cols = ['ID', 'N-Region start', 'N-Region end','H-Region start', 'H-Region end', 'C-Region start', 'C-Region end'] #creates column headers for csv file
        sq_file = pd.DataFrame(columns=sq_cols) #uses pandas dataframe
        with open(result_file, 'r') as f:
            nregionstart = 0
            nregionend = 0
            hregionstart = 0
            hregionend = 0
            cregionstart=0
            cregionend = 0
            ID = ''

            for line in f:

                if 'ID' in line: #parses the ID of the sequence from result file
                    ID = line[2:].strip()
                elif 'N-REGION' in line: #checks if sequence has SP and parses out the N region positions
                    nregionstart = int(line[11:22])
                    nregionend = int(line[23:28])
                elif 'H-REGION' in line: #parses out the H region positions
                    hregionstart = int(line[11:22])
                    hregionend = int(line[23:28])
                elif 'C-REGION' in line: #parses out the C region positions
                    cregionstart = int(line[11:22])
                    cregionend = int(line[23:28])


                    sq_file = sq_file.append(pd.Series(
                        [ID,nregionstart,nregionend,hregionstart,hregionend,cregionstart,cregionend],index=sq_cols), ignore_index=True)

        return sq_file.to_csv(opfilename, header=True, index=False) #converts pandas data fram to CSV file and returns it

    def find_regions(self,parsed_file, sequence_file,opfilename):
        dict_seq = {}
        with open(sequence_file) as seqfile: #creates a dictionary from sequence fasta file where key is the sequence ID and value is the sequence in string format
            for record in SeqIO.parse(seqfile, "fasta"):
                dict_seq[str(record.id)] = str(record.seq)

        # New code here 
        phoebius_df = pd.read_csv(parsed_file)
        sequences_df = pd.DataFrame.from_dict(dict_seq, columns=["Sequence"], orient="index")
        sp_file = phoebius_df.join(sequences_df, on="ID", how="inner")

        sp_file["N_seq"] = sp_file.apply(lambda row: row.Sequence[row["N-Region start"]-1:row["N-Region end"]], axis=1)
        sp_file["H_seq"] = sp_file.apply(lambda row: row.Sequence[row["H-Region start"] - 1:row["H-Region end"]], axis=1)
        sp_file["C_seq"] = sp_file.apply(lambda row: row.Sequence[row["C-Region start"] - 1:row["C-Region end"]], axis=1)


        return sp_file.to_csv(opfilename, header=True, index=False)#creates a csv file with ID, sequence, SP and N,H and C regions and returns it

    def __init__(self,inputfile,bfile):
        p = subprocess.Popen(["perl", "phobius.pl", inputfile], stdout=open('out.txt', 'wb'))
        out_text = p.communicate()
        self.parse_phobius('out.txt',"phobius_result_parsed.csv")

        self.find_regions("phobius_result_parsed.csv",inputfile,"reg.csv")

        p2 = subprocess.Popen(["perl", "phobius.pl", bfile], stdout=open('back_out.txt', 'wb'))
        out_text2 = p2.communicate()
        self.parse_phobius('back_out.txt',"back_phobius_result_parsed.csv")

        self.find_regions("back_phobius_result_parsed.csv", bfile,"back_reg.csv")

        SP_functions("reg.csv","back_reg.csv" )
