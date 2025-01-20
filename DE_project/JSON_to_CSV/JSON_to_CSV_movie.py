import json
import csv

fields = ['id', 'title', 'release_date', 'original_language', 'vote_average', 'vote_count', 'popularity', 'runtime', 'adult', 'genres', 'overview']

# Load JSON data
with open('/opt/airflow/DE_project/data/JSON/movies_data.json', 'r') as json_file:
    movies = json.load(json_file)

# Convert JSON to CSV
with open('/opt/airflow/DE_project/data/CSV/movie.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()

    # Iterate over movies and write each movie's data to the CSV
    for movie in movies:
        # Flatten nested lists (e.g., genres) into comma-separated strings
        movie['genres'] = ', '.join(movie.get('genres', []))

        # Write each movie as a row in the CSV
        writer.writerow({field: movie.get(field, "") for field in fields})

print("Conversion complete. CSV file saved as 'movies_data.csv'")
