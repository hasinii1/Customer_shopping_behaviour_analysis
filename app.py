import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Customer Shopping Intelligence Dashboard",
    page_icon="🛒",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main{
    background-color:#f5f7fb;
}

[data-testid="metric-container"]{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

h1{
    color:#1f2937;
}
.stButton button{
border-radius:10px;
}
</style>
""",unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():

    path=os.path.join(
        os.path.dirname(__file__),
        "customer_shopping_behavior.csv"
    )

    df=pd.read_csv(path)

    df.columns=df.columns.str.strip()


    df.rename(columns={

    "Gender":"gender",
    "Age":"age",
    "Category":"category",
    "Season":"season",
    "Review Rating":"rating",
    "Shipping Type":"shipping",
    "Purchase Amount (USD)":"amount"

    },inplace=True)
    return df
df=load_data()

# =========================
# HEADER
# =========================

st.markdown(
"""
# 🛒 Customer Shopping Analysis Dashboard
##### Customer Insights, Revenue Intelligence & Sales Trend
"""
)

# =========================
# SIDEBAR
# =========================
st.sidebar.header("🎯 Dashboard Filters")
gender=st.sidebar.multiselect(

    "Gender",
    df.gender.unique(),
    df.gender.unique()
)
category=st.sidebar.multiselect(
    "Category",
    df.category.unique(),
    df.category.unique()
)
season=st.sidebar.multiselect(
    "Season",
    df.season.unique(),
    df.season.unique()
)
data=df[
(df.gender.isin(gender)) &
(df.category.isin(category)) &
(df.season.isin(season))
]

# =========================
# KPI SECTION
# =========================
customers=len(data)
revenue=data.amount.sum()
avg=data.amount.mean()
rating=data.rating.mean()
a,b,c,d=st.columns(4)

a.metric(
"👥 Customers",
f"{customers:,}"
)

b.metric(
"💰 Revenue",
f"${revenue:,.0f}"
)

c.metric(
"🛍 Avg Purchase",
f"${avg:.2f}"
)

d.metric(
"⭐ Rating",
f"{rating:.2f}"
)
st.divider()

# =========================
# ROW 1 CHARTS
# =========================
# =========================
# CATEGORY ANALYSIS
# =========================
st.subheader("📦 Category Performance Overview")
left,right=st.columns(2)
with left:

    cat=data.groupby(
    "category"
    ).amount.sum().reset_index()


    fig=px.bar(
        cat,
        x="category",
        y="amount",
        title="💰 Revenue By Category",
        text_auto=True,
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



with right:


    fig=px.pie(
        cat,
        names="category",
        values="amount",
        hole=.45,
        title="📊 Category Contribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# =========================
# CUSTOMER ANALYSIS
# =========================
st.subheader("👥 Customer Analysis")
c1,c2=st.columns(2)
with c1:
    
    fig=px.histogram(
        data,
        x="age",
        nbins=20,
        title="Age Distribution",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)
with c2:

    fig=px.box(
        data,
        x="gender",
        y="amount",
        title="Purchase Distribution By Gender",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================
# SHIPPING
# =========================
st.subheader("🚚 Shipping Performance")
ship=data.groupby(
"shipping"
).amount.sum().reset_index()

fig=px.funnel(
ship,
x="amount",
y="shipping",
title="Revenue Through Shipping Methods"
)

st.plotly_chart(
fig,
use_container_width=True
)

# =========================
# RATING ANALYSIS
# =========================
st.subheader("⭐ Customer Rating Impact")
rate=data.groupby(
"rating"
).amount.mean().reset_index()
fig=px.line(
rate,
x="rating",
y="amount",
markers=True,
title="Rating vs Average Purchase",
template="plotly_white"
)

st.plotly_chart(fig,
use_container_width=True
)

# =========================
# TOP PERFORMANCE TABLE
# =========================
st.subheader("🏆 Top Category")
rank=data.groupby(
"category"
).agg(

Customers=("category","count"),
Revenue=("amount","sum"),
Average=("amount","mean")

).reset_index()

rank=rank.sort_values(
"Revenue",
ascending=False
)

st.dataframe(
rank,
use_container_width=True
)

# =========================
# DOWNLOAD
# =========================
st.download_button(
"📥 Download Filtered Dataset",
data.to_csv(index=False),
"customer_analysis.csv",
"text/csv"
)