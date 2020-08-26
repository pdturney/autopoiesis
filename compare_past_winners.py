#
# Compare Past Winners
#
# Peter Turney, April 23, 2020
#
# Compare the top seed in generation N with the top seed
# from every preceding generation. 
#
import golly as g
import model_classes as mclass
import model_functions as mfunc
import model_parameters as mparam
import numpy as np
import pickle
import os
import re
import sys
#
# -----------------------------
# Get some input from the user.
# -----------------------------
#
[pickle_dir, analysis_dir, sorted_pickle_names, \
  smallest_pickle_size] = mfunc.choose_pickles(g)
#
# -----------------------------------------------------------------
# Initialize some variables and print them to the output.
# -----------------------------------------------------------------
#
# pickles
#
num_runs = len(sorted_pickle_names)
num_generations = smallest_pickle_size
#
# let's assume there is only one run in the selected directory
#
assert num_runs == 1
#
# Initialize some parameters from model_parameters
#
width_factor = mparam.width_factor
height_factor = mparam.height_factor
time_factor = mparam.time_factor
#
# Initialize some parameters locally
#
num_trials = 2 # each pair of seeds will have this many contests
num_top = 10 # num_top Gen i seeds will compete with num_top Gen n seeds
#
# Stats analysis file
#
basename = os.path.basename(os.path.normpath(analysis_dir))
analysis_path = analysis_dir + "/compare-past-winners-" + \
  "top" + str(num_top) + "-try" + str(num_trials) + "-" + \
  basename + ".tsv"
analysis_handle = open(analysis_path, "w", 0) 
#
# Print out a header for the result file
#
mfunc.show_message(g, analysis_handle, "\n\nCompare Past Winners\n\n")
mfunc.show_message(g, analysis_handle, "width_factor = " + \
  str(width_factor) + "\n")
mfunc.show_message(g, analysis_handle, "height_factor = " + \
  str(height_factor) + "\n")
mfunc.show_message(g, analysis_handle, "time_factor = " + \
  str(time_factor) + "\n")
mfunc.show_message(g, analysis_handle, "num_trials = " + \
  str(num_trials) + "\n")
mfunc.show_message(g, analysis_handle, "num_top = " + \
  str(num_top) + "\n")
mfunc.show_message(g, analysis_handle, "path = " + \
  str(pickle_dir) + "\n\n")
mfunc.show_message(g, analysis_handle, \
  "Note the results will change slightly each time this runs.\n\n")
#
# Make a list of the pickles in pickle_dir
#
pickle_list = []
for file in os.listdir(pickle_dir):
  if file.endswith(".bin"):
    pickle_list.append(file)
#
assert len(pickle_list) == num_generations + 1
#
# Extract the base part of the pickles. Assume that all of the 
# pickles have the same base part.
#
# "log-2019-11-15-14h-22m-30s-pickle-21.bin"  -- full file name
# --> "log-2019-11-15-14h-22m-30s-pickle-"    -- base part of name
#
pickle_base_search = re.search(r'(log-.+\d\ds-pickle-)', pickle_list[0])
pickle_base = pickle_base_search.group(1)
#
# Make a list of the num_top winning seeds for each generation
#
winning_seeds = []
for gen_num in range(num_generations + 1):
  # read the pickle file for generation gen_num
  pickle_name = pickle_base + str(gen_num) + ".bin"
  pickle_path = pickle_dir + "/" + pickle_name
  pickle_handle = open(pickle_path, "rb") # rb = read binary
  pickle_data = pickle.load(pickle_handle)
  pickle_handle.close()
  # make a list of the num_top seeds in generation gen_num
  top_seeds = []
  for seed_num in range(num_top):
    top_seeds.append(pickle_data[seed_num])
  # add the top seeds to the list
  winning_seeds.append(top_seeds)
#
# Compare the num_top seeds in past generations with the
# num_top seeds in the current generation. Assume that
# the first generation has a fitness of zero, because
# it is randomly generated and there is no earlier
# generation we can compare it to.
#
for gen_num in range(num_generations + 1):
  # if this is the first generation, then its score is zero
  if (gen_num == 0):
    score = 0.0
    mfunc.show_message(g, analysis_handle, 
      str(gen_num) + "\t" + str(score) + "\n")
  # otherwise, if this is not the first generation, then ...
  else:
    # get the num_top seeds from gen_num
    new_seeds = winning_seeds[gen_num]
    # iterate through the previous generations
    score = 0.0
    for old_num in range(gen_num):
      # get the num_top seeds from old_num
      old_seeds = winning_seeds[old_num]
      # compare the old seeds to the new seeds
      raw_score = 0.0
      for new_seed in new_seeds:
        for old_seed in old_seeds:
          # new_score will range from 0 to 1
          # - new_score is the fraction of the trials that
          #   are won by new_seed
          [old_score, new_score] = mfunc.score_pair(g, \
            old_seed, new_seed, width_factor, height_factor, \
            time_factor, num_trials)
          # increment the sum raw_score
          raw_score = raw_score + new_score
      # calculate the average value of new_score over
      # the pairs of seeds in new_seeds and old_seeds
      norm_score = raw_score / (num_top * num_top)
      # adjust norm_score to range from -1 to +1
      # instead of from 0 to 1
      score = score + (2.0 * norm_score) - 1.0
    # write result to output file
    mfunc.show_message(g, analysis_handle, 
      str(gen_num) + "\t" + str(score) + "\n")
    #
  #
#
# Final message
#
mfunc.show_message(g, analysis_handle, "\nAnalysis complete.\n")
analysis_handle.close()
#
#