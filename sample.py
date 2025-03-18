import meshtastic
import meshtastic.serial_interface

# By default will try to find a meshtastic device,
# otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.serial_interface.SerialInterface(devPath = "COM11")

def on_receive(packet, iface):
    """Callback function that runs when a message is received"""
    if 'decoded' in packet and 'payload' in packet['decoded']:
        payload = packet['decoded']['payload']
        if 'text' in payload:
            message = payload['text']
        elif 'data' in payload:
                message = payload['data']
        else:
             message = "Unknown message type"
        sender = packet.get('fromId', 'Unknown')
        print(f"📩 Received from {sender}: {message}")

#register callback so it listens for incoming messages
interface.onReceive = on_receive

# or sendData to send binary data, see documentations for other options.
interface.sendText("hello from node 1")

ourNode = interface.getNode('^local')
print(f'Our node preferences:{ourNode.localConfig}')

# update a value
print('Changing a preference...')
ourNode.localConfig.position.gps_update_interval = 60

print(f'Our node preferences now:{ourNode.localConfig}')
ourNode.writeConfig("position")

# Keep the script running to listen for messages
print("🔍 Listening for incoming messages... (Press Ctrl+C to stop)")
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nExiting...")
interface.close()
