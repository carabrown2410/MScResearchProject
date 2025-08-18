
import pandas as pd
import numpy as np
import os

# load the data
input_path = os.path.join('bethany-final-c', 'b-28082024-135351.csv')
df = pd.read_csv(input_path)

# only compute bouts up to capture frame + 5
df = df.loc[0:571]

# define cricket x and y coords
x = df['cricket_body_x']
y = df['cricket_body_y']

# calculate speed
dx = x.diff() # difference in x position between frames
dy = y.diff() # difference in y position between frames
speed = np.sqrt(dx**2 + dy**2) # calculate distance

# turn speed into dataframe
df["speed"] = speed

# smooth speed with rolling mean (window = 5 frames)
df["speed_smooth"] = df["speed"].rolling(window=3, center=True).mean()

# set speed threshold to detect movement
threshold = 5
df["moving"] = df["speed_smooth"] > threshold

# mark frames with speed above threshold as glitches
max_speed = 80
df["glitch"] = df["speed"] > max_speed
print(df[df['glitch'] == True])

# remove or exclude these frames from analysis
df["moving"] = df["moving"].astype(float)
df.loc[df["glitch"], ["speed", "speed_smooth", "moving"]] = np.nan

# detect changes in movement state
df["movement_change"] = df["moving"].ne(df["moving"].shift(fill_value=False))
change_indices = df.index[df["movement_change"]].tolist()

# determine start, end of movement bouts
movement_bouts = []
for i in range(0, len(change_indices) -1, 2):
    start = change_indices[i]
    end = change_indices[i + 1] - 1
    if df.loc[start, "moving"]:
        movement_bouts.append((start, end))

# handle cases where movement continues to end of the video
if len(change_indices) % 2 != 0 and df.loc[change_indices[-1], "moving"]:
    movement_bouts.append((change_indices[-1], df.index[-1]))

# backtrack start frames by 3 frames; add 90 to end
adjusted_bouts = [(max(0, s - 3), e + 90) for s, e in movement_bouts]

# merge bouts separated by gaps below 3 frames
def merge_bouts(adjusted_bouts, max_gap=3):
    if not adjusted_bouts:
        return []
    
    merged = []
    current_start, current_end = adjusted_bouts[0]

    for start, end in adjusted_bouts[1:]:
        if start - current_end <= max_gap:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end
    
    merged.append((current_start, current_end))
    
    return merged

merged_bouts = merge_bouts(adjusted_bouts, max_gap=2)

# filter bouts shorted than 5 frames 
min_duration = 5
final_bouts = [(s,e) for s, e in merged_bouts if (e - s + 1) >= min_duration]

# always include a final capture bout covering the last 10 frames
capture_end = df.index[-1]
capture_start = max(0, capture_end - 10) 

capture_bout = (capture_start, capture_end)

# append only if it doesn’t overlap with existing bouts
if all(not (s <= capture_start <= e or s <= capture_end <= e) for s, e in final_bouts):
    final_bouts.append(capture_bout)

final_bouts.sort()

# save movement bouts to output file
movement_df = pd.DataFrame(final_bouts, columns=["start_frame","end_frame"])
output_path = os.path.join('bethany-bouts', 'b-28082024-135351-bouts.csv')
movement_df.to_csv(output_path, index=False)
