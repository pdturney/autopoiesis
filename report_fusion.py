#
# Report Fusion
#
# Peter Turney, February 10, 2020
#
# Read the log file an extract information about fusion events,
# such as the fitness of each of the two seeds before fusion 
# and the fitness of the resulting fused seed.
#
# NOTE: The run that you wish to analyze must be specified by
# setting the path for "log_directory" in "model_parameters.py".
# This is different from "compare_random.py", where the path is
# set with an interactive window in Golly.
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
#
# Report file for fusion events
#
basename = os.path.basename(os.path.normpath(analysis_dir))
analysis_path = analysis_dir + "/report-fusion-" + \
  basename + ".tsv"
analysis_handle = open(analysis_path, "w", 0) 
#
# Print out a header for the result file
#
mfunc.show_message(g, analysis_handle, "\n\nReport Fusion\n\n")
mfunc.show_message(g, analysis_handle, "Format: " + \
  "<seed 0 fitness> <tab> " + \
  "<seed 1 fitness> <tab> " + \
  "<fusion fitness> <new line>\n\n")
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
# Extract the base part of the pickles. Assume that all of the 
# pickles have the same base part.
#
# "log-2019-11-15-14h-22m-30s-pickle-21.bin"  -- full file name
# --> "log-2019-11-15-14h-22m-30s"            -- base part of name
#
pickle_base_search = re.search(r'(log-.+\d\ds)-pickle-', pickle_list[0])
pickle_base = pickle_base_search.group(1)
#
# Log file containing fusion events
#
log_file_name = pickle_base + ".txt"
log_file_path = analysis_dir + "/" + log_file_name
log_file_handle = open(log_file_path, "r")
#
# Look for lines of the following form (all on one line): 
#
# "Run: 2677  Seed 0 fitness (s0): 0.494  
#             Seed 1 fitness (s1): 0.524  
#             Fusion fitness (s4): 0.033  
#             Replaced seed fitness (s5): 0.172"
#
for line in log_file_handle:
  fusion_search = re.search(r'Seed 0 fitness \(s0\)\: (\d\.\d+)\s+' + \
                             'Seed 1 fitness \(s1\)\: (\d\.\d+)\s+' + \
                             'Fusion fitness \(s4\)\: (\d\.\d+)\s+', line)
  if fusion_search:
    s0 = fusion_search.group(1)
    s1 = fusion_search.group(2)
    s4 = fusion_search.group(3)
    # write result to output file
    mfunc.show_message(g, analysis_handle, \
      str(s0) + "\t" + str(s1) + "\t" + str(s4) + "\n")
#
log_file_handle.close()
#
# Final message
#
mfunc.show_message(g, analysis_handle, "\nReport complete.\n")
analysis_handle.close()
#
#