import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def hist():
    # Read Price Label
    data = pd.read_csv("rightmove_london_labeled.csv")
    data_label = data["label"]
    data_count = data_label.value_counts()

    x = np.array(data_count.keys())
    y = np.array(data_count)

    print(x)
    print(y)
    plt.figure(figsize=(19,10))
    plt.barh(x, y, tick_label=x)
    plt.show()


data = pd.read_csv("rightmove_london_cleaned_final.csv")

fig = px.density_mapbox(data, lat='lat', lon='lng',z='price', radius=10,
                        mapbox_style="carto-positron",
                        color_continuous_scale='viridis',
                        center=dict(lat=0, lon=180), zoom=0,
                        )
fig.show()