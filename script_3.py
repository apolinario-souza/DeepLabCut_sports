#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 13:53:06 2024

@author: tercio
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import matplotlib.animation as ani
import math
import cv2


file = 'positions.cvs' # I replaced commas with dots before sending it here and removed column titles

# Read the CSV file starting from the third line
df = pd.read_csv(file, sep='\t', skiprows=2)
df = np.array(df)

total_video_duration = 107 # seconds
frequency = len(df[:, 0]) / total_video_duration
time = df[:, 0] / frequency

# Initialize elements with zeros
element1, element2, element3, element4, element5, element6, element7, element8, element9 = (
    np.zeros((3, len(df[:, 0]))) for _ in range(9)
)

# Assign data to elements
element1[0, :], element1[1, :], element1[2, :] = df[:, 1], df[:, 2], df[:, 3]
element2[0, :], element2[1, :], element2[2, :] = df[:, 4], df[:, 5], df[:, 6]
element3[0, :], element3[1, :], element3[2, :] = df[:, 7], df[:, 8], df[:, 9]
element4[0, :], element4[1, :], element4[2, :] = df[:, 10], df[:, 11], df[:, 12]
element5[0, :], element5[1, :], element5[2, :] = df[:, 13], df[:, 14], df[:, 15]
element6[0, :], element6[1, :], element6[2, :] = df[:, 16], df[:, 17], df[:, 18]
element7[0, :], element7[1, :], element7[2, :] = df[:, 19], df[:, 20], df[:, 21]
element8[0, :], element8[1, :], element8[2, :] = df[:, 22], df[:, 23], df[:, 24]
element9[0, :], element9[1, :], element9[2, :] = df[:, 25], df[:, 26], df[:, 27]

elements = [element1, element2, element3, element4, element5, element6, element7, element8, element9]
elements_transformed = [element1 * 0, element2 * 0, element3 * 0, element4 * 0, element5 * 0, element6 * 0, element7 * 0, element8 * 0, element9 * 0]

for i in range(element1.shape[1]):
    # All points are in format [cols, rows]
    pt_A = [element8[0, i], element8[1, i]] # Bottom left corner
    pt_B = [element9[0, i], element9[1, i]] # Bottom right corner
    pt_C = [element7[0, i], element7[1, i]] # Top right corner
    pt_D = [element6[0, i], element6[1, i]] # Top left corner

    # Calculate average widths and heights
    width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    meanWidth = (width_AD + width_BC) / 2

    height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    meanHeight = (height_AB + height_CD) / 2

    # Real distance between cones in meters
    real_distance = 1  # arbitrary value

    # Pixels per meter ratio
    pixels_per_meter_horizontal = meanWidth / real_distance
    pixels_per_meter_vertical = meanHeight / real_distance

    # Average pixels per meter
    pixels_per_meter = (pixels_per_meter_horizontal + pixels_per_meter_vertical) / 2

    # Coordinates of cones in the original image (in pixels)
    pts_orig = np.float32([pt_A, pt_B, pt_C, pt_D])

    # Desired coordinates in the new image (in pixels, based on pixels per meter ratio)
    pts_dest = np.float32([
        [0, 0], 
        [real_distance * pixels_per_meter, 0], 
        [real_distance * pixels_per_meter, real_distance * pixels_per_meter], 
        [0, real_distance * pixels_per_meter]
    ])

    # Calculate the homography matrix
    matrix = cv2.getPerspectiveTransform(pts_orig, pts_dest)

    # Function to transform points using the homography matrix
    def transform_point(matrix, point):
        point = np.array([point[0], point[1], 1], dtype='float32')
        transformed_point = np.dot(matrix, point)
        return transformed_point[0] / transformed_point[2], transformed_point[1] / transformed_point[2]

    for j in range(len(elements)):
        elements_transformed[j][:2, i] = transform_point(matrix, elements[j][:2, i])
        elements_transformed[j][2, i] = elements[j][2, i]

# Function to replace values with NaN in columns 1 and 2 based on values in column 3
def replace_with_nan(element):
    mask = element[2, :] < 0.80
    element[0, mask] = np.nan
    element[1, mask] = np.nan

replace_with_nan(elements_transformed[0])
replace_with_nan(elements_transformed[1])
replace_with_nan(elements_transformed[2])
replace_with_nan(elements_transformed[3])
replace_with_nan(elements_transformed[4])
replace_with_nan(elements_transformed[5])
replace_with_nan(elements_transformed[6])
replace_with_nan(elements_transformed[7])
replace_with_nan(elements_transformed[8])

# Known distance in meters
distance_meters = 6

# Calculate the distance in pixels between 'topLeft' and 'topRight'
distance_px = np.linalg.norm(np.array([elements_transformed[6][0, 0], elements_transformed[6][1, 0]]) - np.array([elements_transformed[5][0, 0], elements_transformed[5][1, 0]]))

# Calculate the scale (meters per pixel)
scale = distance_meters / distance_px

# List of styles for the points
styles = ['go', 'yo', 'ko', 'bo', 'ro', 'm+', 'm+', 'c+', 'c+']





data_filtered = []
upper_limit = 8
lower_limit = -2

# Filter data
for ii in range(len(elements)):
    # Create data array with only x and y
    data_array = np.array((elements_transformed[ii][0, :] * scale, elements_transformed[ii][1, :] * scale))
    
    # Apply filter: replace values greater than upper_limit with NaN
    data_array[data_array > upper_limit] = np.nan
    data_array[data_array < lower_limit] = np.nan
    
    # Add filtered array to `data_filtered` list
    data_filtered.append(data_array)    


# Define the names of the elements
element_names = ['green', 'yellow', 'black', 'blue', 'ball', 'topLeft', 'topRight', 'bottomLeft', 'bottomRight']

# Initialize a dictionary to store the combined data
data_dict = {'time': time}

# Add data for each element to the dictionary
for i, element_name in enumerate(element_names):
    data_dict[f'{element_name}_x'] = data_filtered[i][0]
    data_dict[f'{element_name}_y'] = data_filtered[i][1]

# Create a DataFrame from the dictionary
final_df = pd.DataFrame(data_dict)

# Save the final DataFrame to an Excel file
final_df.to_excel('data_filtered.xlsx', index=False)

print("Excel file saved successfully!")

#######################   Figures      #######################


time_index = 125 # 30 = 1 second
# Figure and subplot settings
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
legend = ['green', 'yellow', 'black', 'blue', 'ball', 'topLeft', 'topRight', 'bottomLeft', 'bottomRight']

# Plot data in subplots
for ii in range(len(elements)):
    # Without transformation (subplot 1)
    ax1.plot(elements[ii][0, time_index], elements[ii][1, time_index], styles[ii], label=legend[ii],markersize=12)

    # With transformation (subplot 2)
    ax2.plot(elements_transformed[ii][0, time_index] * scale, elements_transformed[ii][1, time_index] * scale, styles[ii], label=legend[ii],markersize=12)

# Subplot 1 settings (without transformation)
ax1.set_title('Without Transformation')
ax1.grid(True)
ax1.set_xlabel('x (px)')
ax1.set_ylabel('y (px)')
# Place legend outside the plot
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Subplot 2 settings (with transformation)
ax2.set_title('With Transformation')
ax2.set_xlabel('x (m)')
ax2.set_ylabel('y (m)')
ax2.grid(True)
# ax2.legend()

# Main figure title
fig.suptitle(f'time: {time[time_index]:.2f}')

plt.tight_layout()
plt.show()



# List of colors for the points
colors = ['g', 'y', 'k', 'b', 'r', 'm', '#ffad6f', '#ccadc3', 'c']

fig, ax = plt.subplots()

for ii in range(len(elements)):
    # Plot x and y data
    ax.plot(time, data_filtered[ii][0, :], color=colors[ii], linestyle='-', label=legend[ii] + '_x')
    ax.plot(time, data_filtered[ii][1, :], color=colors[ii], linestyle='--', label=legend[ii] + '_y')

ax.set_xlabel('time (sec)')
ax.set_ylabel('position (m)')  
# Place legend outside the plot
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Adjust layout
plt.tight_layout()

# Show plot
plt.show()


# Settings for figure and subplots
fig, ax = plt.subplots()
# Plot data on subplots
for ii in range(len(elements)):
    ax.plot(data_filtered[ii][0, :], data_filtered[ii][1, :], styles[ii], markersize=3, label=legend[ii])
    
ax.grid(False)
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')  
# Place legend outside the plot
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Adjust layout
plt.tight_layout()

# Show plot
plt.show()

