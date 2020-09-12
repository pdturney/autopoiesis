#
# Measure Ash Frequencies
#
# Peter Turney, September 9, 2020
#
# See ash frequencies in Catagolue:
#
# https://www.conwaylife.com/wiki/Most_common_objects_on_Catagolue
#
# For each layer in model S, count how often each type
# of ash occurs. Compare these counts with the counts
# in Catagolue.
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import apgsearch_repurposed as apg
import pickle
import glob
#
# Specify the layer to process.
#
layer_num = "3"
#
# Specify the generation to process
#
generation_num = 100
#
# Log file for reporting the results (output).
#
log_file = "C:/Users/peter/Peter's Projects/autopoiesis" + \
    "/Paper Sections/Part 2 - Diversity/layer_" + layer_num + \
    "_ash_frequencies.txt"
#
# The layer of pickles to process (input).
#
pickle_layer = "C:/Users/peter/Peter's Projects/autopoiesis/" + \
    "Pickles/Layer " + layer_num
#
# Some parameters.
#
elite_size = 50 # number of seeds in a pickle
num_runs = 12 # runs range from 1 to 12
#
# Specify rule and symmetry.
#
rulestring = "B3/S23" # Game of Life
symmstring = "C1" # C1 means the soup is asymmetric
numsoups = 1 # soup count
#
# Open log file.
#
f = open(log_file, "w", 0) # 0 means no buffer, so instant results
f.write("\n\nLog File for Ash Frequency Report\n\n")
#
# Make a hash table for mapping ash types to counts.
#
ash_type_count = {}
#
# Iterate over the runs
#
for run in range(1, num_runs + 1):
    #
    # Look in the directory pickle_layer for the file
    # with the current run number. The file will match
    # the pattern "run[run]/log-...-pickle-[gen].bin". Note
    # that glob.glob returns a list, since there may be many
    # matching files, but we hope there is only one matching
    # file.
    #
    pickle_paths = glob.glob(pickle_layer + "/run" + \
        str(run) + "/log-*-pickle-" + str(generation_num) + ".bin")
    assert len(pickle_paths) == 1 # should be exactly one match
    pickle_path = pickle_paths[0] # extract the match from the list
    #
    # Load the pickle.
    # 
    pickle_handle = open(pickle_path, "rb") # rb = read binary
    seed_list = pickle.load(pickle_handle)
    pickle_handle.close()
    #
    # Iterate over the seeds in the pickle.
    #
    for seed in seed_list:
        soup = apg.Soup()
        soup.rg.setrule(rulestring)
        soup.rg.saveAllRules()
        soup.stabilise_seed(seed)
        [objects, frequencies] = soup.basic_census()
        for (obj, freq) in zip(objects, frequencies):
            if obj in ash_type_count:
                ash_type_count[obj] = ash_type_count[obj] + freq
            else:
                ash_type_count[obj] = freq
    #
#
# Count the total number of object types and the total frequency.
#
total_types = 0
total_freq = 0
#
for (obj, freq) in ash_type_count.items():
    total_types = total_types + 1
    total_freq = total_freq + freq
#
f.write("Total number of ash types = {}\n".format(total_types))
f.write("Total ash frequency = {}\n\n\n".format(total_freq))
#
# Get common names for ashes, if available.
#
soup = apg.Soup()
ash_name = {}
for obj in ash_type_count.keys():
    if obj in soup.commonnames:
        ash_name[obj] = soup.commonnames[obj][0]
    else:
        ash_name[obj] = obj # default name
#
# Sort the results by decreasing frequency.
#
sorted_keys = sorted(ash_type_count, key=ash_type_count.get, \
                     reverse=True)
for obj in sorted_keys:
    f.write("{:s}\t{:d}\n".format(ash_name[obj], \
        ash_type_count[obj]))
#
# Close file.
#
f.close()
#
#
#