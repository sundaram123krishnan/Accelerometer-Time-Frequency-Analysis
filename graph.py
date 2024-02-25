import mpu6050
import time
import numpy as np
import matplotlib.pyplot as plt
from azure.iot.device import IoTHubDeviceClient, Message 

CONNECTION_STRING = "HostName=RaspberryConnectHub.azure-devices.net;DeviceId=raspberrypi4;SharedAccessKey=tasxOP9yBafXfJPgAK32tnaHSI4lBubhVAIoTLa4v4g="
MSG_SND = '{{"accelerometer": {accelerometer},"temperature": {temperature}}}'

# Create a new Mpu6050 object
mpu6050_sensor = mpu6050.mpu6050(0x68)

# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050_sensor.get_accel_data()
    
    # Read temp
    temperature = mpu6050_sensor.get_temp()

    return accelerometer_data, temperature

def iothub_client_init():  
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)  
    return client 

def iothub_client_telemetry_sample_run():  
    try:  
        client = iothub_client_init()  
        print("Sending data to IoT Hub, press Ctrl-C to exit")
        
        # Lists to store accelerometer data and time
        accelerometer_y_data = []
        timestamps = []
        
        plt.ion()  # Turn on interactive mode
        
        fig, ax = plt.subplots()  # Create figure and axis objects
        
        while True:  
            accelerometer_data, temperature = read_sensor_data()
            accelerometer_y = accelerometer_data['y']
            
            # Append data to lists
            accelerometer_y_data.append(accelerometer_y)
            timestamps.append(time.time())
            
            msg_txt_formatted = MSG_SND.format(accelerometer=accelerometer_data, temperature=temperature)  
            message = Message(msg_txt_formatted)  
            client.send_message(message)
            
            print("Message successfully sent")
            
            # Update plot
            ax.clear()
            ax.plot(timestamps, accelerometer_y_data)
            ax.set_xlabel('Time')
            ax.set_ylabel('Accelerometer Y-axis')
            ax.set_title('Accelerometer Y-axis Data Over Time')
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            time.sleep(1)
    except KeyboardInterrupt:  
        print("IoTHubClient stopped")
        plt.ioff()  # Turn off interactive mode
        plt.show()

if __name__ == '__main__':  
    print("Press Ctrl-C to exit")  
    iothub_client_telemetry_sample_run()

