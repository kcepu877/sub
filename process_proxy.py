import pandas as pd
import requests
import asyncio
import aiohttp

# Masukkan API key Anda di sini
API_KEY = 'a1e6de2e232d4c'

# Fungsi untuk mendapatkan informasi ID dan ISP menggunakan ipinfo.io API
async def get_ip_info(session, ip):
    url = f"https://ipinfo.io/{ip}/json?token={API_KEY}"
    try:
        async with session.get(url) as response:
            data = await response.json()
            country = data.get('country', 'Unknown')  # Kode negara
            isp = data.get('org', 'Unknown')         # ISP
            # Hapus bagian 'AS' pada ISP jika ada
            if 'AS' in isp:
                isp = isp.split(' ')[1]  # Mengambil bagian setelah 'AS'
            return ip, country, isp
    except Exception as e:
        return ip, 'Unknown', 'Unknown'

# Fungsi utama untuk memproses file
async def process_proxy_file(file_name):
    # Membaca file proxy
    df = pd.read_csv(file_name, delimiter=',', header=None, names=['ip', 'port'])

    # Menyaring duplikat berdasarkan kolom 'ip' dan 'port'
    df_unique = df.drop_duplicates(subset=['ip', 'port'], keep='first')

    # Menyiapkan untuk melakukan request secara asynchronous
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _, row in df_unique.iterrows():
            ip = row['ip']
            tasks.append(get_ip_info(session, ip))

        # Menunggu hasil dari semua request
        results = await asyncio.gather(*tasks)

    # Memasukkan hasil ke dalam DataFrame
    df_unique[['ip', 'id', 'isp']] = pd.DataFrame(results, columns=['ip', 'id', 'isp'])

    # Menyimpan hasil ke file TXT
    output_file = 'proxy_ip_port_with_id_isp_async.txt'
    df_unique.to_csv(output_file, index=False, sep=',', header=False)

    print(f"File telah diproses dan disimpan di {output_file}")

# Menjalankan fungsi asynchronous
file_name = 'proxy_ip_port.txt'  # Nama file Anda
asyncio.run(process_proxy_file(file_name))
