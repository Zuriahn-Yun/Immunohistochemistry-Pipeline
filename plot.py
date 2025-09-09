import pandas as pd
import plotly.express as px


# THIS IS WRONG THIS DOESNT WORK 
df = pd.read_csv("all_image_data.csv")

df["Total_Pixels"] = df.groupby(["File", "Image"])["Color_Count"].transform("sum")
df["Percentage"] = df["Color_Count"] / df["Total_Pixels"] * 100

fig = px.line(
    df,
    x="Image",
    y="Percentage",
    color="Color",
    markers=True,
    title="Pixel Composition per Image",
    hover_data=["File", "Color_Count", "Intensity"]
)
fig.show()

# Option 2: Stacked area chart (each image = 100%)
fig2 = px.area(
    df,
    x="Image",
    y="Percentage",
    color="Color",
    title="Pixel Composition (Stacked) per Image",
    groupnorm="percent"  # ensures it stacks to 100%
)

fig2.show()
