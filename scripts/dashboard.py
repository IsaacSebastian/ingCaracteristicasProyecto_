#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd
import folium

#######################
# Page configuration
st.set_page_config(
    page_title="Salud Mental",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################

# Load data
@st.cache_data
def load_data(data_file):
    df=pd.read_csv(f"data/processed/ENIGH/{data_file}.csv")
    return df

population=load_data('population')
income=load_data('income')
df=pd.merge(income,population, on=['folioviv','foliohog','numren','year','entidad'], how='inner')


####################### Sidebar
with st.sidebar:
    st.title('🏂 US Population Dashboard')
    
    year_list = list(df.year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = df[df.year == selected_year]
    df_selected_year_sorted=df_selected_year.groupby(['year','generacion'],as_index=False)['ing_tri'].mean().sort_values(by="ing_tri", ascending=False).round(2)
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots


def make_barplot(dataframe,entidad):
    

    df=dataframe[['folioviv','foliohog','sexo','numren','edad','generacion',
                    'entidad','ing_tri','alfabetism','year']]
    df[df['entidad']==entidad]
    

    data=df.groupby(['year','generacion'],as_index=False)['ing_tri'].mean()
    pivot_df = data.pivot(index='year', columns='generacion', values='ing_tri')

    # Plot
    pivot_df.plot(kind='bar', figsize=(12, 6), colormap='coolwarm', width=0.8)

    # Formatting the plot
    plt.title("Generational Income Over Years")
    plt.ylabel("Trimester Income (MXN)")
    plt.xlabel("Year")
    plt.legend(title="Generation", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

# Heatmap
def make_heatmap(dataframe, columns):
    df = dataframe[columns]
    
    # Group data
    df_t = df.groupby('entidad')['gradoaprob'].value_counts(normalize=True).reset_index(name='proportion')

    # Load shapefile
    carpeta_descarga = 'data/raw/DATOS GEOREFERENCIALES/2023'
    mapa_a = f'{carpeta_descarga}/2023_1_00_ENT.shp'
    map_a = gpd.read_file(mapa_a)
    map_a['CVE_ENT'] = map_a['CVE_ENT'].astype('int')

    # Merge data with shapefile
    graph_df = pd.merge(df_t, map_a, left_on='entidad', right_on='CVE_ENT', how='inner')

    # Filter data for `gradoaprob == 3`
    data = graph_df[graph_df['gradoaprob'] == 3]

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(data, geometry='geometry')
    
    # Transform to EPSG:4326 for Folium compatibility
    gdf = gdf.to_crs(epsg=4326)

    # Create Folium map
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=6)
    
    # Add choropleth layer
    folium.Choropleth(
        geo_data=gdf,
        data=gdf,
        columns=["CVE_ENT", "proportion"],
        key_on="feature.properties.CVE_ENT",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Proportion"
    ).add_to(m)

    # Add tooltips
    for _, row in gdf.iterrows():
        folium.Popup(f"Entidad: {row['entidad']}, Proportion: {row['proportion']:.2f}").add_to(
            folium.GeoJson(row['geometry'])
        )

    return m

# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year.population)),
                               scope="usa",
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text 
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'




#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Gains/Losses')

    salud=10000
    estado_s='CDMX'
    diferencia_s=600

    st.metric(label=estado_s, value=salud, delta=diferencia_s)

    alfabetismo=20000
    estado='Aguascalientes'
    diferencia=-2000
    st.metric(label=estado, value=alfabetismo, delta=diferencia)

    
    st.markdown('#### States Migration')

 

with col[1]:
    st.markdown('#### Total Population')
    population_columns= ['folioviv', 'foliohog', 'numren', 'entidad','sexo', 'edad','generacion','alfabetism', 'asis_esc', 'nivel','grado', 'tipoesc','nivelaprob', 'gradoaprob']
    selected_entity=1
    #make_barplot(df_selected_year,selected_entity)
    
    heatmap = make_heatmap(df_selected_year,population_columns)
    st.components.v1.html(heatmap._repr_html_(), height=600)
    

with col[2]:
    st.markdown('#### Top States')

    st.dataframe(df_selected_year_sorted,
                 column_order=("generacion", "ing_tri"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "generacion": st.column_config.TextColumn(
                        "Generacion",
                    ),
                    "ing_tri": st.column_config.ProgressColumn(
                        "Proporcion",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted.ing_tri),
                     )}
                 )
    
    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
            - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
            - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
            ''')