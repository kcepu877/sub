import pandas as pd
import requests
import time

# Membaca file proxy_ip_port.txt yang hanya berisi ip dan port
file_name = 'proxy_ip_port.txt'  # Nama file input Anda
df = pd.read_csv(file_name, delimiter=',', header=None, names=['ip', 'port'])

# Fungsi untuk mendapatkan informasi id (kode negara) dan isp berdasarkan IP
def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")  # API ipinfo.io
        data = response.json()
        country = data.get('country', 'Unknown')  # Kode negara
        isp = data.get('org', 'Unknown')         # ISP
        return country, isp
    except Exception as e:
        return 'Unknown', 'Unknown'

# Fungsi untuk memproses IP dalam batch dengan penundaan
def process_batch(df_batch):
    # Menambahkan kolom id (kode negara) dan isp untuk batch
    df_batch[['id', 'isp']] = df_batch['ip'].apply(lambda x: pd.Series(get_ip_info(x)))
    return df_batch

# Membagi DataFrame menjadi batch kecil untuk memproses secara bertahap
batch_size = 1000  # Menentukan ukuran batch
all_results = []

# Proses IP dalam batch
for start in range(0, len(df), batch_size):
    end = min(start + batch_size, len(df))  # Menentukan batas akhir batch
    df_batch = df[start:end]  # Memilih batch
    print(f"Memproses batch {start // batch_size + 1} dari {len(df) // batch_size + 1}")
    df_batch_processed = process_batch(df_batch)
    all_results.append(df_batch_processed)
    time.sleep(1)  # Delay 1 detik untuk menghindari terlalu banyak permintaan dalam waktu singkat

# Menggabungkan hasil batch
df_result = pd.concat(all_results, ignore_index=True)

# Menyimpan hasil ke file proxy_ip_port_with_id_isp.txt
output_file = 'proxy_ip_port_with_id_isp.txt'
df_result.to_csv(output_file, index=False, sep=',', header=True)

print(f"File baru disimpan sebagai {output_file}")
