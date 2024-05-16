import pandas as pd
import matplotlib.pyplot as plt
import os

# Ana dizin yolunu belirleyin
base_dir_path = r"C:\Users\emred\OneDrive\Masaüstü\Bitirme\Arduino Kodları\PYTHON KODLARI\Supplementary Material\Dataset\Dataset"

# #1'den #9'a kadar olan dizin adlarını listele
dir_list = [f"{base_dir_path}\#{i}" for i in range(1, 10)]

# Her dizindeki dosyalar için grafik oluştur ve kaydet
for dir_path in dir_list:
    if not os.path.exists(dir_path):
        print(f"Dizin bulunamadı: {dir_path}")
        continue
    
    # Dizin içindeki tüm dosyaları listeleyin
    file_list = [f for f in os.listdir(dir_path) if f.endswith('.txt')]
    
    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)
        
        # Veriyi oku
        data = pd.read_csv(file_path, delim_whitespace=True, header=None)
        
        # İlk iki sütunu seçin (veriler)
        x = data[0]
        y = data[1]
        
        # Grafik ayarları
        plt.figure(figsize=(12, 8))
        
        # Birinci sütunu göster
        plt.subplot(2, 1, 1)  # 2 satır, 1 sütun, 1. grafik
        plt.plot(x, label='Birinci Sütun')
        plt.xlabel('Index')
        plt.ylabel('Değer')
        plt.title(f'{file_name} - Birinci Sütun Grafiği')
        plt.legend()
        plt.grid(True)
        
        # İkinci sütunu göster
        plt.subplot(2, 1, 2)  # 2 satır, 1 sütun, 2. grafik
        plt.plot(y, label='İkinci Sütun', color='orange')
        plt.xlabel('Index')
        plt.ylabel('Değer')
        plt.title(f'{file_name} - İkinci Sütun Grafiği')
        plt.legend()
        plt.grid(True)
        
        # PNG dosyası olarak kaydetme
        output_file_path = os.path.join(dir_path, f'{os.path.splitext(file_name)[0]}.png')
        plt.tight_layout()
        plt.savefig(output_file_path)
        plt.close()
