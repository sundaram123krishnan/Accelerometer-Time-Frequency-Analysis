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
        accelerometer_data = {'x': [], 'y': [], 'z': []}
        timestamps = []
        
        plt.ion()  # Turn on interactive mode
        
        fig, ax = plt.subplots(3, 1, figsize=(10, 10), sharex=True)  # Create figure and axis objects with shared x-axis
        
        plt.subplots_adjust(hspace=0.5)  # Adjust vertical space between subplots
        
        while True:  
            accelerometer_data_raw, temperature = read_sensor_data()
            accelerometer_data['x'].append(accelerometer_data_raw['x'])
            accelerometer_data['y'].append(accelerometer_data_raw['y'])
            accelerometer_data['z'].append(accelerometer_data_raw['z'])
            timestamps.append(time.time())
            
            msg_txt_formatted = MSG_SND.format(accelerometer=accelerometer_data_raw, temperature=temperature)  
            message = Message(msg_txt_formatted)  
            client.send_message(message)

	    
            
            print("Message successfully sent")
            print(accelerometer_data_raw)
            
            # Update plot
            for i, (axis, data) in enumerate(accelerometer_data.items()):
                ax[i].clear()
                ax[i].plot(timestamps, data)
                ax[i].set_ylabel(f'Accelerometer {axis}-axis')
                ax[i].set_title(f'Accelerometer {axis}-axis Data Over Time')
            ax[2].set_xlabel('Time')  # Set x-label only for the last subplot
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
