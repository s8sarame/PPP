
from Properties import SearchAA
from SignalPeptides import SignalPeptide
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-i",dest= "inputfile",required=True,
                    type= argparse.FileType())
parser.add_argument("-b",dest="backgroundfile", default="humansequencessp.txt",
                    type= argparse.FileType())
parser.add_argument("-p", dest="propertyfile",type=str, default="aaindex1.txt")
parser.add_argument("-d", dest="PropertyID", type=str)
args = parser.parse_args()
inputfile = args.inputfile
backgroundfile = args.backgroundfile
propertyfile = args.propertyfile
propertyid = args.PropertyID
if args.propertyfile == "aaindex1.txt":
    SearchAA.AAindex_property( inputfile.name, propertyfile,propertyid, backgroundfile.name)
else:

    SearchAA.user_property( inputfile.name, propertyfile, backgroundfile.name)
SignalPeptide(inputfile.name,backgroundfile.name)

