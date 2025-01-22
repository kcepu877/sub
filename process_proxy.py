import pandas as pd
import asyncio
import aiohttp

# URL template API
API_URL = "https://p01--boiling-frame--kw6dd7bjv2nr.code.run/check?ip={ip}&host=speed.cloudflare.com&port={port}&tls=true"

# Fungsi untuk mendapatkan informasi dari API
async def get_ip_info(session, ip, port):
    url = API_URL.format(ip=ip, port=port)
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Ambil data yang relevan dari respons
                status = data.get("status", "Unknown")
                isp = data.get("isp", "Unknown")
                return ip, port, status, isp
            else:
                return ip, port, "Error", "Unknown"
    except Exception as e:
        return ip, port, "Error", "Unknown"

# Fungsi utama untuk memproses file
async def process_proxy_file(file_name):
    # Membaca file proxy
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:  # Hanya simpan baris dengan dua kolom (ip, port)
                data.append(parts)

    # Membaca data yang sudah difilter ke dalam DataFrame
    df = pd.DataFrame(data, columns=['ip', 'port'])

    # Menyaring duplikat berdasarkan kolom 'ip' dan 'port'
    df_unique = df.drop_duplicates(subset=['ip', 'port'], keep='first')

    # Menyiapkan untuk melakukan request secara asynchronous
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _, row in df_unique.iterrows():
            ip, port = row['ip'], row['port']
            tasks.append(get_ip_info(session, ip, port))

        # Menunggu hasil dari semua request
        results = await asyncio.gather(*tasks)

    # Menggabungkan hasil ke dalam DataFrame
    ip_info_df = pd.DataFrame(results, columns=['ip', 'port', 'status', 'isp'])
    df_final = pd.merge(df_unique, ip_info_df, on=['ip', 'port'], how='left')

    # Menyimpan hasil ke file TXT
    output_file = 'proxy_ip_port_with_status_isp.txt'
    df_final.to_csv(output_file, index=False, sep=',', header=False)

    print(f"File telah diproses dan disimpan di {output_file}")

# Menjalankan fungsi asynchronous
file_name = 'proxy_ip_port.txt'  # Nama file Anda
asyncio.run(process_proxy_file(file_name))
