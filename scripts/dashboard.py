#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import geopandas as gpd
import folium
import pydeck as pdk
import matplotlib.pyplot as plt


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

shapefile_path = "data/raw/DATOS GEOREFERENCIALES/2023/2023_1_00_ENT.shp"  # Replace with your shapefile path
gdf = gpd.read_file(shapefile_path)

# Ensure the GeoDataFrame has latitude and longitude columns for centroids
gdf['lon'] = gdf.geometry.centroid.x
gdf['lat'] = gdf.geometry.centroid.y
gdf['CVE_ENT']=gdf['CVE_ENT'].astype('int')

# Initialize session state to store the selected CVE_ENT
if "selected_cve_ent" not in st.session_state:
    st.session_state.selected_cve_ent = None

# Load data
@st.cache_data
def load_data(data_file):
    df=pd.read_csv(f"data/processed/ENIGH/{data_file}.csv")
    return df


population=load_data('population')
nivel_nombre_order = [
    'Ninguno',
    'Preescolar',
    'Primaria',
    'Secundaria', 
    'Preparatoria o bachillerato',
    'Profesional',
    'Normal',
    'Carrera técnica o comercial',
    'Maestría',
    'Doctorado'
]

# Convert 'nivel_nombre' column to a categorical type with the defined order
population['nivel_nombre'] = pd.Categorical(population['nivel_nombre'], categories=nivel_nombre_order, ordered=True)


income=load_data('income')
df=pd.merge(income,population, on=['folioviv','foliohog','numren','year','entidad'], how='inner')

background_color = "#1E1E1E"  # Dark gray
text_color = "#FFFFFF"  # White


####################### Sidebar
with st.sidebar:
    st.title('🏂 US Population Dashboard')
    
    year_list = list(df.year.unique())[::-1]
    entidades=list(population.nombre_entidad.unique())[::-1]
    entidades.append('Nacional')
    
    selected_entidad = st.selectbox('Selecciona una entidad', entidades)
    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = df[df.year == selected_year]
    df_selected_year_sorted=df_selected_year.groupby(['year','generacion'],as_index=False)['ing_tri'].mean().sort_values(by="ing_tri", ascending=False).round(2)
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots
    

def plot_literacy_proportion_over_time(population, selected_entidad,text_color,background_color):
    # Filter the data for the specific 'entidad'
    df = population[['folioviv', 'foliohog', 'numren', 'alfabetism', 'year', 'entidad', 'sexo', 'nombre_entidad']]
    is_entidad = df['nombre_entidad'] == selected_entidad
    if selected_entidad!='Nacional':
        df = df[is_entidad]
        
    
    df = df.groupby('year', as_index=False)['alfabetism'].value_counts(normalize=True)
    
    
    # Filter for both alfabetism levels: 1 and 2
    df_alfabetism_1 = df[df['alfabetism'] == 1]
    

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot for alfabetism == 1
    ax.plot(
        df_alfabetism_1['year'],
        df_alfabetism_1['proportion'],
        marker='o',
        label='Alfabetas',
        color='white'
    )

    
    fig.patch.set_facecolor(background_color)  # Figure background
    ax.set_facecolor(background_color)

    # Customize the plot
    ax.set_title(f"Proportion of Alfabetism Over Time in {selected_entidad}",color=text_color, fontsize=14)
    ax.set_xlabel("Year", fontsize=12,color=text_color)
    ax.set_ylabel("Proportion", fontsize=12,color=text_color)
    ax.set_xticks(df['year'].unique())
    ax.tick_params(colors=text_color)
    ax.legend(title="Alfabetism Level")
    ax.grid(True, linestyle='--', alpha=0.6)

    

    # Show the plot in the Streamlit app
    plt.tight_layout()
    st.pyplot(fig)


def plot_proportion_by_year(population,selected_entidad,text_color,background_color):
    # Select necessary columns
    df = population[['folioviv', 'foliohog', 'numren', 'nivelaprob', 'year', 'entidad', 'sexo', 'nombre_entidad']]
    is_entidad = df['nombre_entidad'] == selected_entidad
    if selected_entidad!='Nacional':
        df = df[is_entidad]

    # Grouping and calculating proportions
    df_counts = (
        df.groupby(['year'])['nivelaprob']
        .value_counts(normalize=True)
        .rename('percentage')
        .reset_index()
    )

    # Pivoting the data to get a better structure for plotting
    df_pivot = df_counts.pivot(index='year', columns='nivelaprob', values='percentage').fillna(0)

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))
    df_pivot.plot(kind='bar', stacked=True, ax=ax, colormap='viridis')

    
    fig.patch.set_facecolor(background_color)  # Figure background
    ax.set_facecolor(background_color)

    # Customizing the plot
    ax.set_title('Proporciones de Grado Aprobado por Año',color=text_color)
    ax.set_xlabel('Año',color=text_color)
    ax.set_ylabel('Porcentaje',color=text_color)
    ax.tick_params(colors=text_color)
    ax.legend(title='Gradoaprob', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Display the plot in the Streamlit app
    st.pyplot(fig)

def plot_proportion_by_generation(population, year,selected_entidad,text_color,background_color):
    # Grouping the data
    df=population
    is_entidad = df['nombre_entidad'] == selected_entidad
    if selected_entidad!='Nacional':
        df= df[is_entidad]

    data = df.groupby(['year', 'nivel_nombre'], as_index=False)['generacion'].value_counts(normalize=True)
    data = data[data['year'] == year]

    

    # Pivoting the data
    pivot_df = data.pivot(index='generacion', columns='nivel_nombre', values='proportion')

    # Plotting the data
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot_df.plot(kind='bar', ax=ax, colormap='viridis', width=0.8)

    
    fig.patch.set_facecolor(background_color)  # Figure background
    ax.set_facecolor(background_color)

    # Formatting the plot
    ax.set_title(f"Tazas de proporción de grado aprobado Nacional {year}",color=text_color)
    ax.set_ylabel("Taza ",color=text_color)
    ax.set_xlabel("Generacion",color=text_color)
    ax.tick_params(colors=text_color)
    ax.legend(title="Generation", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Display the plot in the Streamlit dashboard
    st.pyplot(fig)

def plot_income_by_grade_and_year(income, population,selected_entidad,text_color,background_color):
    # Merging the dataframes
    df = pd.merge(income, population, on=['folioviv', 'foliohog', 'numren', 'year', 'entidad'], how='inner')

    # Selecting relevant columns
    df = df[['folioviv', 'foliohog', 'sexo', 'numren', 'edad', 'generacion',
             'entidad','nombre_entidad', 'ing_tri', 'nivel_nombre', 'year']]

    is_entidad = df['nombre_entidad'] == selected_entidad
    if selected_entidad!='Nacional':
        df = df[is_entidad]
                
    # Calculating total income per group
    df['ing_tri_total'] = df.groupby(['folioviv', 'foliohog', 'numren', 'year'])['ing_tri'].transform('sum')

    # Grouping by year and level name, calculating average income
    data = df.groupby(['year', 'nivel_nombre'], as_index=False)['ing_tri_total'].mean()
    
    # Calculating monthly income
    data['ing_mens'] = data['ing_tri_total'] / 3

    # Pivoting the data for the plot
    pivot_df = data.pivot(index='year', columns='nivel_nombre', values='ing_mens')

    # Plotting the bar graph
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot_df.plot(kind='bar', ax=ax, colormap='viridis', width=0.8)

    
    fig.patch.set_facecolor(background_color)  # Figure background
    ax.set_facecolor(background_color)

    # Formatting the plot
    ax.set_title("Grade Income Over Years",color=text_color)
    ax.set_ylabel("Trimester Income (MXN)",color=text_color)
    ax.set_xlabel("Year",color=text_color)
    ax.tick_params(colors=text_color)
    ax.legend(title="Grade", bbox_to_anchor=(1.05, 1), loc='upper left')
    

    plt.tight_layout()

    # Display the plot in the Streamlit app
    st.pyplot(fig)




# Display map
def display_map():
    
    deck = pdk.Deck(
        layers=[
            pdk.Layer(
                "GeoJsonLayer",
                data=gdf.__geo_interface__,  # Convert GeoDataFrame to GeoJSON
                get_fill_color="[255, 180, 180]",
                get_line_color="[200, 0, 0]",
                pickable=True,  # Enables interaction
                auto_highlight=True,
            )
        ],
        initial_view_state=pdk.ViewState(
            latitude=gdf['lat'].mean(),
            longitude=gdf['lon'].mean(),
            zoom=4,
        ),
        tooltip={"html": "<b>Estado:</b> {NOMGEO}"},
    )

    # Render the map in Streamlit
    map_data = st.pydeck_chart(deck)
    return map_data


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
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=4)
    
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
    st.markdown('#### Selecciona Estado')
    map_data = display_map()
    col1, col2 = st.columns(2)

    # Nacional
    with col1:
    
        plot_proportion_by_generation(population, selected_year,'Nacional',text_color,background_color)
        plot_income_by_grade_and_year(income, population,'Nacional',text_color,background_color)
        plot_proportion_by_year(population,'Nacional',text_color,background_color)
        plot_literacy_proportion_over_time(population,'Nacional',text_color,background_color)

    # Estatal
    with col2:

        plot_proportion_by_generation(population, selected_year,selected_entidad,text_color,background_color)
        plot_income_by_grade_and_year(income, population,selected_entidad,text_color,background_color)
        plot_proportion_by_year(population,selected_entidad,text_color,background_color)
        plot_literacy_proportion_over_time(population,selected_entidad,text_color,background_color)
        

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