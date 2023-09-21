from flask import Flask, render_template, request, redirect, url_for, send_file
import smbus2
import time
import os
import csv
import pandas as pd
from datetime import datetime

# Konfigurasi pin GPIO dan I2C
pin_led_green = 9  # Pin Pisik di Pin no 16
pin_led_blue = 10  # Pin Pisik di Pin no 18 
pin_led_red = 16   # Pin Pisik di Pin no 26
bus_number = 0

device_address = 0x50
MAX_STRING_LENGTH = 256


os.system(f"gpio mode {pin_led_green} out")
os.system(f"gpio mode {pin_led_red} out")
os.system(f"gpio mode {pin_led_blue} out")

bus = smbus2.SMBus(bus_number)

app = Flask(__name__)

def write_string_to_eeprom(start_address, data):
    os.system(f"gpio write {pin_led_blue} 1")
    for i in range(len(data)):
        msb = start_address >> 8
        lsb = start_address & 0xFF
        bus.write_i2c_block_data(device_address, msb, [lsb, ord(data[i])])
        time.sleep(0.01)
        start_address += 1
    os.system(f"gpio write {pin_led_blue} 0")

def read_string(address, length):
    bus = smbus2.SMBus(0)
    bus.write_byte_data(device_address, (address >> 8) & 0xFF, address & 0xFF)
    time.sleep(0.005)

    data = []
    for _ in range(length):
        data.append(bus.read_byte(device_address))

    return "".join([chr(byte) for byte in data])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write_data', methods=['POST'])
def write_data():

    if request.method == 'POST':
        write_barcode = request.json['barcode']
        write_name = request.json['name']
        write_token = request.json['token']
        write_uuid = request.json['uuid']
        write_jwt = request.json['jwt']
        write_type = request.json['type']
        write_version = request.json['version']

        print(write_barcode, write_name, write_token, write_uuid, write_jwt, write_type, write_version)

        address = 0
        write_string_to_eeprom(address, write_barcode)
        address += len(write_barcode)
        write_string_to_eeprom(address, write_name)
        address += len(write_name)
        write_string_to_eeprom(address, write_token)
        address += len(write_token)
        write_string_to_eeprom(address, write_uuid)
        address += len(write_uuid)
        write_string_to_eeprom(address, write_jwt)
        address += len(write_jwt)
        write_string_to_eeprom(address, write_type)
        address += len(write_type)
        write_string_to_eeprom(address, write_version)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Membaca file CSV jika sudah ada atau membuatnya jika belum ada
        csv_file = 'inject_history.csv'
        fieldnames = ['Barcode', 'Name','Date']

        # Menambahkan data baru ke CSV
        with open(csv_file, mode='a', newline='') as history_file:
            history_writer = csv.DictWriter(history_file, fieldnames=fieldnames)

            # Jika file kosong, tulis header
            if os.stat(csv_file).st_size == 0:
                history_writer.writeheader()

            history_writer.writerow({
                'Barcode': write_barcode,
                'Name': write_name,
                'Date': current_time,
            })

        os.system(f"gpio write {pin_led_green} 1")
        time.sleep(2)
        os.system(f"gpio write {pin_led_green} 0")
        
        return redirect(url_for('index'))

@app.route('/read_data', methods=['POST'])
def read_data():
        
        feederBarcode = read_string(0, 22)
        feederName = read_string(22, 14)
        feederToken = read_string(36, 14)
        feederUuid = read_string(50, 36)
        feederJwt = read_string(86, 72)
        feederType = read_string(158, 4)
        feederVersion = read_string(162, 4)

        os.system(f"gpio write {pin_led_green} 1")
        time.sleep(2)
        os.system(f"gpio write {pin_led_green} 0")

        print("Feeder Barcode:", feederBarcode)
        print("Feeder Name:", feederName)
        print("Feeder Token:", feederToken)
        print("Feeder UUID:", feederUuid)
        print("Feeder JWT:", feederJwt)
        print("Feeder Type:", feederType)
        print("Feeder Version:", feederVersion)

        return render_template('index.html', Barcode=feederBarcode, Name=feederName, Token=feederToken, Uuid=feederUuid, Jwt=feederJwt, Type=feederType, Version=feederVersion)

@app.route('/download_history')
def download_history():
    try:
        return send_file('inject_history.csv', as_attachment=True)
    except FileNotFoundError:
        return "File not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
