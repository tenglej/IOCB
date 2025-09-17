import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

dataset = 0
# === Original data ===

min1_index = 3
min2_index = 25
saddle_index = 14
interpolationType = 'quadratic'  # 'quadratic' or 'linear'
data = [
    [220, 240, 1.46922268, 14.69496128],
    [220, 260, 1.45849363, 13.02985302],
    [220, 280, 1.45523045, 12.19890045],
    [220, 300, 1.45812052, 11.9401194],
    [220, 320, 1.46619153, 12.19971358],
    [230, 240, 1.70798744, 15.97789933],
    [230, 260, 1.70195465, 14.36082288],
    [230, 280, 1.70303676, 13.84498744],
    [230, 300, 1.70607827, 13.2455833],
    [230, 320, 1.71520976, 13.40178899],
    [240, 240, 1.83864838, 16.23117316],
    [240, 260, 1.83509917, 14.63053433],
    [240, 280, 1.83569667, 13.77102968],
    [240, 290, 1.83550614, 13.5641493],
    [240, 300, 1.83970957, 13.425137],
    [240, 320, 1.84791106, 13.47477825],
    [250, 240, 1.91281605, 16.00361375],
    [250, 260, 1.91069201, 14.41971419],
    [250, 280, 1.91100897, 13.50483253],
    [250, 300, 1.91439409, 13.0946231],
    [250, 320, 1.92010443, 13.04604422],
    [260, 240, 1.95532107, 15.56135292],
    [260, 260, 1.95371447, 13.99204918],
    [260, 280, 1.95414266, 13.05386281],
    [260, 300, 1.95603848, 12.55627091],
    [260, 320, 1.95971857, 12.4256788]
]
if dataset == 1:
    interpolationType = 'linear'  # 'quadratic' or 'linear'
    min1_index = 0
    min2_index = 1
    saddle_index = 5
    data = [
        [150, 170, 0.88872626, 0],
        [230, 100, 1.34629315, 6.83],
        [190, 160, 1.00168324, 22.42623401],
        [170, 150, 0.88872626, 10.82219126],
        [170, 160, 0.88294176, 10.0260798],
        [170, 170, 0.88051851, 9.841896835],
        [190, 150, 1.00645949, 23.45545125],
        [190, 160, 1.00450778, 22.63323845],
        [190, 170, 1.00168324, 22.42623401],
        [210, 150, 1.2764304, 30.14409182],
        [210, 160, 1.34054241, 29.49151819],
        [210, 170, 1.34629315, 29.32418299],
        [190, 190, 1.34629315, 23.19158066],
        [190, 130, 1.34629315, 10]

    ]

    data = [
        [150, 170, 0.88872626, 0],
        [230, 100, 1.34629315, 6.83],
        # [190, 160, 1.00168324, 22.42623401],
        [160, 170, 0.24678227, 3.275993264],
        [170, 170, 0.16874623, 7.565281707],
        [180, 170, 0.081328, 11.3364204],
        [190, 170, 0.26364357, 11.67970407],
        [200, 170, 0.43310639, 9.702595827],
        [210, 170, 0.46690892, 8.006662703],
        [220, 170, 0.41961577, 7.877330194],
        [190, 190, 1.34629315, 23.19158066],
        [190, 130, 1.34629315, 17]
    ]

data = np.array(data, dtype=np.float64)

# === User selects minima and saddle by index into the data list ===
min1 = data[min1_index]
min2 = data[min2_index]
saddle = data[saddle_index]

# === Generate fine grid for smoother interpolation ===
bond1_vals = np.unique(data[:, 0])
bond2_vals = np.unique(data[:, 1])
R1_fine = np.linspace(bond1_vals.min(), bond1_vals.max(), 400)
R2_fine = np.linspace(bond2_vals.min(), bond2_vals.max(), 400)
R1_grid, R2_grid = np.meshgrid(R1_fine, R2_fine)
E_grid = griddata(data[:, 0:2], data[:, 3],
                  (R1_grid, R2_grid), method='linear')

# === Generate smooth parabolic reaction coordinate through saddle ===


def interpolate(min1, saddle, min2, n_path=400, interpolation='quadratic'):
    t = np.linspace(0, 1, n_path)
    fR1_path = 0
    fR2_path = 0
    if interpolation == 'quadratic':
        # Quadratic Lagrange interpolation for 3 points (min1, saddle, min2)
        fR1_path = (1 - t)*(1 - 2*t)*min1[0] + 4*t * \
            (1 - t)*saddle[0] + t*(2*t - 1)*min2[0]
        fR2_path = (1 - t)*(1 - 2*t)*min1[1] + 4*t * \
            (1 - t)*saddle[1] + t*(2*t - 1)*min2[1]
    else:
        n_seg = n_path  # points per segment
        # Linear segment: min1 -> saddle
        t1 = np.linspace(0, 1, n_seg)
        R1_seg1 = (1 - t1) * min1[0] + t1 * saddle[0]
        R2_seg1 = (1 - t1) * min1[1] + t1 * saddle[1]

        # Linear segment: saddle -> min2
        t2 = np.linspace(0, 1, n_seg)
        R1_seg2 = (1 - t2) * saddle[0] + t2 * min2[0]
        R2_seg2 = (1 - t2) * saddle[1] + t2 * min2[1]

        # Concatenate segments
        fR1_path = np.concatenate([R1_seg1, R1_seg2])
        fR2_path = np.concatenate([R2_seg1, R2_seg2])
    return fR1_path, fR2_path


R1_path, R2_path = interpolate(
    min1, saddle, min2, n_path=400, interpolation=interpolationType)
E_path = griddata(data[:, 0:2], data[:, 3],
                  (R1_path, R2_path), method='linear')


# === 3D PES plot ===
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Draw surface first
surf = ax.plot_surface(R1_grid, R2_grid, E_grid,
                       cmap='viridis', edgecolor='none', alpha=0.6, zorder=0)

# Plot the curve AFTER the surface so it is on top
ax.plot(R1_path, R2_path, E_path, color='red', linewidth=3,
        zorder=20)

# Scatter points on top of everything, no depth shading
ax.scatter(min1[0], min1[1], min1[3], color='blue', s=80,
           depthshade=False, zorder=30)
ax.scatter(min2[0], min2[1], min2[3], color='green', s=80,
           depthshade=False, zorder=30)
ax.scatter(saddle[0], saddle[1], saddle[3], color='black', s=100,
           depthshade=False, zorder=30)

# Add labels directly above the points
ax.text(min1[0], min1[1], min1[3] + 0.4, "O3", color='blue')
ax.text(min2[0], min2[1], min2[3] + 0.4, "O2", color='green')
ax.text(saddle[0], saddle[1], saddle[3] + 0.4, "TS1", color='black')


ax.set_clip_on(False)

if dataset == 1:
    ax.set_xlabel('[H-O] (pm)')
    ax.set_ylabel('[O-O] (pm)')
else:
    ax.set_xlabel('[C-O] (pm)')
    ax.set_ylabel('[Cu-O] (pm)')


ax.set_zlabel('E/(kcal/mol)')
ax.set_title('PES')
plt.show()
