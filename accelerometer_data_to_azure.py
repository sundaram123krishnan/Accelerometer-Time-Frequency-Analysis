import mpu6050
import time
from azure.iot.device import IoTHubDeviceClient, Message 
CONNECTION_STRING = "HostName=RaspberryConnectHub.azure-devices.net;DeviceId=raspberrypi4;SharedAccessKey=tasxOP9yBafXfJPgAK32tnaHSI4lBubhVAIoTLa4v4g="
MSG_SND = '{{"accelerometer": {accelerometer},"temperature": {temperature}}}'  

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    # Read temp
    temperature = mpu6050.get_temp()

    return accelerometer_data, gyroscope_data, temperature

def iothub_client_init():  
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)  
        return client 

def iothub_client_telemetry_sample_run():  
        try:  
            client = iothub_client_init()  
            print ( "Sending data to IoT Hub, press Ctrl-C to exit" )  

            while True:  
                accelerometer_data, gyroscope_data, temperature = read_sensor_data()
                msg_txt_formatted = MSG_SND.format(accelerometer=accelerometer_data, temperature=temperature)  
                message = Message(msg_txt_formatted)  
                print( "Sending message: {}".format(message) )  
                client.send_message(message)  
                print ( "Message successfully sent" )  
                time.sleep(3)  
        except KeyboardInterrupt:  
            print ( "IoTHubClient stopped" )  



# Start a while loop to continuously read the sensor data

if __name__ == '__main__':  
        print ( "Press Ctrl-C to exit" )  
        iothub_client_telemetry_sample_run()
