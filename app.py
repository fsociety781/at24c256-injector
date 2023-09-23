from flask import Flask, render_template, request, redirect, url_for, send_file
import smbus2
import time
import os
import csv
import pandas as pd
from datetime import datetime
from tinydb import TinyDB, Query

pin_led_green = 9  # Pin Pisik di Pin no 16
pin_led_blue = 10  # Pin Pisik di Pin no 18 
pin_led_red = 16   # Pin Pisik di Pin no 26

bus_number = 0
device_address = 0x50

bus = smbus2.SMBus(bus_number)

app = Flask(__name__)

def write_string_to_eeprom(start_address, data):
    os.system(f"gpio write {pin_led_blue} 0")
    for i in range(len(data)):
        msb = start_address >> 8
        lsb = start_address & 0xFF
        bus.write_i2c_block_data(device_address, msb, [lsb, ord(data[i])])
        time.sleep(0.01)
        start_address += 1
    os.system(f"gpio write {pin_led_blue} 0")

def read_string(address, length):
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

            save_data = {
                'barcode': write_barcode,
                'name': write_name,
                'token': write_token,
                'uuid': write_uuid,
                'jwt': write_jwt,
                'type': write_type,
                'version': write_version
            }

            data_str = ''
            for key, value in save_data.items():
                data_str += str(value) + ';'

            write_string_to_eeprom(0, data_str)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Database
            db = TinyDB('db.json')
            print("Check TinyDB")
            db.insert({'Datetime': current_time,'Barcode': write_barcode, 'Name': write_name})
            for item in db:
                print(item.doc_id, item)

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
    read_data = read_string(0, 1024)  

    print("Data yang dibaca dari EEPROM:", read_data)

    strArr = list(filter(None, read_data.split(';')))

    data = {
        'barcode': strArr[0],
        'name': strArr[1],
        'token': strArr[2],
        'uuid': strArr[3],
        'jwt': strArr[4],
        'type': strArr[5],
        'version': strArr[6]
    }

    print("Objek yang dihasilkan dari data EEPROM:", data)
    print("Barcode:", data['barcode'])
    print("Name:", data['name'])
    print("Token:", data['token'])
    print("UUID:", data['uuid'])
    print("JWT:", data['jwt'])
    print("Type:", data['type'])
    print("Version:", data['version'])

    return render_template('index.html', Barcode=data['barcode'], Name=data['name'], Token=data['token'], Uuid=data['uuid'], Jwt=data['jwt'], Type=data['type'], Version=data['version'])

@app.route('/download_history')
def download_history():
    try:
        return send_file('inject_history.csv', as_attachment=True)
    except FileNotFoundError:
        return "File not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



      

