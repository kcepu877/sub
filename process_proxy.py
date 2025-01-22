import pandas as pd
import asyncio
import aiohttp

# Fungsi untuk mendapatkan informasi ID dan ISP menggunakan endpoint API custom
async def get_ip_info(session, ip, port):
    url = f"https://p01--boiling-frame--kw6dd7bjv2nr.code.run/check?ip={ip}&host=speed.cloudflare.com&port={port}&tls=true"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                country = data.get('country', 'Unknown')  # ID Negara
                isp = data.get('isp', 'Unknown')         # ISP
                return ip, port, country, isp
            else:
                return ip, port, 'Unknown', 'Unknown'
    except Exception as e:
        return ip, port, 'Unknown', 'Unknown'

# Fungsi utama untuk memproses file
async def process_proxy_file(file_name):
    # Membaca file proxy dengan pengecekan untuk jumlah kolom
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
            ip = row['ip']
            port = row['port']
            tasks.append(get_ip_info(session, ip, port))

        # Menunggu hasil dari semua request
        results = await asyncio.gather(*tasks)

    # Memasukkan hasil ke dalam DataFrame
    result_df = pd.DataFrame(results, columns=['ip', 'port', 'id', 'isp'])

    # Menyimpan hasil ke file TXT
    output_file = 'proxy_ip_port_with_id_isp_async.txt'  # Mengubah nama file output
    result_df.to_csv(output_file, index=False, sep=',', header=False)

    print(f"File telah diproses dan disimpan di {output_file}")

# Menjalankan fungsi asynchronous
file_name = 'proxy_ip_port.txt'  # Nama file Anda
asyncio.run(process_proxy_file(file_name))
