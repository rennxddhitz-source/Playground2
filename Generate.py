import os
import requests
import re

# 1. Ambil data dari environment GitHub Actions
issue_body = os.environ.get('ISSUE_BODY', '')
api_key = os.environ.get('OPENROUTER_API_KEY')

if not issue_body:
    print("Tidak ada prompt di Issue.")
    exit(0)

# 2. Siapkan instruksi untuk AI
system_prompt = """Kamu adalah developer game HTML5 profesional. 
Tulis kode game lengkap berdasarkan permintaan user. 
ATURAN WAJIB:
1. Tulis semua kode dalam SATU file HTML (gabungkan HTML, CSS, dan JS).
2. Gunakan HTML5 Canvas. Jangan gunakan aset eksternal, gunakan bentuk/emoji.
3. Berikan HANYA kode HTML-nya saja (mulai <!DOCTYPE html> sampai </html>). Jangan ada penjelasan teks apapun."""

# 3. Tembak API OpenRouter
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "qwen/qwen3-coder:free", # Model gratis yang bagus untuk coding
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": issue_body}
        ]
    }
)

if response.status_code == 200:
    data = response.json()
    game_code = data['choices'][0]['message']['content']
    
    # Bersihkan format markdown (jika AI mengirim ```html)
    game_code = re.sub(r'```html', '', game_code)
    game_code = re.sub(r'```', '', game_code).strip()
    
    # 4. Simpan sebagai index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(game_code)
    print("Game berhasil dibuat dan disimpan!")
else:
    print(f"Gagal memanggil AI: {response.text}")
    exit(1)
