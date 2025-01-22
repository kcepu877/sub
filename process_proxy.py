import pandas as pd

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

# Menyaring duplikat berdasarkan kolom 'ip' dan 'port'
df_unique = df.drop_duplicates(subset=['ip', 'port'], keep='first')

# Menyimpan hasil ke file TXT
output_file = 'proxy_ip_port_cleaned.txt'
df_unique.to_csv(output_file, index=False, sep=',', header=False)

# Menyediakan file untuk diunduh
print(f"File telah diproses dan disimpan di {output_file}")
