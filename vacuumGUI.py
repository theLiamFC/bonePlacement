import PySimpleGUI as sg
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import matplotlib as plt
import json
import PS4Controller
import time

# MQTT Settings
mqtt_broker_address = "broker.hivemq.com"
mqtt_topic = "theVacuum"

# Important variables
fidelity = 5
mode = True
vac = False
startup = True

def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)

# PySimpleGUI Layout
leftFrame = [[sg.Frame("Settings",layout=[
        [sg.Text("Drive Mode: "), LEDIndicator('driveM')],
        [sg.Text("Surgery Mode: "), LEDIndicator('surgM')],
        [sg.Text("Motion Fidelity: 5",key="fidelity")],
])]]

rightFrame = [[sg.Frame("Status:",layout=[
        [sg.Text("",key="status")],
        [sg.Text("Vac Status: "), LEDIndicator('vac')]
])]]

layout = [
    [sg.Text("The Vacuum Car", font=("Helvetica", 20))],
    [sg.Column(leftFrame), sg.VSeparator(), sg.Column(rightFrame)],
    [sg.Image(size=(640, 480),filename="", key="image")],
    [sg.Canvas(size=(640, 480), key="graph_canvas")],
    [sg.Button("Exit")]
]

window = sg.Window("Robot Interface", layout, finalize=True)


# PS4 Controller Initializing
ps4 = PS4Controller.PS4Controller()
ps4.init()

# Initialize MQTT Client
client = mqtt.Client("RobotControl")

def draw_figure(canvas, figure):
   figure_canvas_agg = plt.FigureCanvasTkAgg(figure, canvas)
   figure_canvas_agg.draw()
   figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
   return figure_canvas_agg

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to MQTT topic
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        # Use data from MQTT for updating the line graph
        # Example: graph_elem.draw_line(...)
        
    except json.JSONDecodeError:
        print("Failed to decode MQTT message.")

client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_address)

# Main Event Loop
cap = cv2.VideoCapture(0)
graph_elem = window["graph_canvas"]
while True:
    if startup:
        buttons, joystick = ps4.listen()
        window["status"].update(value="Take 3 seconds to calibrate the controller.\nMove both joysticks in a full circle...")
        while len(joystick) < 4:
            event, values = window.read(timeout=20)
            buttons, joystick = ps4.listen()
            time.sleep(0.3)
        window["status"].update(value="Take 3 seconds to calibrate the controller.\nPull both triggers...")
        while len(joystick) < 6:
            event, values = window.read(timeout=20)
            buttons, joystick = ps4.listen()
            time.sleep(0.3)
        window["status"].update(value="Ready to suck")
        startup = False

    # read joystick input
    buttons, joystick = ps4.listen()

    # read gui input
    event, values = window.read(timeout=20)

    if buttons[6] and mode:
        mode = not mode
        SetLED(window, 'driveM', 'grey')
        SetLED(window, 'surgM', 'red')
        time.sleep(0.1)
    elif buttons[6] and not mode:
        mode = not mode
        SetLED(window, 'driveM', 'red')
        SetLED(window, 'surgM', 'grey')
        time.sleep(0.1)
    if buttons[4] and vac:
        vac = not vac
        SetLED(window, 'vac', 'grey')
        time.sleep(0.1)
    elif buttons[4] and not vac:
        vac = not vac
        SetLED(window, 'vac', 'red')
        time.sleep(0.1)
    if buttons[14]:
        fidelity = fidelity + 1
        if fidelity > 10:
            fidelity = 10
        window["fidelity"].update(value="Motion Fidelity: "+str(fidelity))
        time.sleep(0.1)
    if buttons[13]:
        fidelity = fidelity - 1
        if fidelity < 1:
            fidelity = 1
        window["fidelity"].update(value="Motion Fidelity: "+str(fidelity))
        time.sleep(0.1)

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    ret, frame = cap.read()
    if ret:
        resize = cv2.resize(frame, (960, 540))
        imgbytes = cv2.imencode(".png", resize)[1].tobytes()
        window["image"].update(data=imgbytes)

    # Send data to MQTT broker
    data_to_send = {
        "mode": mode,
        "motion_fidelity": fidelity,
        "vac": vac,
        "triangle": buttons[3],
        "circle": buttons[1],
        "x": buttons[0],
        "square": buttons[2],
        "up": buttons[11],
        "down": buttons[12],
        "left": buttons[13],
        "right": buttons[14],
        "leftJoyY": joystick[1],
        "leftJoyX": joystick[0],
        "rightJoyY": joystick[3],
        "rightJoyX": joystick[2],
        "leftTrig": joystick[4],
        "rightTrig": joystick[5],
    }

    mqttStatus, num = client.publish(mqtt_topic, json.dumps(data_to_send))

    if mqttStatus == 0:
        window["status"].update(value="MQTT connection is good")
    else:
        window["status"].update(value="Bad MQTT")

# Release resources
cap.release()
cv2.destroyAllWindows()
window.close()
