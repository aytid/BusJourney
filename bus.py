import streamlit as st
import datetime
import matplotlib.pyplot as plt

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
    fig, ax = plt.subplots(figsize=(6, 6))
    seats = [(i, j) for i in range(4) for j in range(2)]  # 4 rows, 2 columns
    
    for seat in seats:
        color = "yellow" if (best_side == "Right" and seat[1] == 1) or (best_side == "Left" and seat[1] == 0) else "gray"
        ax.add_patch(plt.Rectangle((seat[1], -seat[0]), 1, 1, edgecolor='black', facecolor=color))
        ax.text(seat[1] + 0.5, -seat[0] + 0.5, f"{chr(65+seat[0])}{seat[1]+1}", 
                ha='center', va='center', fontsize=12, color='black')
    
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-4.5, 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Bus Seating Layout")
    st.pyplot(fig)

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

