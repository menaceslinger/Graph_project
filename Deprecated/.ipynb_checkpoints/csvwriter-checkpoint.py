
import csv


class CustomCSV:
    '''
    Custom CSV Writer for writing to csvs
        cols: The name of the header columns to write to the csv. Defaults to both performance metrics and properties
        dir_path: Relative directory to save to. Should end with "/". Defaults to "csvs" folder
    '''

    # Default column names
    PROPERTIES = ["Number of nodes",
                  "Number of Edges", "Average Degree", "Density"]
    PERFOMANCE_METRICS = ["Cut-Ratio",
                          "Avg. internal density", "Coverage", "Performance", "Modularity","Execution Time"]
    ALL_HEADER = PROPERTIES + PERFOMANCE_METRICS

    def __init__(self, cols, dir_path="./csvs/"):
        self.dir_path = dir_path
        self.cols = cols
        if(not self.dir_path.endswith("/")):
            raise NameError('Directory path must end with /')

    def write_to_csv(self, data, filename="default"):
        '''
        Helper function to write data to csv and save the file

        Input: 
            data: 2D array of size (m x n), where m is the columns (properties) and n is the rows (data points)

            filename: Filename of the csv. Defaults to default.csv
        '''

        if(len(data[0]) != len(self.cols)):
            raise ValueError(
                'Size of data (columns) must be same as column names')

        if(data):
            with open(self.dir_path+filename+".csv", 'w', newline='') as file:
                writer = csv.writer(file)
                # write header
                writer.writerow(self.cols)
                # write data
                writer.writerows(data)
            print(f"> Sucessfully written to {self.dir_path + filename} ...")
