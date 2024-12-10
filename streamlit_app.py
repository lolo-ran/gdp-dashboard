import streamlit as st
import socket
import struct
import matplotlib.pyplot as plt
from collections import deque
import time

# Set up Streamlit UI
st.title("Lung Sounds Data Stream")

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

# Real-time Plot Loop
st.write("Streaming Data...")
while True:
    try:
        # Receive raw data from the UDP socket
        sock.settimeout(0.1)  # Add timeout to ensure Streamlit doesn't block
        data, addr = sock.recvfrom(1024)  # Buffer size
        # Decode the 32-bit integer from raw binary
        value = struct.unpack('<i', data)[0]
        data_queue.append(value)  # Add value to the deque
    except socket.timeout:
        pass  # No data received in timeout

    # Create real-time plot
    if len(data_queue) > 0:
        st.write("Current Data Stream:")

        # Plot the incoming data
        fig, ax = plt.subplots()
        ax.plot(list(data_queue), label="Filtered Values")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Amplitude")
        ax.set_title("Real-Time Data Plot")
        ax.legend()

        st.pyplot(fig)

    time.sleep(0.01)  # Short delay to pace UI updates

