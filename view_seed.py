#
# View Seed
#
# Peter Turney, August 9, 2020
#
# Load a seed from a pickle and display it
# in Golly.
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import pickle
#
# Set the colours so they are suitable for printing.
# The background should be light and the foreground 
# should be dark.
#
g.setcolors([0,255,255,255,1,0,0,0])
#
# Ask the user to select a pickle.
#
g.note("You will be asked to select a pickled seed file.\n" + \
       "The top seed in the file will be inserted into Golly.")
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
# Write the seed into Golly.
#
for x in range(seed.xspan):
    for y in range(seed.yspan):
        state = seed.cells[x][y]
        g.setcell(x, y, state)
#
# Fit the pattern to the viewport.
#
g.fit()
#
#
#