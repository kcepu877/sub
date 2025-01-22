import pandas as pd
import asyncio
import aiohttp

# Masukkan API key Anda di sini
API_KEY = 'a1e6de2e232d4c'

# Fungsi untuk mendapatkan informasi ID dan ISP menggunakan ipinfo.io API
async def get_ip_info(session, ip):
    url = f"https://ipinfo.io/{ip}/json?token={API_KEY}"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                # Jika status tidak 200, kembalikan Unknown
                print(f"Failed to fetch data for IP: {ip}, Status Code: {response.status}")
                return ip, 'Unknown', 'Unknown'
            
            data = await response.json()
            country = data.get('country', 'Unknown')  # Kode negara
            isp = data.get('org', 'Unknown')         # ISP

            # Hapus bagian 'AS' pada ISP jika ada
            if 'AS' in isp:
                isp = isp.split(' ')[1]  # Mengambil bagian setelah 'AS'

            return ip, country, isp
    except Exception as e:
        print(f"Error fetching data for IP: {ip}, Error: {e}")
        return ip, 'Unknown', 'Unknown'

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
            tasks.append(get_ip_info(session, ip))

        # Menunggu hasil dari semua request
        results = await asyncio.gather(*tasks)

    # Memasukkan hasil ke dalam DataFrame
    # Mengonversi results menjadi DataFrame dan menggabungkannya dengan df_unique
    ip_info_df = pd.DataFrame(results, columns=['ip', 'id', 'isp'])

    # Menggabungkan DataFrame ip_info_df dengan df_unique berdasarkan kolom 'ip'
    df_unique = df_unique.merge(ip_info_df, on='ip', how='left')

    # Menyimpan hasil ke file TXT tanpa header dan tanpa AS pada ISP
    output_file = 'proxy_ip_port_with_id_isp_async.txt'
    df_unique.to_csv(output_file, index=False, sep=',', header=False)

    print(f"File telah diproses dan disimpan di {output_file}")

# Menjalankan fungsi asynchronous
file_name = 'proxy_ip_port.txt'  # Nama file Anda
asyncio.run(process_proxy_file(file_name))
