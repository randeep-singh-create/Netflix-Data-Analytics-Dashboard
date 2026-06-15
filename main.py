import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Netflix Dashboard",layout="wide")

st.header("Netflix Data Analysis Dashboard")


@st.cache_data
def load_data():
    df=pd.read_csv("netflix_titles.csv")
    df["date_added"]=pd.to_datetime(df["date_added"],errors="coerce")
    df["year_added"]=df["date_added"].dt.year
    return df

df=load_data()

# SIDEBAR BNAVAGE
st.sidebar.header("Dashboard Filters")

type_filter=st.sidebar.multiselect("Select Content Type",
                                   options=df["type"].dropna().unique(),
                                   default=df["type"].dropna().unique())

country_filter=st.sidebar.multiselect("Select Country",
                                      options=df["country"].dropna().unique())

rating_filter=st.sidebar.multiselect("Select Rating",
                                     options=df["rating"].dropna().unique())

year_filter=st.sidebar.slider("Select Release Year",
                              int(df["release_year"].min()),
                              int(df["release_year"].max()),
                              (2000,2020))

fil_df=df[df["type"].isin(type_filter)]
if country_filter:
    fil_df=fil_df[fil_df["country"].isin(country_filter)]
if rating_filter:
    fil_df=fil_df[fil_df["rating"].isin(rating_filter)]
if year_filter:
    fil_df=fil_df[(fil_df["release_year"]>=year_filter[0]) & (fil_df["release_year"]<=year_filter[1])]

# KPI (key performance index) [ehi show kravaunde h generally]

st.subheader("Key Metrics")
col1,col2,col3,col4 = st.columns(4)
tottil=len(fil_df) # [dataframe di jehni lenght hovegi ohna total hovega]
totmov=len(fil_df[fil_df["type"]=="Movie"])
totshw=len(fil_df[fil_df["type"]=="TV Show"])
totcnt=fil_df["country"].nunique()  # itho tak calculation ho gyi hun dikhauna h
col1.metric("Total Titles",tottil)
col2.metric("Movies",totmov)
col3.metric("TV Shows",totshw)
col4.metric("Countries",totcnt)
st.divider()


col1,col2=st.columns(2)
with col1:
    st.subheader("Movies vs TV Shows")
    type_count=fil_df["type"].value_counts()
    #st.write(type_count)
    fig=px.pie(values=type_count.values,
               names=type_count.index,
               color_discrete_sequence=px.colors.sequential.Plasma)
    fig=fig.update_layout(showlegend=True)
    st.plotly_chart(fig,width="stretch")

with col2:
    st.subheader("Content Added Over Years")
    year_count=fil_df["year_added"].value_counts().sort_index()
    #st.write(year_count)
    fig=px.line(x=year_count.index,y=year_count.values,markers=True)
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Content Added")
    st.plotly_chart(fig,width="stretch")
st.divider()



col1,col2=st.columns(2)
with col1:
    st.header("Top Countries Producing Content")
    cnt_count=fil_df["country"].value_counts().head(10)
    #st.write(cnt_count)
    fig = px.bar(x=cnt_count.index, y=cnt_count.values,
                 color=cnt_count.index,
                 color_continuous_scale="Reds")
    fig.update_layout(xaxis_title="Country",
                      yaxis_title="No. of Titles")
    st.plotly_chart(fig, width="stretch")

    # fig=px.bar(x=cnt_count.values,y=cnt_count.index,
    #            color=cnt_count.index,
    #            color_continuous_scale="Reds")
    # fig.update_layout(xaxis_title="No. of Titles",
    #                   yaxis_title="Country")
    # st.plotly_chart(fig,width="stretch")

with col2:
    st.subheader("Rating Distribution")
    rating_counts = fil_df['rating'].value_counts()
    fig = px.bar(
        x=rating_counts.index,
        y=rating_counts.values,
        color=rating_counts.values,
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        xaxis_title="Rating",
        yaxis_title="Count"
    )

    st.plotly_chart(fig, width="stretch")

st.divider()

genres=fil_df["listed_in"].str.split(",").explode()
#st.write(genres)
st.subheader(" Top Genres")
genre_counts=genres.value_counts().head(10)
fig = px.bar(
    x=genre_counts.index,
    y=genre_counts.values,
    color=genre_counts.values,
    color_continuous_scale="Reds"
)

fig.update_layout(
    xaxis_title="Genre",
    yaxis_title="Number of Titles"
)

st.plotly_chart(fig, width="stretch")
st.divider()


st.subheader("Global Distribution of Netflix Content")

country_counts = fil_df['country'].value_counts().reset_index()
country_counts.columns = ['country','count']

fig = px.choropleth(
    country_counts,
    locations="country",
    locationmode="country names",
    color="count",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig,width="stretch")

st.divider()

search=st.text_input("Enter Title To Search")
if search:
    scrres=fil_df[fil_df["title"].str.contains(search,case=False)]
    st.write(scrres.head(50))
    st.markdown("---")
    st.markdown(
        "Netflix Data Dashboard"
    )
#st.write(fil_df)    #[isde nal pta lg janda h ke data aa reha h]
