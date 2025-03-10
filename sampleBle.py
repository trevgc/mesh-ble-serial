import meshtastic
import meshtastic.ble_interface
import time
import asyncio

# Bluetooth MAC address
DEVICE_ADDRESS = "CC:BA:97:0E:FF:21"  

# ✅ Step 1: Ensure Your Meshtastic Device is Already Paired!
print("🔗 Ensure your Meshtastic device is paired via system Bluetooth settings.")
print("⏳ Waiting 5 seconds before attempting to connect...")
time.sleep(5)  # Give time for manual pairing if needed

# ✅ Step 2: Attempt to Connect to the Meshtastic Device
try:
    print(f"🔗 Attempting to connect to {DEVICE_ADDRESS} via Bluetooth...")
    interface = meshtastic.ble_interface.BLEInterface(address=DEVICE_ADDRESS)
    print("✅ Successfully connected via Bluetooth!")
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    exit(1)

# ✅ Step 3: Define a Callback Function for Incoming Messages
def on_receive(packet, iface):
    """Callback function that runs when a message is received"""
    if 'decoded' in packet and 'payload' in packet['decoded']:
        if 'text' in packet['decoded']['payload']:
            message = packet['decoded']['payload']['text']
            sender = packet['fromId']
            print(f"📩 Received from {sender}: {message}")

# ✅ Register the callback to listen for incoming messages
interface.onReceive = on_receive

# ✅ Step 4: Send a Test Message
interface.sendText("Hello from Bluetooth laptop!")

# ✅ Step 5: Retrieve Local Node Configuration
ourNode = interface.getNode('^local')
print(f'Our node preferences: {ourNode.localConfig}')

# ✅ Step 6: Modify a Configuration Setting
print('Changing a preference...')
ourNode.localConfig.position.gps_update_interval = 60
print(f'Updated preferences: {ourNode.localConfig}')
ourNode.writeConfig("position")

# ✅ Step 7: Keep Listening for Messages
print("🔍 Listening for incoming messages... (Press Ctrl+C to stop)")
try:
    while True:
        time.sleep(1)  # Keep the script alive efficiently
except KeyboardInterrupt:
    print("\n🔌 Closing connection...")
    interface.close()
    print("✅ Connection closed. Exiting...")
