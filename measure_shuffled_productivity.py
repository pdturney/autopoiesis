#
# Measure Shuffled Productivity
#
# Peter Turney, August 9, 2020
#
# Productivity is the number of ashes observed. Whereas diversity
# is the number of types of ash, productivity is the number of
# tokens of ash. Here we shuffle the seeds before measuring productivity, 
# to show that the structure of the seeds is essential to their productivity.
#
# For each of the four layers, for each generation, calculate
# the average productivity of a seed, averaging over the elite samples
# in the 12 runs. Sample size is elite_size (50) * num_runs (12)
# = 600. This is the productivity of an individual seed (the average
# number of ash components of a seed).
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import apgsearch_repurposed as apg
import pickle
import glob
from statistics import mean
#
# Specify the layer to process.
#
layer_num = "4"
#
# Log file for reporting the results (output).
#
log_file = "C:/Users/peter/Peter's Projects/autopoiesis" + \
    "/Paper Sections/Part 4 - Shuffling/layer_" + \
    layer_num + "_shuffled_productivity.txt"
#
# The layer of pickles to process (input).
#
pickle_layer = "C:/Users/peter/Peter's Projects/autopoiesis/" + \
    "Pickles/Layer " + layer_num
#
# Some parameters.
#
num_generations = 101 # generations range from 0 to 100
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
f.write("\n\nLog File for Productivity Report\n\n")
f.write("generation\tavg seed productivity\n")
#
# Iterate over the generations.
#
for gen in range(num_generations):
    #
    # Iterate over the runs
    #
    sum_seed_productivities = 0.0
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
            str(run) + "/log-*-pickle-" + str(gen) + ".bin")
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
        seed_productivity = list() # a list of token counts for seeds
        #
        for seed in seed_list:
            seed = seed.shuffle() # shuffle the seed
            soup = apg.Soup()
            soup.rg.setrule(rulestring)
            soup.rg.saveAllRules()
            soup.stabilise_seed(seed)
            [objects, frequencies] = soup.basic_census()
            total_ash_count = sum(frequencies) # number of tokens of ash
            seed_productivity.append(total_ash_count)
        #
        sum_seed_productivities += mean(seed_productivity)
        #
    #
    # Report the statistics for the current generation.
    #
    avg_num_tokens_in_seed = sum_seed_productivities / float(num_runs)
    #
    f.write("{:5d}\t{:8.2f}\n".format(gen, avg_num_tokens_in_seed))
    #
#
# Close file.
#
f.close()
#
#
#