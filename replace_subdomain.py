import random
import string
import os
import yaml

# Fungsi untuk menghasilkan subdomain acak
def generate_random_subdomain(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Fungsi untuk mengganti subdomain "ns1.cepu.us.kg" dengan subdomain acak di wrangler.toml
def replace_subdomain_in_toml(toml_file, new_subdomain):
    with open(toml_file, 'r') as file:
        lines = file.readlines()

    # Ganti "ns1.cepu.us.kg" dengan subdomain acak di setiap baris yang mengandung "ns1.cepu.us.kg"
    updated_lines = []
    for line in lines:
        if 'ns1.cepu.us.kg' in line:
            line = line.replace('ns1.cepu.us.kg', f'{new_subdomain}.cepu.us.kg')
        updated_lines.append(line)

    with open(toml_file, 'w') as file:
        file.writelines(updated_lines)

# Fungsi untuk mengganti subdomain "ns1.cepu.us.kg" dengan subdomain acak di index.html
def replace_subdomain_in_html(html_file, new_subdomain):
    with open(html_file, 'r') as file:
        content = file.read()

    updated_content = content.replace('ns1.cepu.us.kg', f'{new_subdomain}.cepu.us.kg')

    with open(html_file, 'w') as file:
        file.write(updated_content)

# Fungsi untuk menyimpan subdomain yang digunakan ke file YAML
def save_subdomain_to_yaml(subdomain, yaml_file):
    with open(yaml_file, 'w') as file:
        yaml.dump({'subdomain': subdomain}, file)

# Fungsi untuk membaca subdomain terakhir dari file YAML
def read_subdomain_from_yaml(yaml_file):
    if os.path.exists(yaml_file):
        with open(yaml_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            return data.get('subdomain', None)
    return None

def main():
    yaml_file = 'subdomain.yml'
    toml_file = 'wrangler.toml'
    html_file = 'index.html'

    # Cek apakah subdomain sudah ada dari YAML (subdomain terakhir)
    last_subdomain = read_subdomain_from_yaml(yaml_file)
    
    # Jika belum ada, buat subdomain baru
    if not last_subdomain:
        last_subdomain = generate_random_subdomain()

    # Ganti subdomain di wrangler.toml dan index.html
    replace_subdomain_in_toml(toml_file, last_subdomain)
    replace_subdomain_in_html(html_file, last_subdomain)

    # Simpan subdomain yang digunakan ke file YAML
    save_subdomain_to_yaml(last_subdomain, yaml_file)

if __name__ == "__main__":
    main()
