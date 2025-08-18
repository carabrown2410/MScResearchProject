import numpy as np 
import pandas as pd 
import os

# import dlc csv files
mouse_df = pd.read_csv(os.path.join('anthony-final', 'a-21082024-142955.csv')) 
cricket_df = pd.read_csv(os.path.join('anthony-final-c', 'a-21082024-142955.csv'))

# load movement bouts (start frame, end frame)
bouts_df = pd.read_csv(os.path.join('anthony-bouts', 'a-21082024-142955-bouts.csv'))

# create variables to store results in later
results_list = []
mouse_speeds = []
cricket_speeds = []
latencies = []

# loop through each bout
for i, row in bouts_df.iterrows():
    start = row['start_frame']
    end = row['end_frame']

    try:
        # calculate mouse nose vector
        nx_start = mouse_df.loc[start, 'nose_x']  # retrieve x coords
        nx_end = mouse_df.loc[end, 'nose_x']
        ny_start = mouse_df.loc[start, 'nose_y'] # retrieve y coords
        ny_end = mouse_df.loc[end, 'nose_y'] 
        nose_vector = np.array([nx_end - nx_start, ny_end - ny_start]) # calculate vector

        # calculate cricket vector
        cx_start = cricket_df.loc[start,'cricket_body_x'] # retrieve x coords
        cx_end = cricket_df.loc[end, 'cricket_body_x']
        cy_start = cricket_df.loc[start, 'cricket_body_y'] # retrieve y coords
        cy_end = cricket_df.loc[end, 'cricket_body_y']
        cricket_vector = np.array([cx_end - cx_start, cy_end - cy_start]) # calculate vector

        # calculate mouse head vector
        hx_start = mouse_df.loc[start, 'head_midpoint_x']
        hx_end = mouse_df.loc[end, 'head_midpoint_x']
        hy_start = mouse_df.loc[start, 'head_midpoint_y']
        hy_end = mouse_df.loc[end, 'head_midpoint_y']
        head_vector = np.array([hx_end - hx_start, hy_end - hy_start]) 

        # calculate head to nose vector
        head2nose_vector = np.array([hx_start - nx_start, hy_start - ny_start])

        # calculate mouse vector
        mouse_vector = nose_vector + head2nose_vector - head_vector

        # calculate angle between vectors
        dot_product = np.dot(mouse_vector, cricket_vector) # calculate dot product
        magnitude_m = np.linalg.norm(mouse_vector) # calculate magnitudes
        magnitude_c = np.linalg.norm(cricket_vector)

        if magnitude_m == 0 or magnitude_c == 0: # check for zero vectors 
            angle_degrees = np.nan
        else:
            value = dot_product / (magnitude_m * magnitude_c)
            value = np.clip(value, -1.0, 1.0) # avoid floating point errors
            angle_radians = np.arccos(value) # calculate angle in radians
            angle_degrees = np.degrees(angle_radians) # convert to degrees
            print(f"Angle between m and c: {angle_degrees} degrees")

        # calculate speed
        fps = 90
        duration_frames = end - start # calculate duration 
        mouse_distance = np.linalg.norm(mouse_vector) # avg speeed (px/frame)
        cricket_distance = np.linalg.norm(cricket_vector)
        mouse_speed = (mouse_distance / duration_frames) * fps if duration_frames > 0 else np.nan
        cricket_speed = (cricket_distance / duration_frames) * fps if duration_frames > 0 else np.nan
        
        
        results_list.append(angle_degrees)
        mouse_speeds.append(mouse_speed)
        cricket_speeds.append(cricket_speed)

    except KeyError as e:
        print(f"skipping bout {i} frames {start}{end} due to missing frame: {e}")
        results_list.append(angle_degrees)
        mouse_speeds.append(np.nan)
        cricket_speeds.append(np.nan)  
    

# add a column for the mouse id
mouse_id = 'c'  
bouts_df['mouse_id'] = mouse_id
day = 'day4'
bouts_df['day'] = day

# add a column that numbers each movement bout
bouts_df['bout_number'] = np.arange(1, len(bouts_df) + 1)  # starts from 1

# save results to csv file
bouts_df['angle_degrees'] = results_list
bouts_df['mouse_speed'] = mouse_speeds
bouts_df['cricket_speed'] = cricket_speeds
output_path = os.path.join('anthony-calcs', 'a-21082024-142955-calcs.csv')
bouts_df.to_csv(output_path, index=False)


