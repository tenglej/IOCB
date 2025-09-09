import matplotlib.pyplot as plt
import numpy as np

# Example states and energies
states = ["1P", "TS1", "O2", "TS2", "O3"]

energies_methods = {
    "tppsh with def2-tzvpd-all": [0, 16.48, 11.60, 10.56, 0],
}

x = np.arange(len(states))  # evenly spaced positions

plt.figure(figsize=(8, 5))
colors = ["orange", "blue", "green"]

for i, (method, energies) in enumerate(energies_methods.items()):
    energies = np.array(energies) - energies[0]  # normalize
    color = colors[i]

    # Flat horizontal lines (plateaus)
    for xi, yi in zip(x, energies):
        plt.hlines(y=yi, xmin=xi - 0.3, xmax=xi + 0.3, color=color, lw=2)

    # Dashed connectors between plateaus
    for (xi, yi), (xj, yj) in zip(zip(x[:-1], energies[:-1]), zip(x[1:], energies[1:])):
        plt.plot([xi + 0.3, xj - 0.3], [yi, yj],
                 color=color, lw=1.5, linestyle="--")

    # Labels above each plateau
    for xi, yi in zip(x, energies):
        plt.text(xi, yi + 1, f"{yi:.1f}", ha='center', color=color)

# Axis styling
plt.xticks(x, states)
plt.xlabel("Reaction Coordinate")
plt.ylabel("Relative Energy /(kcal/mol)")
plt.title("Reaction Energy Profiles (normalized to Reactant)")

# Remove top, right, and left spines
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)

# Add headspace above highest point
ymax = max(max(energies) for energies in energies_methods.values())
plt.ylim(top=ymax + 5)

plt.show()
