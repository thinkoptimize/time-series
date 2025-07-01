import os
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Klasör yolunu belirtin
data_folder = 'data_USD'

# Sonuçları saklamak için bir liste oluşturuyoruz
results = []

# data_USD klasöründeki tüm Excel dosyalarını alalım
files = [f for f in os.listdir(data_folder) if f.endswith('.xlsx')]

# Tüm dosyalar için işlemi gerçekleştirelim
for file in files:
    file_path = os.path.join(data_folder, file)

    # Veriyi yükleyelim
    data = pd.read_excel(file_path)

    # Prophet için DataFrame hazırlığı
    df = pd.DataFrame()
    df["USD_Close"] = data["USD_Close"]
    df.set_index(data["Date"], inplace=True)

    # Prophet formatı için veri dönüşümü
    df_prophet = df[['USD_Close']].reset_index()
    df_prophet.columns = ['ds', 'y']
    df_prophet['y'] = np.log(df_prophet['y'])  # Log dönüşüm

    # Son 25 günü test verisi olarak ayıralım
    train = df_prophet[:-25]
    test = df_prophet[-25:]

    # Prophet modelini oluşturuyoruz
    model = Prophet(
        growth='linear',
        changepoint_prior_scale=0.5,
        n_changepoints=100,
        yearly_seasonality=True,
        weekly_seasonality=True,
        interval_width=0.95,
        seasonality_prior_scale=10.0
    )

    # Modeli eğitim verisiyle eğitelim
    model.fit(train)

    # Test tarih aralığını belirleyelim
    test_end = test['ds'].max()
    train_end = train['ds'].max()
    business_days_needed = pd.bdate_range(start=train_end, end=test_end).size

    # Prophet için gelecekteki tarihleri oluşturalım
    future = model.make_future_dataframe(periods=business_days_needed, freq='B')

    # Tahminleri alalım
    forecast = model.predict(future)

    # Sadece gerekli sütunları alalım
    predicted = forecast[['ds', 'yhat']]

    # Gerçek test verisiyle tahminleri karşılaştıralım
    compare = pd.merge(test, predicted, on='ds', how='inner')
    compare['y'] = np.exp(compare['y'])  # Gerçek değerler
    compare['yhat'] = np.exp(compare['yhat'])  # Tahmin edilen değerler

    # Hata metriklerini hesaplayalım
    mae = mean_absolute_error(compare['y'], compare['yhat'])
    rmse = mean_squared_error(compare['y'], compare['yhat'], squared=False)

    # Sonuçları saklayalım
    results.append({
        'File': file,
        'MAE': mae,
        'RMSE': rmse,
    })

    # Gerçek ve tahmin edilen verileri ayrı kolonlar olarak yazalım
    compare_result_path = os.path.join(data_folder, f"compare_{file}")
    compare.to_excel(compare_result_path, index=False)  # Her dosyaya karşılaştırma dosyası yazılıyor

    print(f'{file} için MAE ve RMSE hesaplandı: MAE={mae:.4f}, RMSE={rmse:.4f}')

# Sonuçları bir DataFrame olarak oluşturuyoruz
results_df = pd.DataFrame(results)

# Raporu Excel dosyasına kaydediyoruz
results_df.to_excel('prophet_comparison_report_all_files.xlsx', index=False)

# Sonuçları yazdıralım
print("Tüm dosyalar için sonuçlar kaydedildi.")
print(results_df)
