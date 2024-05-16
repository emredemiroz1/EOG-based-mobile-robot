import pandas as pd
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Ana dizin yolunu belirleyin
base_dir_path = r"C:\Users\emred\OneDrive\Masaüstü\Bitirme\Arduino Kodları\PYTHON KODLARI\Supplementary Material\Dataset\Dataset"

# #1'den #9'a kadar olan dizin adlarını listele
dir_list = [f"{base_dir_path}\#{i}" for i in range(1, 10)]

# Tüm verileri birleştirmek için boş bir DataFrame oluşturun
all_data = pd.DataFrame()

# Her dizindeki dosyaları oku ve birleştir
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
        
        # Verileri birleştir
        all_data = pd.concat([all_data, data], ignore_index=True)

# Sütun adlarını belirle
all_data.columns = ['Dikey_Genlik', 'Yatay_Genlik', 'Dikey_Etiket', 'Yatay_Etiket']

# Özellikler ve etiketleri ayır
X = all_data[['Dikey_Genlik', 'Yatay_Genlik']]
y = all_data[['Dikey_Etiket', 'Yatay_Etiket']]

# Verileri eğitim ve test setlerine ayırın
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Verileri ölçeklendirin (normalleştirin)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# KNN modelini oluşturun ve hiperparametre ayarlarını yapmak için GridSearchCV kullanın
param_grid = {
    'n_neighbors': range(1, 31),  # Komşu sayısını 1'den 30'a kadar deneyin
    'weights': ['uniform', 'distance'],  # Ağırlıklandırma seçenekleri
    'metric': ['euclidean', 'manhattan', 'minkowski']  # Mesafe metrikleri
}

knn = KNeighborsRegressor()
grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_train_scaled, y_train)

# En iyi parametreleri kullanarak modeli yeniden eğitin
best_knn = grid_search.best_estimator_
best_knn.fit(X_train_scaled, y_train)

# Test seti üzerinde tahminler yapın
y_pred = best_knn.predict(X_test_scaled)

# Performans metriklerini hesaplayın
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"En iyi parametreler: {grid_search.best_params_}")
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Tahmin ve gerçek değerleri görselleştirme
plt.figure(figsize=(12, 6))

# Birinci hedef değişkeni görselleştirme (Dikey Etiket)
plt.subplot(1, 2, 1)
plt.scatter(y_test.iloc[:, 0], y_pred[:, 0], alpha=0.5)
plt.xlabel('Gerçek Değerler')
plt.ylabel('Tahminler')
plt.title('Dikey Etiket')

# İkinci hedef değişkeni görselleştirme (Yatay Etiket)
plt.subplot(1, 2, 2)
plt.scatter(y_test.iloc[:, 1], y_pred[:, 1], alpha=0.5, color='orange')
plt.xlabel('Gerçek Değerler')
plt.ylabel('Tahminler')
plt.title('Yatay Etiket')

plt.tight_layout()
plt.show()
