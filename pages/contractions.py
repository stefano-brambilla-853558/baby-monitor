import streamlit as st
import pandas as pd
from datetime import datetime
from src.utils import read_blob, write_blob, add_row_blob
from src.config import data_columns, data_files, Keys
import plotly.express as px
import plotly.graph_objects as go


mode = Keys.CONTRACTION
mode_prim = Keys.CONTRACTION_PRIMARY

df = read_blob(mode)
status = "End" if df.empty else df[df["Timestamp"] == df["Timestamp"].max()]["Type"].values[0]

if status == "End":
    button = st.button("START CONTRAPTION!")
else :
    button = st.button("END CONTRAPTION!")
# st.session_state.Intensity = "low"
# def set_intensity(level):
#     st.session_state.Intensity = level

# c1, c2, c3 = col2.columns(3)
# with c1:
#     level = "low"
#     if st.button(level, on_click=set_intensity, args=(level,)):
#         st.session_state.Intensity = level
# with c2:
#     level = "mid"
#     if st.button(level, on_click=set_intensity, args=(level,)):
#         st.session_state.Intensity = level
# with c3:
#     level = "high"
#     if st.button(level, on_click=set_intensity, args=(level,)):
#         st.session_state.Intensity = level

col1, col2 = st.columns(2)
calendar = col1.date_input("Data", datetime.now())
hour = col2.time_input("Ora", value=datetime.now(), step=60)
if button:
    if status == "End":
        row =  {
            "Timestamp": f"{calendar} {hour}",
            "Type": "Start",
            "Intensity": "",
            "Note": ""
        },
        add_row_blob(mode, row)
    if status == "Start":
        row =  {
            "Timestamp": f"{calendar} {hour}",
            "": "End",
            "Intensity": "", # st.session_state.Intensity,
            "Note": ""
        },
        add_row_blob(mode, row)
with st.expander("Visualizza le contrazioni"):
    df = read_blob(mode)
    df = st.data_editor(df, num_rows="dynamic")
    write_blob(mode, df)

df = read_blob(mode).sort_values(by="Timestamp", ascending=True)
df_prim = pd.DataFrame(columns=[
    "ID",
    "Timestamp_start",
    "Timestamp_end",
    "Duration",
    "Time_between",
    "Intensity",
    "Note"
])



start_time = None
id_counter = 1

for index, row in df.iterrows():
    if row["Type"] == "Start":
        start_time = datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
    elif row["Type"] == "End" and start_time is not None:
        end_time = datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
        duration = end_time - start_time
        if id_counter == 1:
            time_between = pd.Timedelta(0)
        else:
            time_between = start_time - prev_start_time

        df_prim = pd.concat([df_prim, pd.DataFrame([{
            "ID": id_counter,
            "Timestamp_start": start_time,
            "Timestamp_end": end_time,
            "Duration": duration,
            "Time_between": time_between,
            "Intensity": "",  # Add intensity if needed
            "Note": ""  # Add note if needed
        }])], ignore_index=True)

        prev_start_time = start_time
        start_time = None
        id_counter += 1

with st.expander("Correggi le contrazioni"):
    unmatched_starts = df[df["Type"] == "Start"].copy()
    unmatched_starts["End_Matched"] = unmatched_starts.apply(
        lambda row: any(
            (df["Type"] == "End") & 
            (df["Timestamp"] > row["Timestamp"]) & 
            (df["Timestamp"] <= (datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S") + pd.Timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
        ), axis=1
    )
    unmatched_starts = unmatched_starts[~unmatched_starts["End_Matched"]]
    unmatched_starts.drop(columns=["End_Matched"], inplace=True)

    st.write("Starts without an end:")
    st.data_editor(unmatched_starts)

with st.expander("Visualizza le contrazioni processate"):
    df_prim = st.data_editor(df_prim, num_rows="dynamic")

df_prim["Duration_minutes"] = df_prim["Duration"].dt.total_seconds() / 60
df_prim["Time_between_minutes"] = df_prim["Time_between"].dt.total_seconds() / 60
df_prim["Timestamp_start_from_zero"] = (df_prim["Timestamp_start"] - df_prim["Timestamp_start"].min()).dt.total_seconds() / 60

fig = px.scatter(df_prim, x="Timestamp_start", y="Duration_minutes", color="Intensity", title="Contractions")
st.plotly_chart(fig)
fig = px.scatter(df_prim, x="Time_between_minutes", y="Duration_minutes", color="Timestamp_start_from_zero", title="Contractions", color_continuous_scale=px.colors.sequential.Viridis)
st.plotly_chart(fig)