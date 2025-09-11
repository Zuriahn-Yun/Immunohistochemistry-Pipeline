import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("cleaned.csv", header=None)
df.columns = ["File", "Image", "Color", "Color_Count", "Intensity"]

# Convert to numeric
df["Color_Count"] = pd.to_numeric(df["Color_Count"], errors="coerce")
df["Intensity"] = pd.to_numeric(df["Intensity"], errors="coerce")
df["Image"] = pd.to_numeric(df["Image"], errors="coerce")

# Compute percentages
df["Total"] = df.groupby(["File", "Image"])["Color_Count"].transform("sum")
df["Percentage"] = (df["Color_Count"] / df["Total"]) * 100

# Define custom line colors
custom_colors = {
    "Black": "black",
    "White": "gray",
    "Red": "red",
    "Green": "green",
    "Blue": "blue"
}

# One line graph per file
for file, subset in df.groupby("File"):
    fig = px.line(
        subset,
        x="Image",
        y="Percentage",
        color="Color",
        title=f"Color Percentages Across Images - {file}",
        markers=True,
        color_discrete_map=custom_colors  # Set Custom Colors
    )
    fig.update_layout(
        yaxis_title="Percentage (%)",
        xaxis_title="Image Number"
    )
    fig.show()
