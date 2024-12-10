import streamlit as st
import socket
import struct
from collections import deque
import time

# Set up Streamlit UI
st.title("Real-Time UDP Data Stream")

# Set the maximum number of data points to display on the plot
MAX_POINTS = 100

# Set up UDP socket to listen
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

st.write("Listening for UDP packets...")

# Set up a deque to hold incoming data for plotting
data_queue = deque(maxlen=MAX_POINTS)

# Use Streamlit's line_chart for efficient dynamic plotting
st.write("Streaming Data...")
line_chart = st.line_chart([0] * MAX_POINTS)  # Initialize with empty data

while True:
    try:
        # Receive raw data from the UDP socket
        sock.settimeout(0.1)  # Add timeout to ensure Streamlit doesn't block
        data, addr = sock.recvfrom(1024)  # Buffer size
        # Decode the 32-bit integer from raw binary
        value = struct.unpack('<i', data)[0]
        
        # Update the data queue with new data
        data_queue.append(value)
        
        # Update the line chart dynamically with data only when deque is updated
        if len(data_queue) > 0:
            line_chart.line_chart_data = list(data_queue)  # Send only recent deque data for plotting

    except socket.timeout:
        # Handle timeout gracefully
        continue

    # Wait a tiny bit to pace the loop
    time.sleep(0.01)