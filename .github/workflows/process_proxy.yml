import pandas as pd
import requests
import time

# Fungsi untuk mendapatkan ID (kode negara) dan ISP berdasarkan IP
def get_ip_info(ip, retries=3):
    api_key = 'a1e6de2e232d4c'  # Ganti dengan API Key Anda
    url = f"https://ipinfo.io/{ip}/json?token={api_key}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            data = response.json()
            if 'error' in data:
                print(f"Error for IP {ip}: {data['error']}")
                return 'Unknown', 'Unknown'
            country = data.get('country', 'Unknown')  # Kode negara
            isp = data.get('org', 'Unknown')         # ISP
            return country, isp
        except Exception as e:
            print(f"Error fetching info for IP {ip}: {e}")
            if attempt < retries - 1:
                time.sleep(2)  # Tunggu 2 detik sebelum mencoba lagi
            else:
                return 'Unknown', 'Unknown'

# Nama file proxy yang diunggah
file_name = "proxy_ip_port.txt"  # Nama file Anda

# Menangani kesalahan jika format baris salah
data = []
with open(file_name, 'r') as file:
    for line in file:
        try:
            parts = line.strip().split(',')
            if len(parts) == 2:  # Pastikan hanya ada 2 kolom (ip, port)
                data.append(parts)
        except Exception as e:
            print(f"Error parsing line: {line}, Error: {e}")

# Membuat DataFrame dengan data yang valid
df = pd.DataFrame(data, columns=['ip', 'port'])

# Menambahkan kolom 'id' dan 'isp' berdasarkan IP
df[['id', 'isp']] = df['ip'].apply(lambda x: pd.Series(get_ip_info(x)))

# Menyaring duplikat berdasarkan kolom 'ip' dan 'port'
df_unique = df.drop_duplicates(subset=['ip', 'port'], keep='first')

# Menyimpan hasil ke file TXT
output_file = 'proxy_ip_port_with_id_isp.txt'
df_unique.to_csv(output_file, index=False, sep=',', header=False)

# Menyediakan file untuk diunduh
print(f"File telah diproses dan disimpan di {output_file}")
