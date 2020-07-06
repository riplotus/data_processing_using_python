# Data processing with python  course exercises.

Here includes the following data processing functions using python. 
For all functions, the libraries used include: os, pandas. 

1. ftpDownloader: downloading a batch of compressed \*.gz files from given ftp url. Used python package: ftplib.

2. extractFiles: extracting the \*.gz files. Used python package: glob, patoolib.

3. addField: reading a .csv file as a data frame, adding a field, and save it to a .csv file. Used python package: glob, pandas.

4. concatenate: concatenating a batch of .csv files which share the same columns, and save the results into a .csv file. Used python package: glob, pandas.

5. merge: merging a .csv file and a .txt file based on given keys.  

6. pivot: data aggregation, reading a .csv file, chosing the needed columns and save it as a table, and saving it as a .csv file. Used python package: pandas, Numpy.

7. plot: visualizin data. Used python packages: maplotlib.pyplot

8. kml: mapping spatial data, creating google earth files using python, adding user interaction by _input()_.  Used python package: simplekml

In the end, these functions were put together. The all_func.py was then imported to python as a module. 
