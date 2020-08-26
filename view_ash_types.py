#
# View Ash Types
#
# Peter Turney, August 21, 2020
#
# Uses a modified form of Adam P Goucher's Ash Pattern 
# Generator (Apgsearch) to compare the demographics of
# different populations of organisms that have formed
# in a model of the evolution of symbiosis (Model-S).
#
# Load a seed from a pickle generated by Model-S and
# use routines borrowed from "apgsearch-2015-05-25.py" to 
# run the seed and analyze the resulting soup.
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import apgsearch_repurposed as apg
import pickle
import time
import hashlib
import datetime
#
# Ask the user to select a pickle.
#
g.note("You will be asked to select a pickled seed file.\n" + \
       "The top seed in the file will be inserted into Golly.\n" + \
       "Ash Pattern Generator (apgsearch) will run Golly and\n" + \
       "present a summary of the ash that it finds.")
#
pickle_path = g.opendialog("Select a pickled seed file (*.bin)", \
  "(*.bin)|*.bin", g.getdir("app"))
#
# Read the pickle file.
#
pickle_handle = open(pickle_path, "rb") # rb = read binary
pickle = pickle.load(pickle_handle)
pickle_handle.close()
#
# Select the top seed from the pickle file.
#
seed = pickle[0]
#
# Specify rule and symmetry.
#
rulestring = "B3/S23"
symmstring = "C1" # C1 means the soup is asymmetric
numsoups = 1 # soup count
#
# Create associated rule tables.
#
soup = apg.Soup()
soup.rg.setrule(rulestring)
soup.rg.saveAllRules()
#
# Make an ID for the soup.
#
soupid = datetime.datetime.now().isoformat()
#
# Make a soup from a seed.
#
soup.stabilise_seed(seed)
#
# Write census as tab-separated value (.tsv) file.
#
spreadsheet_path = "C:/Users/peter/Peter's Projects" + \
  "/autopoiesis/Paper Sections/Part 2 - Diversity/test.tsv"
#
soup.spreadsheet_census(spreadsheet_path, numsoups, soupid, symmstring)
#
#