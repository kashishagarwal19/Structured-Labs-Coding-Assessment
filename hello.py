from preswald import connect, get_df, text, table, slider, plotly, selectbox, text_input
import plotly.express as px
import pandas as pd

#Connect and load
connect()
df = pd.read_csv('data/population_density.csv')

#Clean column names
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

#Drop the "State Total" row and NaN rank rows
df = df[(df["District"] != "State Total") & (df["Rank"].notna())]

#Convert area to numeric safely
df["Geograpical_Area_(Sq.Kms)"] = pd.to_numeric(df["Geograpical_Area_(Sq.Kms)"], errors="coerce")

#Calculate total population
df["Total_Population"] = df["Male"] + df["Female"]

#Title and description
text("# India District Census Dashboard (2011)")
text("Explore population trends, gender distribution, and area density across Indian districts using 2011 Census data.")

#Full dataset
table(df, title="Complete Census Dataset")

#Slider control
threshold = slider("Filter by Minimum Total Population", min_val=0, max_val=int(df["Total_Population"].max()), default=350000)
filtered_df = df[df["Total_Population"] > threshold]

#Explain filtering
text("This table shows only the districts with a total population above the selected threshold. Use the slider to adjust the cutoff.")

#Filtered table
table(filtered_df, title="Districts Above Population Threshold")

#Scatter plot
scatter_df = filtered_df.dropna(subset=["Geograpical_Area_(Sq.Kms)", "Total_Population"])
fig1 = px.scatter(
    scatter_df,
    x="Geograpical_Area_(Sq.Kms)",
    y="Total_Population",
    size="Population_Density",
    size_max=100,
    color="District",
    hover_data=["Male", "Female", "Population_Density"],
    title="Area vs Total Population (Bubble Size = Density)"
)
plotly(fig1)

#Gender distribution
top_gender = filtered_df.sort_values(by="Total_Population", ascending=False).head(15)
fig2 = px.bar(
    top_gender,
    x="District",
    y=["Male", "Female"],
    barmode="group",
    title="Gender Distribution (Top 15 Most Populated Districts)"
)
plotly(fig2)

#Top 10 populated districts
top10 = df.sort_values(by="Total_Population", ascending=False).head(10)
fig3 = px.bar(
    top10,
    x="District",
    y="Total_Population",
    color="District",
    title="Top 10 Most Populated Districts"
)
plotly(fig3)


