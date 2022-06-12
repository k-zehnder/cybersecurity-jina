from docarray import Document, DocumentArray
import pandas as pd
import plotly.express as px
import streamlit as st

from helpers import get_preds


st.set_page_config(page_title="Cybersecurity Dashboard", page_icon=":spider:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="./data/supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

def get_data(index_path):
    da = DocumentArray.load(index_path)
    da_df = da.to_dataframe()
    return da_df

# old_df = get_data_from_excel()
df = get_data("index")
  
df["id"] = df["id"].apply(lambda x: x[:8])
df["datetime"] = df["tags"].apply(lambda x: x.get("dt"))
df["known_label"] = df["tags"].apply(lambda x: x.get("known_label"))
df["known_label"] = df["known_label"].map(lambda x: "Benign" if x == 0.0 else "Attack")
df["predicted"] = get_preds("index")
df['is_wrong'] = df.apply(lambda x: x['predicted'] != x['known_label'], axis=1)

st.dataframe(df[["id", "datetime", "predicted", "known_label", "is_wrong", "tags", "embedding"]])


# # ---- SIDEBAR ----
# st.sidebar.header("Please Filter Here:")
# city = st.sidebar.multiselect(
#     "Select the City:",
#     options=df["City"].unique(),
#     default=df["City"].unique()
# )

# customer_type = st.sidebar.multiselect(
#     "Select the Customer Type:",
#     options=df["Customer_type"].unique(),
#     default=df["Customer_type"].unique(),
# )

# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )

# df_selection = df.query(
#     "City == @city & Customer_type ==@customer_type & Gender == @gender"
# )

# # # ---- MAINPAGE ----
# # st.title(":bar_chart: Sales Dashboard")
# # st.markdown("##")

# # # TOP KPI's
# # total_sales = int(df_selection["Total"].sum())
# # average_rating = round(df_selection["Rating"].mean(), 1)
# # star_rating = ":star:" * int(round(average_rating, 0))
# # average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

# # left_column, middle_column, right_column = st.columns(3)
# # with left_column:
# #     st.subheader("Total Sales:")
# #     st.subheader(f"US $ {total_sales:,}")
# # with middle_column:
# #     st.subheader("Average Rating:")
# #     st.subheader(f"{average_rating} {star_rating}")
# # with right_column:
# #     st.subheader("Average Sales Per Transaction:")
# #     st.subheader(f"US $ {average_sale_by_transaction}")

# # st.markdown("""---""")

# # # SALES BY PRODUCT LINE [BAR CHART]
# # sales_by_product_line = (
# #     df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
# # )
# # fig_product_sales = px.bar(
# #     sales_by_product_line,
# #     x="Total",
# #     y=sales_by_product_line.index,
# #     orientation="h",
# #     title="<b>Sales by Product Line</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
# #     template="plotly_white",
# # )
# # fig_product_sales.update_layout(
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     xaxis=(dict(showgrid=False))
# # )

# # # SALES BY HOUR [BAR CHART]
# # sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# # fig_hourly_sales = px.bar(
# #     sales_by_hour,
# #     x=sales_by_hour.index,
# #     y="Total",
# #     title="<b>Sales by hour</b>",
# #     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
# #     template="plotly_white",
# # )
# # fig_hourly_sales.update_layout(
# #     xaxis=dict(tickmode="linear"),
# #     plot_bgcolor="rgba(0,0,0,0)",
# #     yaxis=(dict(showgrid=False)),
# # )


# # left_column, right_column = st.columns(2)
# # left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
# # right_column.plotly_chart(fig_product_sales, use_container_width=True)




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
