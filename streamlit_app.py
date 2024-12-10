import streamlit as st
import socket
import struct
from collections import deque
import time

# Set up Streamlit UI
st.title("Real-Time UDP Data Stream with add_rows")

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

# Initialize line chart
st.write("Streaming Data...")
line_chart = st.line_chart([0] * MAX_POINTS)  # Dummy initial values

while True:
    try:
        # Receive data from the UDP socket
        sock.settimeout(0.1)  # Timeout to ensure Streamlit doesn't hang
        data, addr = sock.recvfrom(1024)  # Receive UDP packets
        value = struct.unpack('<i', data)[0]  # Decode the UDP packet

        # Add received value to deque for visualization
        data_queue.append(value)

        # Use add_rows to dynamically add values to the chart
        if len(data_queue) > 0:
            line_chart.add_rows([[value]])  # Dynamically append only new data

    except socket.timeout:
        pass  # Handle timeout gracefully

    # Allow Streamlit loop to stay responsive
    time.sleep(0.01)