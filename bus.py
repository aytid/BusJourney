import streamlit as st
import datetime
import plotly.figure_factory as ff

def get_best_seat(time, direction):
    hour = time.hour
    morning = hour < 12
    evening = hour >= 16
    
    sun_side = {
        "North": "Right" if morning else "Left" if evening else None,
        "South": "Left" if morning else "Right" if evening else None,
        "East": "Front" if morning else "Back" if evening else None,
        "West": "Back" if morning else "Front" if evening else None,
    }
    
    if sun_side[direction] is None:
        return "Sun exposure is balanced. Any seat is fine."
    return f"Choose a seat on the {sun_side[direction]} side to minimize sun exposure."

def plot_bus_seating(best_side):
    labels = [["A1", "A2"], ["B1", "B2"], ["C1", "C2"], ["D1", "D2"], ["E1", "E2"]]
    colors = [["yellow" if (best_side == "Right" and j == 1) or (best_side == "Left" and j == 0) else "lightgray" for j in range(2)] for i in range(5)]
    
    fig = ff.create_annotated_heatmap(z=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], 
                                      annotation_text=labels, colorscale=colors, showscale=False)
    
    st.plotly_chart(fig)

st.title("Best Bus Seating for Sun Exposure Reduction")

col1, col2 = st.columns(2)

time = col1.time_input("Select Journey Time", datetime.datetime.now().time())
direction = col2.selectbox("Select Bus Direction", ["North", "South", "East", "West"])

if st.button("Find Best Seat"):
    best_seat = get_best_seat(time, direction)
    st.success(best_seat)
    if "Choose a seat on the" in best_seat:
        best_side = best_seat.split(" ")[-2]
        plot_bus_seating(best_side)
