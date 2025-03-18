import meshtastic.util
import time
import logging

# Enable logging
logging.basicConfig(level=logging.DEBUG)

def on_receive(packet, interface):
    """Callback function to handle received messages."""
    logging.info(f"Received message: {packet}")
    if 'decoded' in packet:
        logging.info(f"Decoded message: {packet['decoded']['payload'].decode('utf-8')}")

# Create an instance of SerialInterface
interface = meshtastic.serial_interface.SerialInterface()

# Set the callback for received messages
interface.onReceive = on_receive

# Send a message
interface.sendText("hello mesh")

# Keep the script running to listen for incoming messages
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Close the interface when the script is interrupted
    interface.close()
    logging.info("Interface closed.")