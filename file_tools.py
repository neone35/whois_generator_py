import pandas as pd  # open source data analysis and manipulation tool
import os


def create_output_dir():
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


def write_to_txt(data_arr, filename='output.txt'):
    create_output_dir()
    abs_output_dir = os.getcwd() + '/output/'
    f = open(abs_output_dir + filename, 'w')
    for i in range(0, len(data_arr)):
        if isinstance(data_arr[0], list):  # check if 2D array given
            f.write(f"{data_arr[i][0]} {data_arr[i][1]} {data_arr[i][2]}\n")
        else:
            f.write(f"{data_arr[i]}\n")
    f.close()


def write_to_csv(header, data_arr, filename='output.csv'):
    create_output_dir()
    pd_data = pd.DataFrame(data_arr, columns=header)
    pd_data.sort_values(by=header[1])
    abs_output_dir = os.getcwd() + '/output/'
    pd_data.to_csv(abs_output_dir + filename, index=False)
