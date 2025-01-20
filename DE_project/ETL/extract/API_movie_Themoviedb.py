import requests
import json
import os

api_key = '9fb9d335431a9f6007701ac905fcd5e5'
url_popular = 'https://api.themoviedb.org/3/movie/popular'
url_movie_details = 'https://api.themoviedb.org/3/movie'
all_movie_data = []
max_retries = 3
num_page = 500

# Specify the output path
output_path = '/opt/airflow/DE_project/data/JSON/movies_data.json'

def get_movie_data():
    for page in range(1, num_page+1):
        for attempt in range(max_retries):
            try:
                params = {
                    'api_key': api_key,
                    'page': page
                }
                response = requests.get(url_popular, params=params)
                response.raise_for_status()
                movie_data = response.json()['results']

                for movie in movie_data:
                    movie_id = movie['id']
                    movie_details_url = f"{url_movie_details}/{movie_id}"

                    # Fetch movie details
                    for attempt_details in range(max_retries):
                        try:
                            details_params = {'api_key': api_key}
                            details_response = requests.get(movie_details_url, params=details_params)
                            details_response.raise_for_status()
                            details = details_response.json()

                            # Extract only the necessary fields
                            filtered_movie = {
                                'id': movie['id'],
                                'title': movie['title'],
                                'release_date': movie['release_date'],
                                'original_language': movie['original_language'],
                                'vote_average': movie['vote_average'],
                                'vote_count': movie['vote_count'],
                                'popularity': movie['popularity'],
                                'runtime': details.get('runtime'),
                                'adult': movie['adult'],
                                'genres': [genre['name'] for genre in details.get('genres', [])],
                                'overview': movie['overview']
                            }

                            # Add the filtered movie data to the list
                            all_movie_data.append(filtered_movie)
                            break
                        except requests.exceptions.RequestException as e:
                            print(f"Failed to fetch details for movie ID {movie_id} (attempt {attempt_details + 1}): {e}")
                    else:
                        print(f"Failed to fetch details for movie ID {movie_id} after {max_retries} attempts.")

                print(f"Fetched data for page {page}")
                break  # Exit the retry loop on success
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed for page {page}: {e}")
        else:
            print(f"Failed to fetch data for page {page} after {max_retries} attempts.")
            break

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Save data to the specified path
    with open(output_path, 'w') as file:
        json.dump(all_movie_data, file, indent=4)

    print(f"Movie data with selected fields has been saved to {output_path}")

if __name__ == '__main__':
    get_movie_data()
