import os
import pandas as pd

# Klasör yolunu belirtin
data_folder = 'data'

# USD_TL_data dosyasını yükleyelim
usd_tl_path = os.path.join(data_folder, 'USDTRY=X_data.xlsx')
usd_tl_df = pd.read_excel(usd_tl_path, index_col=0, parse_dates=True)

# 'data' klasöründeki diğer Excel dosyalarını alalım
files = [f for f in os.listdir(data_folder) if f.endswith('.xlsx') and f != 'USD_TL_data.xlsx']

# Her dosyayı yükleyip USD_TL_data ile birleştirelim
for file in files:
    file_path = os.path.join(data_folder, file)

    # Hisse verisini yükleyelim
    df = pd.read_excel(file_path, index_col=0, parse_dates=True)

    # Sadece her iki veri setinde de bulunan ortak tarihleri alalım
    merged_df = df.join(usd_tl_df[['Close']], how='inner', rsuffix='_USD')

    # USD'ye dönüştürülmüş kapanış fiyatını hesaplayalım
    merged_df['USD_Close'] = merged_df['Close'] / merged_df['Close_USD']

    # Yeni veriyi kaydedelim
    output_path = os.path.join(data_folder, f"merged_{file}")
    merged_df.to_excel(output_path)
    print(f"{file} dosyası USD verisiyle birleştirildi ve kaydedildi: {output_path}")
