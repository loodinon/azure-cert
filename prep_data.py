import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_ag_grid as dag
from datetime import datetime
import pathlib


def load_data(data_file):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(data_file))


def get_content():
    df = load_data("cert_list.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%b-%y")
    df["Name_link"] = df.apply(lambda row: f"[{row['Name']}]({row['Link']})"
                               if not pd.isna(row['Link']) else row['Name'], axis=1)
    return df


df = get_content()

df1 = df.groupby("Date").count()["Name"].reset_index().rename(
    {"Name": "Count"}, axis=1)
total_cert = sum(df1["Count"])

min_date = df1['Date'].min()
max_date = datetime.today().date()
month_diff = (max_date.year - min_date.year) * \
    12 + (max_date.month - min_date.month)
year = month_diff // 12
month = month_diff - year * 12

MAIN_COLOR = 'rgb(49,130,200)'
SUB_COLOR = 'rgb(150,150,150)'

CHART_HEIGHT = '74vh'

AXIS_COLOR = 'rgb(204, 204, 204)'

PLOT_TITLE_FONT = dict(
    family="Bahnschrift SemiCondensed",
    size=40
)

SUB_PLOT_TITLE_FONT = dict(
    family="Bahnschrift Condensed",
    size=24
)

HOVER_LABEL = dict(
    bgcolor="rgb(240,240,240)",
    font_size=16,
    font_family="Bahnschrift"
)

TICK_FONT = dict(
    family='Bahnschrift Light',
    color='rgb(82, 82, 82)',
)

DARKER_TICK_FONT = dict(
    family='Bahnschrift',
    color='rgb(40, 40, 40)',
)

# FIG1 (main line chart)
start_date = datetime(df1['Date'].min().year, 1, 1)
end_date = datetime.today().date()
date_range = pd.date_range(start=start_date, end=end_date, freq='MS')

df_all_dates = pd.DataFrame({'Date': date_range})
df_merged = pd.merge(df_all_dates, df1, on='Date', how='left')
df_merged['Count'] = df_merged['Count'].fillna(0)
df_merged['CumCount'] = df_merged['Count'].cumsum()
df_merged["Year"] = df_merged["Date"].dt.year
df_merged["Month"] = df_merged["Date"].dt.strftime('%b')


fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True)
fig1.add_trace(go.Scatter(
    x=[df_merged["Year"], df_merged["Month"]],
    y=df_merged["Count"],
    line=dict(color=MAIN_COLOR, width=6),
    name="# Certs",
    hoverinfo='name+y',
),
    row=2, col=1
)
fig1.add_trace(go.Scatter(
    x=[df_merged["Year"], df_merged["Month"]],
    y=df_merged["CumCount"],
    line=dict(color=SUB_COLOR, width=3),
    name="Cum. Certs",
    hoverinfo='name+y',
),
    row=1, col=1
)

fig1.update_layout(
    title=dict(
        text=f"<span style='color:{MAIN_COLOR};'>Number of Certs</span> <span \
                style='color:rgb(170,170,170);'> and </span> <span \
                style='color:{SUB_COLOR};'>Cummulative Certs</span>",
        x=0.03,
        y=1,
        font=PLOT_TITLE_FONT
    ),
    autosize=True,
    margin=dict(l=10, r=10, t=50, b=45),
    xaxis2=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor=AXIS_COLOR,
        linewidth=2,
        ticks='outside',
        tickfont=TICK_FONT,
        showspikes=True,
        spikemode='across+toaxis',
        spikesnap='cursor',
        spikedash='solid'
    ),
    yaxis1=dict(
        domain=[0.75, 1],
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor=AXIS_COLOR,
        linewidth=2,
        ticks='outside',
        tickfont=TICK_FONT,
    ),
    yaxis2=dict(
        domain=[0.0, 0.73],
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor=AXIS_COLOR,
        linewidth=2,
        ticks='outside',
        tickfont=TICK_FONT,
    ),
    hoversubplots="axis",
    hoverlabel=HOVER_LABEL,
    plot_bgcolor='white',
    showlegend=False,
    hovermode='x',
    spikedistance=-1,
    legend_traceorder="normal"
)
fig1.update_traces(xaxis='x2')


# FIG2 (group hbar)
df2 = df.groupby("Group").count()["Name"].reset_index().rename(
    {"Name": "Count"}, axis=1).sort_values(["Count"]).reset_index(drop=True)

fig2 = go.Figure(go.Bar(
    x=df2["Count"],
    y=df2["Group"],
    orientation='h',
    hovertemplate='%{y}: %{x}<extra></extra>',
    marker={"color": SUB_COLOR}
))

fig2.update_layout(
    title=dict(
        text=f"<span style='color:{SUB_COLOR};'>By Topic</span>",
        x=0.03,
        y=1,
        font=SUB_PLOT_TITLE_FONT
    ),
    autosize=True,
    margin=dict(l=0, r=10, t=40, b=0),
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor=AXIS_COLOR,
        linewidth=2,
        ticks='outside',
        tickfont=TICK_FONT,
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        tickfont=dict(
            family='Bahnschrift',
            size=10,
            color='rgb(40, 40, 40)',
        ),
    ),
    xaxis_title="",
    yaxis_title="",
    hoverlabel=HOVER_LABEL,
    plot_bgcolor='white',
    showlegend=False,
)

# fig3 (org hbar)
bound = 5
df3 = df.groupby("Organization").count()[
    "Name"].reset_index().rename({"Name": "Count"}, axis=1)
less_than_10 = df3[df3['Count'] < bound]
aggregated_row = pd.DataFrame(less_than_10.sum()).T
aggregated_row.iloc[0, 0] = "Others"
df3 = df3[df3['Count'] >= bound]
df3 = pd.concat([df3, aggregated_row], ignore_index=True)
df3 = df3.sort_values(["Count"]).reset_index(drop=True)

fig3 = go.Figure(go.Bar(
    x=df3["Count"],
    y=df3["Organization"],
    orientation='h',
    hovertemplate='%{y}: %{x}<extra></extra>',
    marker={"color": SUB_COLOR}
))

fig3.update_layout(
    title=dict(
        text=f"<span style='color:{SUB_COLOR};'>By Organization</span>",
        x=0.03,
        y=1,
        font=SUB_PLOT_TITLE_FONT
    ),
    autosize=True,
    margin=dict(l=130, r=10, t=40, b=0),
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor=AXIS_COLOR,
        linewidth=2,
        ticks='outside',
        tickfont=TICK_FONT,
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        tickfont=dict(
            family='Bahnschrift',
            size=12,
            color='rgb(40, 40, 40)',
        ),
    ),
    xaxis_title="",
    yaxis_title="",
    hoverlabel=HOVER_LABEL,
    plot_bgcolor='white',
    showlegend=False,
)

# fig4 (table)
df4 = df.loc[:, ["Date", "Name_link", "Group", "Organization"]]
df4["Date"] = df4["Date"].dt.strftime('%Y-%m')

column_defs = [
    {
        "headerName": "Date",
        "field": "Date",
        "width": 150,
        "lockPosition": "left"
    },
    {
        "headerName": "Name",
        "field": "Name_link",
        'cellRenderer': 'markdown',
        "flex": 3,
        "lockPosition": "left"
    },
    {
        "headerName": "Topic",
        "field": "Group",
        "flex": 1,
        "lockPosition": "left"
    },
    {
        "headerName": "Organization",
        "field": "Organization",
        "flex": 1,
        "lockPosition": "left"
    },
]

table4 = dag.AgGrid(
    rowData=df4.to_dict("records"),
    columnDefs=column_defs,
    defaultColDef={"sortable": True,
                   "filter": True,
                   "resizable": False},
    style={"height": CHART_HEIGHT}
)
