import pandas as pd
import asyncio
import aiohttp

# Fungsi untuk mendapatkan informasi IP dari ProxyCheck.io
async def get_ip_info(session, ip, port):
    url = f"https://proxycheck.io/v2/{ip}?vpn=1&asn=1"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                country = data.get('country', 'Unknown')
                isp = data.get('isp', 'Unknown')
                return ip, port, country, isp
            else:
                return ip, port, "Unknown", "Unknown"
    except Exception as e:
        return ip, port, "Unknown", "Unknown"

# Fungsi utama untuk memproses file
async def process_proxy_file(file_name):
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                data.append(parts)

    df = pd.DataFrame(data, columns=['ip', 'port'])
    df_unique = df.drop_duplicates(subset=['ip', 'port'], keep='first')

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _, row in df_unique.iterrows():
            ip = row['ip']
            port = row['port']
            tasks.append(get_ip_info(session, ip, port))

        results = await asyncio.gather(*tasks)

    ip_info_df = pd.DataFrame(results, columns=['ip', 'port', 'country', 'isp'])
    df_unique = pd.merge(df_unique, ip_info_df, on=['ip', 'port'], how='left')

    output_file = 'proxy_ip_port_with_id_isp_async.txt'
    df_unique.to_csv(output_file, index=False, sep=',', header=False)

    print(f"File telah diproses dan disimpan di {output_file}")

# Memulai proses
file_name = 'proxy_ip_port.txt'
asyncio.run(process_proxy_file(file_name))
