
import requests
import json
import os

# Сбор данных с OpenStreetMap
def get_osm_camps():
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = """
    [out:json];
    (
      node["tourism"="camp_site"](51.0,103.0,56.0,110.0);
      way["tourism"="camp_site"](51.0,103.0,56.0,110.0);
      node["tourism"="wild_camp"](51.0,103.0,56.0,110.0);
    );
    out center;
    """
    response = requests.post(overpass_url, data=query)
    return response.json()

# Ручные проверенные данные
def get_manual_entries():
    return [
        {
            "name": "Кемпинг 'Байкальские Дюны'",
            "lat": 52.4156,
            "lon": 106.2813,
            "source": "wikimapia"
        },

    ]

# Сохранение данных в JSON
def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Удаление объектов 'Без названия' из файла
def clean_unnamed_camps(filename):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Фильтрация объектов
    cleaned_data = [camp for camp in data if camp['name'] != 'Кемпинг без названия']
    
    # Перезаписываем файл
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print(f"Удалено {len(data) - len(cleaned_data)} объектов без названия")

def main():
    # Автоматический сбор
    print("Получаем данные с OpenStreetMap...")
    osm_data = get_osm_camps()
    
    # Обработка OSM-данных
    camps = []
    for element in osm_data['elements']:
        camps.append({
            'name': element.get('tags', {}).get('name', 'Кемпинг без названия'),
            'lat': element.get('lat', element.get('center', {}).get('lat')),
            'lon': element.get('lon', element.get('center', {}).get('lon')),
            'source': 'OpenStreetMap'
        })
    
    # Добавление ручных данных
    print("Добавляем проверенные точки...")
    camps.extend(get_manual_entries())
    
    # Сохранение
    output_file = 'baikal_camps1.json'
    save_to_file(camps, output_file)
    print(f"Готово! Сохранено {len(camps)} кемпингов в файл '{output_file}'")
    
    # Очистка от объектов без названия
    print("\nОчищаем данные...")
    clean_unnamed_camps(output_file)
    
    # Финальная проверка
    with open(output_file, 'r', encoding='utf-8') as f:
        final_data = json.load(f)
    print(f"Итоговое количество объектов: {len(final_data)}")

if __name__ == '__main__':
    main()