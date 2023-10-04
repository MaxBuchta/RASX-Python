import os
import numpy as np
import struct
import zipfile
import io
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

input_directory = filedialog.askdirectory(title="Select Input Directory")
if not input_directory:
    print("No directory selected. Exiting.")
    exit()

output_directory = os.path.join(input_directory, "TXT")
os.makedirs(output_directory, exist_ok=True)

def convert_rasx_to_txt(rasx_path):
    file_name = os.path.splitext(os.path.basename(rasx_path))[0]

    with open(rasx_path, 'rb') as binary_file:
        binary_data = binary_file.read()
        data = io.BytesIO(binary_data)
        with zipfile.ZipFile(data, 'r') as zip_file:
            file_list = zip_file.namelist()

            if file_list:
                first_file_name = file_list[0]

                with zip_file.open(first_file_name) as first_file:
                    first_file_content = first_file.read().decode('utf-8')
                    lines = first_file_content.split('\n')
                    data_columns = []
                    for line in lines:
                        line = line.lstrip('\ufeff')
                        columns = line.split('\t')
                        numeric_columns = [float(column) for column in columns if column.strip()]
                        data_columns.append(numeric_columns)

                    data_columns = [[x[0], x[1]] if len(x) >= 3 else x for x in data_columns]
                    if data_columns and data_columns[-1] == []:
                        data_columns.pop()
                    
                    data_columns = np.array(data_columns)
                    data_columns[:, 0] = np.round(data_columns[:, 0], 2)
                    data_columns[:, 1] = np.round(data_columns[:, 1], 4)


    output_txt_path = os.path.join(output_directory, f'{file_name}.txt')


    header_line1 = file_name
    header_line2 = "Angle ° Intensity [a.u.]"

    # Save the data as a text file with the custom header and specific formatting
    formatted_data = "\n".join(["{:.2f}\t{:.4f}".format(row[0], row[1]) for row in data_columns])
    with open(output_txt_path, 'w') as txt_file:
        txt_file.write(header_line1 + '\n' + header_line2 + '\n' + formatted_data)

for root, _, files in os.walk(input_directory):
    for file in files:
        if file.endswith(".rasx"):
            rasx_path = os.path.join(root, file)
            convert_rasx_to_txt(rasx_path)

print("Conversion completed.")

