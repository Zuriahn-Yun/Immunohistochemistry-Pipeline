import pandas as pd
df = pd.read_csv("all_image_data.csv", header=None)

# 
df[0] = df[0].str.removeprefix("LIF FILES\\")  # works in Python 3.9+


# Save back
df.to_csv("cleaned.csv", index=False, header=False)
print("Done")