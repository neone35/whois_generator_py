import pandas as pd  # open source data analysis and manipulation tool
import os
import sys

abs_output_dir = os.getcwd() + '/output/'


def create_output_dir():
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


def write_to_txt(data_arr, filename='output.txt'):
    create_output_dir()
    f = open(abs_output_dir + filename, 'w')
    try:
        for i in range(0, len(data_arr)):
            if isinstance(data_arr[0], list):  # check if 2D array given
                f.write(f"{data_arr[i][0]} {data_arr[i][1]}"
                        f" {data_arr[i][2]} {data_arr[i][3]}\n")
            else:
                f.write(f"{data_arr[i]}\n")
    except Exception as e:
        print('Error while writing to txt file. Info below. Exiting.. \n')
        print(e)
        sys.exit(0)
    f.close()


def write_to_csv(header, data_arr, filename='output.csv'):
    create_output_dir()
    try:
        pd_data = pd.DataFrame(data_arr, columns=header)
        pd_data.sort_values(by=header[1])
        pd_data.to_csv(abs_output_dir + filename, index=False)
    except Exception as e:
        print('Error while writing to csv file. Info below. Exiting.. \n')
        print(e)
        sys.exit(0)

