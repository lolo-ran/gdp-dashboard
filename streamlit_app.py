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

# Initialize the line_chart with some empty data
st.write("Streaming Data...")
line_chart = st.line_chart([0] * MAX_POINTS)  # Initialize with dummy values

# Main loop for real-time data streaming
while True:
    try:
        # Receive data from the UDP socket
        sock.settimeout(0.1)  # Timeout to keep Streamlit UI responsive
        data, addr = sock.recvfrom(1024)  # Receive UDP packets
        # Decode the data
        value = struct.unpack('<i', data)[0]
        st.write(f"Received data value: {value}")
        # Update deque with received values
        data_queue.append(value)

        # Only redraw when deque has updated data
        if len(data_queue):
            # Send the latest window of data for plotting
            line_chart.line_chart_data = list(data_queue)

    except socket.timeout:
        pass  # If no UDP data is received, proceed without blocking

    # Short delay
    time.sleep(0.01)