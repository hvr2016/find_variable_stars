###################################################
# Find Stars Variability                          #
# Matheus J. Castro                               #
# Version 1.2                                     #
# Last Modification: 09/16/2020 (month/day/year)  #
###################################################

import matplotlib.pyplot as plt
import numpy as np
import os


def find_files(dir_name):
    # Find all files inside the dir_name and create a list with these files
    # with the dir_name before of each file
    files = os.listdir(dir_name)  # search for files
    if dir_name[-1] != "/":  # verify the separator character
        separator = "/"
    else:
        separator = ""

    for i in range(len(files)):
        files[i] = dir_name + separator + files[i]  # concatenate the dir_name with file names

    return files


def open_data(fl_name):
    # Open a specific file with the format needed
    data = np.genfromtxt(fl_name, delimiter=",", dtype=None, encoding="ASCII")
    file = open(fl_name).readlines()[1:17]
    param = {}
    for i in file:
        line = i[1:-1].split(",")
        try:
            param[line[0]] = [line[1], line[2]]
        except IndexError:
            param[line[0]] = line[1]

    return param, data


def format_data(data):
    # Format data to separate data for each filter
    fdata = {}
    filter_list = [data[0][3]]
    filter_verify = data[0][3]
    for i in data:  # create a list with the filters found
        if filter_verify != i[3]:
            filter_verify = i[3]
            filter_list.append(i[3])

    for i in filter_list:  # append data for each filter
        fdata[i] = [[], [], []]
        for j in data:
            if i == j[3]:
                fdata[i][0].append(j[0])
                fdata[i][1].append(j[1])
                fdata[i][2].append(j[2])

    return fdata


def plot_data(data, show=False):
    # Plot data
    plt.figure(figsize=(21, 9))
    plt.title("Change of MAG on each filter")
    plt.xlabel("Time")
    plt.ylabel("MAG")

    for i in data.keys():  # plot data for each filter
        plt.plot(data[i][0], data[i][1], ".-", label=i)
        # plt.errorbar(data_plot[i][0], data_plot[i][1], yerr=data_plot[i][2], fmt=".", label=i)

    plt.legend()
    plt.grid()
    plt.savefig("Change of MAG on each filter")
    if show:
        plt.show()
    plt.close()


def save_results(iqr, eta, dir_name, fl_name):
    if not os.path.isdir("results_" + dir_name):
        os.mkdir("results_" + dir_name)
    fl_name = "results_" + fl_name

    iqr = np.array(list(iqr.items()))
    eta = np.array(list(eta.items()))

    save = "Method, Filter, Result\n"

    for i in range(len(iqr)):
        save += "IQR, {}, {}\n".format(iqr[i][0], iqr[i][1])
    for i in range(len(eta)):
        save += "ETA, {}, {}\n".format(eta[i][0], eta[i][1])

    np.savetxt(fl_name, [save], fmt="%s")


def iqr_method(data):
    # Find the IQR value for each filter of an file opened
    iqr = {}
    for i in data.keys():
        data_len = len(data[i][1])
        if data_len != 1:
            data_of_interest = np.sort(data[i][1])[data_len//4:-data_len//4]  # Exclude the 25% lower and highest values
        else:
            data_of_interest = data[i][1]

        data_len = len(data_of_interest)
        if data_len != 1:
            # Diference between the median of the upper and lower halves
            iqr[i] = np.median(data_of_interest[data_len//2:]) - np.median(data_of_interest[:data_len//2])
        else:
            iqr[i] = 0

    return iqr


def eta_method(data):
    # Find the IQR value for each filter of an file opened
    eta = {}
    for i in data.keys():
        data_len = len(data[i][1])-1

        mean_square = 0
        for j in range(data_len):  # find mean square successive difference
            mean_square += (data[i][1][j+1] - data[i][1][j]) ** 2 / data_len

        if data_len != 0:
            var = 0
            for j in range(data_len+1):  # find variance manually
                var += (data[i][1][j] - np.mean(data[i][1]))**2 / data_len

        var = np.std(data[i][1])**2  # find the variance

        if var != 0:
            eta[i] = mean_square/var
        else:
            eta[i] = 0

    return eta


def main(dir_name):
    # Main function
    fls_names = find_files(dir_name)

    for fl_name in fls_names:
        param, data = open_data(fl_name)
        data = format_data(data)

        iqr_results = iqr_method(data)
        eta_results = eta_method(data)

        save_results(iqr_results, eta_results, dir_name, fl_name)
        # plot_data(data)


if __name__ == '__main__':
    direc_name = "202006_Matheus"
    main(direc_name)
