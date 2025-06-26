import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

# Загрузка данных
df = pd.read_excel('bd_camping.xlsx', sheet_name='camping')

# Загрузка всех GeoJSON-файлов из папки
districts_gdf = gpd.GeoDataFrame()
geojson_folder = 'districts'  

for file in os.listdir(geojson_folder):
    if file.endswith('.geojson'):
        file_path = os.path.join(geojson_folder, file)
        temp_gdf = gpd.read_file(file_path)
        districts_gdf = pd.concat([districts_gdf, temp_gdf], ignore_index=True)

# Проверка загруженных данных
print("Загружено районов:", len(districts_gdf))
print("Пример данных:", districts_gdf.head(2))

# Функция для определения района по координатам
def get_district(lat, lon):
    point = Point(lon, lat)  
    for idx, row in districts_gdf.iterrows():
        if row['geometry'].contains(point):
            return row['name'] 
    return "Не определен"

# Добавление столбца с районом
df['district'] = df.apply(lambda row: get_district(row['lat'], row['lon']), axis=1)

# Сохранение результата
output_file = 'camping_with_districts.xlsx'
df.to_excel(output_file, index=False)

print(f"Данные сохранены в файл: {output_file}")
print("Распределение по районам:")
print(df['district'].value_counts())





