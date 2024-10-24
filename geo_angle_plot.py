import matplotlib.pyplot as plt
import numpy as np

# Set up the figure and 3D axis
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot a sphere (Earth)
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 6371 * np.outer(np.cos(u), np.sin(v))  # Earth's radius ~6371 km
y = 6371 * np.outer(np.sin(u), np.sin(v))
z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))

# Plot Earth with light green and navy colors
ax.plot_surface(x, y, z, color='lightgreen', rstride=5, cstride=5, alpha=0.6, edgecolor='navy')

# Plot geographic angle (similar to the figure between City A and B)
x_geo = [0, 2500, 5000]
y_geo = [0, 2500, 5000]
z_geo = [0, 1500, 3000]

ax.plot(x_geo, y_geo, z_geo, color='darkred', lw=3, label='Geographic Angle')

# Adding example points for City A and City B
ax.scatter(x_geo[0], y_geo[0], z_geo[0], color='navy', s=100, label='Point A', marker='o')
ax.scatter(x_geo[-1], y_geo[-1], z_geo[-1], color='navy', s=100, label='Point B', marker='o')

# Labels and title
ax.text(x_geo[0], y_geo[0], z_geo[0], "Point A", color='black', fontsize=12)
ax.text(x_geo[-1], y_geo[-1], z_geo[-1], "Point B", color='black', fontsize=12)

# Customizing the view and removing grid
ax.set_xlim([-7000, 7000])
ax.set_ylim([-7000, 7000])
ax.set_zlim([-7000, 7000])

ax.set_xlabel('X axis (km)', fontsize=12)
ax.set_ylabel('Y axis (km)', fontsize=12)
ax.set_zlabel('Z axis (km)', fontsize=12)

ax.set_title("Geographic Angle Between Point A and B", fontsize=14)

# Removing the grid for a cleaner view
ax.grid(False)

# Dark gray for axis borders
ax.xaxis._axinfo["grid"].update({"color": "darkgray"})
ax.yaxis._axinfo["grid"].update({"color": "darkgray"})
ax.zaxis._axinfo["grid"].update({"color": "darkgray"})

# Saving the plot as a PNG file
plt.savefig('geoangle_modified_clean.png', dpi=300)  # Saves as high-resolution PNG

# Show the plot
plt.legend()
plt.show()
