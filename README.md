# Accelerometer Data Analysis: Time and Frequency Domain Visualization

This project is aimed at analyzing accelerometer data by plotting time domain graphs and then converting them into frequency domain graphs using Fast Fourier Transform (FFT) in Python. The accelerometer data is pushed to Azure for storage and analysis.

## Introduction

Accelerometers are sensors that measure acceleration and are commonly used in various applications, including motion sensing in mobile devices, activity tracking, vibration analysis, and more. Analyzing accelerometer data can provide valuable insights into motion patterns, vibrations, and other phenomena.

This project focuses on processing accelerometer data and visualizing it in both the time and frequency domains. The primary steps involved in this analysis include:

1. Data Acquisition: Obtaining accelerometer data from sensors or pre-recorded datasets.
2. Data Push to Azure: Pushing the acquired data to Azure for storage and further analysis.
3. Time Domain Analysis: Plotting time series graphs to visualize the raw accelerometer data.
4. Frequency Domain Analysis: Converting time domain signals into frequency domain using Fast Fourier Transform (FFT) to identify dominant frequencies and spectral characteristics.

## Requirements

- Python 3.x
- NumPy
- Matplotlib
- Azure SDK for Python

## Usage

1. Ensure you have an Azure account and set up Azure Blob Storage for data storage.
2. Configure Azure credentials in your environment.
3. Modify the `push_to_azure.py` script to include your Azure Blob Storage details.
4. Provide accelerometer data as input to the `push_to_azure.py` script.
5. Run the script to push data to Azure.
6. Use the `analyze_accelerometer_data.py` script to perform analysis and generate visualizations locally.

Example usage:
## Azure IOT Hub:
![image](https://github.com/sundaram123krishnan/Accelerometer-Analysis-Time-Frequency/assets/104441812/b55ef837-9833-4a32-bbe8-778fd170683d)

## Time and Frequency domain graph
![image](https://github.com/sundaram123krishnan/Accelerometer-Analysis-Time-Frequency/assets/104441812/1c097606-6670-43ed-a548-c05f0492af2b)




