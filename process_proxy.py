import pandas as pd
import requests

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

# Fungsi untuk mendapatkan id (kode negara) dan ISP berdasarkan IP
def get_ip_info(ip):
    try:
        # Menggunakan API ipinfo.io untuk mendapatkan informasi IP
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        country = data.get('country', 'Unknown')  # Kode negara
        isp = data.get('org', 'Unknown')         # ISP
        return country, isp
    except Exception as e:
        return 'Unknown', 'Unknown'

# Menambahkan kolom 'id' dan 'isp' berdasarkan IP
df[['id', 'isp']] = df['ip'].apply(lambda x: pd.Series(get_ip_info(x)))

# Menyaring duplikat berdasarkan kolom 'ip' dan 'port'
df_unique = df.drop_duplicates(subset=['ip', 'port'], keep='first')

# Menyimpan hasil ke file TXT
output_file = 'proxy_ip_port_with_id_isp.txt'
df_unique.to_csv(output_file, index=False, sep=',', header=False)

# Menyediakan file untuk diunduh
print(f"File telah diproses dan disimpan di {output_file}")
