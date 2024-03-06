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

def plot_frequency_domain(data_x, data_y, data_z, sampling_rate, ax_freq):
    # Compute the FFT for each axis
    fft_x = np.abs(np.fft.fft(data_x))
    fft_y = np.abs(np.fft.fft(data_y))
    fft_z = np.abs(np.fft.fft(data_z))

    # Compute the frequencies
    freqs = np.fft.fftfreq(len(data_x), 1 / sampling_rate)

    # Plot frequency domain for each axis as sinusoidal curves
    ax_freq.plot(freqs[:len(data_x)//2], np.sin(fft_x[:len(data_x)//2]), label='X-axis', color='r')
    ax_freq.plot(freqs[:len(data_y)//2], np.sin(fft_y[:len(data_y)//2]), label='Y-axis', color='g')
    ax_freq.plot(freqs[:len(data_z)//2], np.sin(fft_z[:len(data_z)//2]), label='Z-axis', color='b')

    ax_freq.set_xlabel('Frequency (Hz)')
    ax_freq.set_ylabel('Magnitude')
    ax_freq.set_title('Frequency Domain (Sinusoidal)')
    ax_freq.legend()
    ax_freq.grid(True)

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("Sending data to IoT Hub, press Ctrl-C to exit")
        
        # Lists to store accelerometer data and time
        accelerometer_data = {'x': [], 'y': [], 'z': []}
        timestamps = []
        sampling_rate = None
        
        plt.ion()  # Turn on interactive mode
        
        fig, axs = plt.subplots(4, 1, figsize=(8, 10))  # Reduced width and height
        
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
            
            # Calculate sampling rate
            if len(timestamps) > 1:
                sampling_rate = len(timestamps) / (timestamps[-1] - timestamps[0])
            
            # Plot frequency domain every 100 samples
            if len(timestamps) >= 10:
                plot_frequency_domain(accelerometer_data['x'], accelerometer_data['y'], accelerometer_data['z'], sampling_rate, axs[-1])
                
                # Clear time domain data after plotting frequency domain
                timestamps.clear()
                accelerometer_data = {'x': [], 'y': [], 'z': []}
                
            # Plot time domain data
            for i, (axis, data) in enumerate(accelerometer_data.items()):
                axs[i].clear()
                axs[i].plot(timestamps, data)
                axs[i].set_ylabel(f'Accelerometer {axis}-axis')
                axs[i].set_title(f'Accelerometer {axis}-axis Data Over Time')
            axs[-1].set_xlabel('Time')
            
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
