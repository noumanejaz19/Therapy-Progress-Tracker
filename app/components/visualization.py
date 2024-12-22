import matplotlib.pyplot as plt
import numpy as np

# Line chart visualization
def create_line_chart(data, title, x_label, y_label):
    fig, ax = plt.subplots()

    for label, values in data.items():
        # Plot the line
        ax.plot(range(len(values)), values, label=label)

        # Annotate the data points with a minimal offset
        for i, v in enumerate(values):
            offset = 8 if i == 0 or v < values[max(0, i - 1)] else -8  # Reduced offset
            ax.annotate(
                f"{v}",  # Value text
                (i, v),  # Position
                textcoords="offset points",
                xytext=(0, offset),  # Reduced offset above or below
                ha="center",
                fontsize=10,  # Adjust font size for clarity
                color="black"  # Set annotation text color
            )
    
    # Adjust title and labels
    ax.set_title(title, pad=30)  # Add extra padding to move the title down
    ax.set_xlabel(x_label, labelpad=10)
    ax.set_ylabel(y_label, labelpad=10)
    
    # Place the legend above the graph with additional spacing
    ax.legend(
        loc="lower center", 
        bbox_to_anchor=(0.5, 1.15),  # Move legend further above the title
        ncol=1, 
        frameon=False
    )

    # Ensure layout is adjusted
    fig.tight_layout()
    return fig

# Bar chart visualization
def create_bar_chart(data, title, x_label, y_label):
    fig, ax = plt.subplots()
    x = np.arange(len(data))
    heights = list(data.values())
    labels = list(data.keys())
    ax.bar(x, heights, tick_label=labels)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig

# Pie chart visualization
def create_pie_chart(data, title):
    fig, ax = plt.subplots()
    sizes = list(data.values())
    labels = list(data.keys())
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(title)
    return fig

# Scatter plot visualization
def create_scatter_plot(x_data, y_data, title, x_label, y_label):
    fig, ax = plt.subplots()
    ax.scatter(x_data, y_data)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig