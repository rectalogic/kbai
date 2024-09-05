# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///


import matplotlib.pyplot as plt
import numpy as np


def create_custom_plot():
    # Create a new figure with specified size
    fig, ax = plt.subplots(figsize=(6.4, 4.8))  # 640x480 pixels at 100 dpi

    # Set the axis limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(1, -1)

    # Create tick locations
    ticks = np.arange(-0.9, 1, 0.1)

    # Set ticks and labels for both axes
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    # Format tick labels to show only two decimal places
    ax.xaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))

    # Add gridlines
    ax.grid(True, linestyle="--", alpha=0.7)

    # Move the x-axis to y=0
    ax.spines["bottom"].set_position("zero")

    # Move the y-axis to x=0
    ax.spines["left"].set_position("zero")

    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add some colored dots for reference
    points = [
        (0.3, 0.3, "r"),
        (-0.3, -0.3, "r"),
        (0.3, -0.3, "r"),
        (-0.3, 0.3, "r"),
        (0.8, 0.8, "g"),
        (-0.8, -0.8, "g"),
        (0.8, -0.8, "g"),
        (-0.8, 0.8, "g"),
        (0.4, 0.8, "b"),
        (-0.4, -0.8, "b"),
        (0.4, -0.8, "b"),
        (-0.4, 0.8, "b"),
        (0.8, 0.4, "c"),
        (-0.8, -0.4, "c"),
        (0.8, -0.4, "c"),
        (-0.8, 0.4, "c"),
        (0.6, 0.6, "y"),
        (-0.6, -0.6, "y"),
        (0.6, -0.6, "y"),
        (-0.6, 0.6, "y"),
        (0.9, 0.9, "k"),
        (-0.9, -0.9, "k"),
        (0.9, -0.9, "k"),
        (-0.9, 0.9, "k"),
    ]
    ax.scatter([p[0] for p in points], [p[1] for p in points], c=[p[2] for p in points])

    # Adjust layout and display the plot
    plt.tight_layout(pad=0)
    plt.show()


if __name__ == "__main__":
    create_custom_plot()
