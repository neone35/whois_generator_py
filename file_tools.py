import pandas as pd  # open source data analysis and manipulation tool


def write_to_txt(data_arr, filename='output.txt'):
    f = open(filename, "w")
    # check if 2D array given
    for i in range(0, len(data_arr)):
        if isinstance(data_arr[0], list):  # check if 2D array given
            f.write(f"{data_arr[i][0]} {data_arr[i][1]} {data_arr[i][2]}\n")
        else:
            f.write(f"{data_arr[i]}\n")
    f.close()


def write_to_csv(header, data_arr, filename='output.csv'):
    pd_data = pd.DataFrame(data_arr, columns=header)
    pd_data.to_csv(filename, index=False)
