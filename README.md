# Quantitative Analysis of Prey Capture Behaviour in Rodents

This repository contains a two-part analysis pipeline developed for my MSc thesis:  
**"Unveiling sensorimotor strategies in prey capture: behavioural testing of the kinetic anti-alignment model."**

The project investigates **sensorimotor coordination during prey capture** in rodents, with a focus on quantifying movement dynamics between a mouse and a cricket using pose estimation data. The analysis is grounded in the **kinetic anti-alignment model**, which predicts specific angular relationships and pursuit strategies in naturalistic hunting behaviour.

Using high-frame-rate videos and DeepLabCut-tracked positions, the pipeline performs:

1. **Movement Bout Detection**  
   Identifies discrete bouts of cricket movement based on smoothed velocity thresholds, while accounting for tracking noise and ensuring inclusion of key behavioural events like capture.

2. **Kinematic Feature Extraction**  
   Computes bout-level metrics including the angle between mouse and cricket movement vectors, average speeds, and bout durations — enabling detailed comparison with theoretical models of pursuit.

The code could be easily adaptable for similar behavioural tracking datasets (specifically with use of DeepLabCut datasets).

## Movement Bout Detection

The script performs the following steps:

1. **Load positional data** (`cricket_body_x`, `cricket_body_y`)
2. **Calculate speed** from positional changes
3. **Smooth speed** using a rolling window
4. **Threshold speed** to classify movement
5. **Identify glitches** (frames with unrealistically high speed)
6. **Detect movement bouts**, backtrack start frames and extend ends
7. **Merge short gaps** between bouts
8. **Filter out short bouts**
9. **Always include the final capture event**
10. **Export** movement bouts as a `.csv`

Each row in the output `.csv` corresponds to a detected bout.

## Bout Kinematics Analysis: Mouse-Cricket Interactions

This script calculates **kinematic and geometric features** during identified movement bouts between a mouse and a cricket. It extracts bout-level measures such as:

- Mouse-cricket **alignment angle**
- Mouse and cricket **average speed**
- Duration-normalised movement metrics

These metrics are intended to support analysis of **sensorimotor control** and test predictions from the **kinetic anti-alignment model**.

## Outputs

For each detected bout, the script calculates:

- `angle_degrees`: angle between the mouse movement vector and cricket movement vector  
- `mouse_speed`: average mouse speed during bout (px/s)  
- `cricket_speed`: average cricket speed during bout (px/s)  
- `mouse_id`, `day`, `bout_number`: metadata for multi-session analysis  


