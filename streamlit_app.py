import streamlit as st
import socket
import struct
from collections import deque
import time

# Constants
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005
MAX_POINTS = 100

# Set up Streamlit UI
st.title("Lung Sounds Data Stream")

# Initialize or retrieve shared resources
if "data_queue" not in st.session_state:
    st.session_state.data_queue = deque(maxlen=MAX_POINTS)
if "line_chart" not in st.session_state:
    st.session_state.line_chart = st.line_chart([0] * MAX_POINTS)
if "udp_socket" not in st.session_state:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(0.1)
    st.session_state.udp_socket = sock
else:
    sock = st.session_state.udp_socket

# Clear Chart Button
if st.button("Clear Chart"):
    st.session_state.data_queue.clear()
    st.session_state.line_chart = st.line_chart([0] * MAX_POINTS)  # Create a new chart instance

# Listen for UDP data
try:
    while True:
        try:
            # Receive data from the UDP socket
            data, addr = sock.recvfrom(1024)  # Receive UDP packets
            value = struct.unpack('<i', data)[0]  # Decode the UDP packet

            # Add received value to deque for visualization
            st.session_state.data_queue.append(value)

            # Update the chart with the new value
            st.session_state.line_chart.add_rows([[value]])  # Dynamically append only new data
        except socket.timeout:
            pass  # Handle timeout gracefully

        # Allow Streamlit loop to stay responsive
        time.sleep(0.01)
except KeyboardInterrupt:
    sock.close()