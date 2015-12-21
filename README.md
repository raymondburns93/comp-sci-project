# comp-sci-project

Python scripts which I have recently written to automate the collection and plotting of hardware event statistics for a FFT benchmark which I am studying as part of my final year project. This was my first time using python.


More Information

Document prepared for Interim Demo

To date I have been working on automating the performance analyse process for the fft implementation.

I have created two python scripts

-get_fft_stats.py
-plot_fft_stats.py

Description of get_fft_stats.py

The purpose of this script is to collect hardware performance counter event statistics for the fft benchmark and save to an output file. This script takes a number of positional and optional arguments. The user can optionally specify the max number of threads to run. So for example if the user enters 128, the fft benchmark will be run for all threads that are powers of 2 up to and including this number of threads (i.e. 1,2,4,8,16,32,64,128). A comma seperated list of hardware events to collect is required. All arguments are used to dynamically build commands using perf to run in a subprocess. The output of perf is captured in stderr and written to an output file in an easily parseable format. The output of the fft benchmark run is sent to stdout and this is parsed to retrieve the execution time before also appending this to the output file. The output file is stored in an output subdirectory as a timestamped text file.

Description of plot_fft_stats.py

The purpose of this script is to take an input file created by the previous script and to plot graphical representations of fft statistics for hardware counter events. The script parses the input file and builds a dictionary of events and their statistics. Events per second will also be calculated and plotted. Because raw event codes can be used, I have also made use of a raw-code-translations file which contains mappings between descriptive names and raw codes for commonly used events. A dictionary of these known translations is built. Next plots are created using the Matplotlib plotting library. Each plot is saved as a png file to an output_dir. If a raw code is encountered, the translation dictionary is searched for a match and if present, its descriptive name is appended to the plot names and labels. Both total event counts and event counts per second are plotted against the number of threads.
