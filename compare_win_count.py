#
# Compare Win Count
#
# Peter Turney, January 24, 2020
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
# Initialize some parameters from model_parameters
#
pickle_dir = mparam.log_directory
analysis_dir = mparam.log_directory
num_generations = mparam.num_generations
width_factor = mparam.width_factor
height_factor = mparam.height_factor
time_factor = mparam.time_factor
#
# Initialize some parameters locally
#
# each pair of seeds will have this many contests
num_trials = 50
# this many wins is significant at 95% level 
# (p = 0.0325, Binomial Exact Test)
num_wins = 32
#
# Stats analysis file
#
basename = os.path.basename(os.path.normpath(analysis_dir))
analysis_path = analysis_dir + "/compare-win-count-" + \
  basename + ".tsv"
analysis_handle = open(analysis_path, "w", 0) 
#
# Print out a header for the result file
#
mfunc.show_message(g, analysis_handle, "\n\nCompare Winners\n\n")
mfunc.show_message(g, analysis_handle, "width_factor = " + \
  str(width_factor) + "\n")
mfunc.show_message(g, analysis_handle, "height_factor = " + \
  str(height_factor) + "\n")
mfunc.show_message(g, analysis_handle, "time_factor = " + \
  str(time_factor) + "\n")
mfunc.show_message(g, analysis_handle, "num_trials = " + \
  str(num_trials) + "\n")
mfunc.show_message(g, analysis_handle, "num_wins = " + \
  str(num_wins) + "\n")
mfunc.show_message(g, analysis_handle, "path = " + \
  str(pickle_dir) + "\n\n")
mfunc.show_message(g, analysis_handle, \
  "Note the numbers will change slightly each time this runs.\n\n")
#
# Make a list of the pickles in pickle_dir
#
# We assume that the directory pickle_dir contains the pickles from
# only one single run of Model-T. That is, all of the pickles will
# have the same date and time stamp as part of their file names.
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
# Make a list of the winning seed for each generation
#
winning_seeds = []
for pickle_num in range(num_generations + 1):
  pickle_name = pickle_base + str(pickle_num) + ".bin"
  pickle_path = pickle_dir + "/" + pickle_name
  pickle_handle = open(pickle_path, "rb") # rb = read binary
  pickle_data = pickle.load(pickle_handle)
  pickle_handle.close()
  # seeds are sorted in order of decreasing score, so the
  # first seed is the winning seed for this pickle
  winning_seed = pickle_data[0]
  winning_seeds.append(winning_seed)
#
# Calculate the score for each winning seed by comparing
# it with the preceding seeds. Let's say that the first
# seed (generation 0) has a fitness of zero. This is 
# reasonable, since the first seed is randomly generated
# and there is no earlier generation we can compare it to.
#
for new_seed_num in range(num_generations + 1):
  # if this is the first seed, then its score is zero ...
  if (new_seed_num == 0):
    new_seed_score = 0
    mfunc.show_message(g, analysis_handle, 
      str(new_seed_num) + "\t" + str(new_seed_score) + "\n")
  # if this is not the first seed ...
  else:
    new_seed = winning_seeds[new_seed_num]
    # initialize sum of scores
    new_seed_score = 0
    # compare all the old winners to new_seed
    for old_seed_num in range(new_seed_num):
      old_seed = winning_seeds[old_seed_num]
      [old_score, new_score] = mfunc.score_pair(g, \
        old_seed, new_seed, width_factor, height_factor, \
        time_factor, num_trials)
      # increment sum of scores
      if (new_score >= float(num_wins) / num_trials):
        new_seed_score = new_seed_score + 1
    # write result to output file
    mfunc.show_message(g, analysis_handle, 
      str(new_seed_num) + "\t" + str(new_seed_score) + "\n")
    #
  #
#
# Final message
#
mfunc.show_message(g, analysis_handle, "\nAnalysis complete.\n")
analysis_handle.close()
#
#