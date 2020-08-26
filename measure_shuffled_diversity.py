#
# Measure Shuffled Diversity
#
# Peter Turney, August 9, 2020
#
# Diversity is the number of different types of ash observed.
# Here we shuffle the seeds before measuring diversity, to show
# that the structure of the seeds is essential to their diversity.
#
# (1) For each of the four layers, for each generation, calculate
# the diversity of the elite sample as a whole, averaging over
# the 12 runs. Sample size is num_runs = 12. This is a kind
# of population diversity.
#
# (2) For each of the four layers, for each generation, calculate
# the average diversity of a seed, averaging over the elite samples
# in the 12 runs. Sample size is elite_size (50) * num_runs (12)
# = 600. This is a kind of individual diversity (diversity of
# components within an average seed).
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
    "/Paper Sections/Part 4 - Shuffling/layer_" + layer_num + \
    "_shuffled_diversity.txt"
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
f.write("\n\nLog File for Shuffled Diversity Report\n\n")
f.write("generation\tavg elite diversity\tavg seed diversity\n")
#
# Iterate over the generations.
#
for gen in range(num_generations):
    #
    # Iterate over the runs
    #
    sum_elite_diversities = 0.0
    sum_seed_diversities = 0.0
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
        elite_types = set() # a set of types of objects in the pickle
        seed_diversity = list() # a list of type counts for seeds
        #
        for seed in seed_list:
            seed = seed.shuffle() # shuffle the seed
            soup = apg.Soup()
            soup.rg.setrule(rulestring)
            soup.rg.saveAllRules()
            soup.stabilise_seed(seed)
            [objects, frequencies] = soup.basic_census()
            elite_types.update(objects) # types of distinct ashes
            seed_diversity.append(len(objects)) # number of distinct ashes
        #
        sum_elite_diversities += len(elite_types) # a set, thus no duplicates
        sum_seed_diversities += mean(seed_diversity)
        #
    #
    # Report the statistics for the current generation.
    #
    avg_num_types_in_elite = sum_elite_diversities / float(num_runs)
    avg_num_types_in_seed = sum_seed_diversities / float(num_runs)
    #
    f.write("{:5d}\t{:8.2f}\t{:8.2f}\n".format( \
        gen, avg_num_types_in_elite, avg_num_types_in_seed))
    #
#
# Close file.
#
f.close()
#
#
#