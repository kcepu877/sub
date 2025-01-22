import pandas as pd
import asyncio
import aiohttp

# Masukkan API key Anda di sini
API_KEY = '157683ca5f7ec12a96671988855e5b59'  # Gantilah dengan API key Anda

# Fungsi untuk mendapatkan informasi ID dan ISP menggunakan ipapi.com API
async def get_ip_info(session, ip):
    url = f"https://api.ipapi.com/{ip}?access_key={API_KEY}&fields=country,org"
    try:
        async with session.get(url) as response:
            if response.status == 200:  # Hanya proses jika status OK
                data = await response.json()
                country = data.get('country', 'Unknown')  # Kode negara
                isp = data.get('org', 'Unknown')         # ISP
                # Hapus bagian 'AS' pada ISP jika ada
                if 'AS' in isp:
                    isp = isp.split(' ')[1]  # Mengambil bagian setelah 'AS'
                return ip, country, isp
            else:
                return ip, 'Unknown', 'Unknown'
    except Exception as e:
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

    # Menggabungkan hasil ke dalam DataFrame
    ip_info_df = pd.DataFrame(results, columns=['ip', 'country', 'isp'])
    df_unique = pd.merge(df_unique, ip_info_df, on='ip', how='left')

    # Menyimpan hasil ke file TXT
    output_file = 'proxy_ip_port_with_id_isp_async.txt'
    df_unique.to_csv(output_file, index=False, sep=',', header=False)

    print(f"File telah diproses dan disimpan di {output_file}")

# Menjalankan fungsi asynchronous
file_name = 'proxy_ip_port.txt'  # Nama file Anda
asyncio.run(process_proxy_file(file_name))
