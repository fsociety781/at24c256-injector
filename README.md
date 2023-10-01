# Guide Installation

Web APP at24c256 Injector Eeprom

## Note
Password default pada Orange Pi : orangepi

## A. Setup Orange Pi

Setup terlebih dahulu orangepi nya agar bisa menjalankan Web App ini.

1.    Setup Orange (Untuk memperbarui sistem debian yang terinstall di orange pi)
      - [1. Buka terminal pada Orange Pi ]
      - [2. Ketik pada terminal ```sudo apt-get update ```, untuk mengambil daftar paket terbaru (metadata) dari repositori paket Debian.]
      - [3. Ketik pada terminal ```sudo apt-get upgrade```, untuk memperbarui semua paket yang ada ke versi terbaru. ]
      - [4. Done Debian sudah terupdate pada package terbaru.]
2.    Install Tools dan Software
      Bertujuan Untuk dapat Menjalankan Web Aplikasi ini.
      - [1. Buka terminal pada Orange Pi ]
      - [2. Install pip untuk install liblary yang di butuhkan ```sudo apt-get install python3-pip```.]
      - [3. Install Flask ```sudo pip3 install flask```,framework web pada python.]
      - [4. Install smbus2 ```sudo pip3 install smbus2```,library untuk berkomunikasi dengan perangkat yang terhubung melalui protokol I2C.]
      - [5. Install tinydb ```sudo pip3 install tinydb```,liblary database untuk mengelola data.]
4.    Setting i2c pin
      Tambahkan konfigurasi i2c pada ENV orangepi agar bisa berjalan.
      - [1. Buka terminal pada Orange Pi ]
      - [2. Edit file ```orangepiEnv.txt``` dengan cara buka berkas dengan perintah pada terminal ```sudo nano /boot/orangepiEnv.txt```.]
      - [3. Tambahkan code ```overlays=i2c0``` pada file```orangepiEnv.txt``` tersebut.]
      - [4. Save file nya dengan cara tekan kombinasi```CTRL + O``` lalu Enter.]
      - [5. Keluar dari file tersebu dengan menekan kombinasi ```CTRL + X``` lalu Enter.]
      - [6. Kemudian restart Orange Pi dengan masukan perintah ```sudo reboot```]
      - [7. Setelah reboot cek apakah i2c sudah bisa terpakai dan mendeteksi perangkat dengan cara ```sudo i2cdetect -y 0```.]
      - [8. Done.]
6.    Setting Pin io
      Setting ini bertujuan agar membuka konfigurasi input dan ouput dari pin io yang ada di Orange Pi
      - [1. Buka terminal pada Orange Pi ]
      - [2. Clone tools untuk setting pin io pada repo github ini : ```https://github.com/orangepi-xunlong/wiringOP.git```.]
      - [3. Masuk ke folder direktori wiringOPnya ketikan perintah ```cd wiringOP```.]
      - [4. Lalu build tool nya dengan ketik perintah```sudo ./build clean``` dan ```sudo ./build``` untuk membuil tool agar bisa di pakai.]
      - [5. Setelah selesai ketik ```sudo gpio readall``` untuk melihat settingan awal pada Orange Pi.]
      - [6. Kemudian setting pin beberapa pin io sesui denga kebutuhan dengan ketik perintah ```sudo gpio mode (pin yang akan di setting) ALT3```]
        -[Contoh]
        -[untuk pin 9 pada pin pisiknya terdapat pada pin ke 16 ```gpio mode 9 alt3```]
        -[untuk pin 10 pada pin pisiknya terdapat pada pin ke 18 ```gpio mode 10 alt3```]
        -[untuk pin 16 pada pin pisiknya terdapat pada pin ke 26 ```gpio mode 16 alt3```]  
      - [7. Setelah kemudian reboot Orange Pinya ```sudo reboot```.]
      - [9. Setelah setelah reboot cek apakah sudah berubah settingan nya dengan melakukan kembali langkah no 1 sampai 5.]
      - [8. Done.]
    

## B. Instalasi Perangkat Lunak dan Alat yang Diperlukan

Untuk menginstal perangkat lunak dan alat yang diperlukan, ikuti instruksi berikut:

- [Instruksi 1: Buka terminal pada Orange Pi.]
- [Instruksi 2: Gunakan perintah `apt-get` atau `pip` untuk menginstal perangkat lunak yang diperlukan.]
- [Langkah 1: Buka terminal pada Orange Pi.]
- [Langkah 2: Gunakan perintah `git clone` untuk mengklon repositori dari Bitbucket.]
- [Langkah 3: Konfigurasikan dan jalankan perangkat lunak sesuai instruksi yang ada.]
