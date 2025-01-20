import requests
import json
import time
import os

# Your TMDb API Key
api_key = '9fb9d335431a9f6007701ac905fcd5e5'
base_url = 'https://api.themoviedb.org/3/movie/popular'
num_pages = 500

# Specify the output path
output_path = '/opt/airflow/DE_project/data/JSON/movie_ratings.json'

def get_movie_reviews(movie_id):
    reviews = []
    page = 1
    while True:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={api_key}&page={page}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            reviews.extend(results)
            if not results:
                break

            print(f'Fetched reviews for movie ID {movie_id}, page {page}, number of reviews: {len(results)}')
            page += 1
        elif response.status_code in {429, 500, 503}:
            print(f'Rate limit hit or server error for reviews (ID {movie_id}). Retrying in 5 seconds...')
            time.sleep(5)
        else:
            print(f'Failed to retrieve reviews for movie ID {movie_id}: {response.status_code}')
            break
    return reviews

# Main function to fetch movie ratings
def get_rating_data():
    all_movie_ratings = []
    for page in range(1, num_pages+1):
        url = f'{base_url}?api_key={api_key}&page={page}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
            print(f'Fetched page {page}, number of movies: {len(movies)}')

            for movie in movies:
                movie_id = movie['id']
                title = movie['title']

                # Fetch reviews with retry on failure
                retries = 3
                all_reviews = []
                while retries > 0:
                    try:
                        all_reviews = get_movie_reviews(movie_id)
                        break
                    except Exception as e:
                        print(f'Error fetching reviews for movie {movie_id}: {e}')
                        retries -= 1
                        if retries > 0:
                            print(f'Retrying in 5 seconds... ({retries} attempts left)')
                            time.sleep(5)

                # Collect ratings with userID and timestamp
                user_ratings = [
                    {
                        'author': review['author'],
                        'userID': review['author_details'].get('username'),
                        'rating': review['author_details'].get('rating'),
                        'content': review['content'],
                        'timestamp': review.get('created_at')
                    }
                    for review in all_reviews if review['author_details'].get('rating') is not None
                ]

                all_movie_ratings.append({
                    'title': title,
                    'id': movie_id,
                    'ratings': user_ratings
                })

            # Ensure the output directory exists
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            # Save progress after each page to prevent data loss
            with open(output_path, 'w') as f:
                json.dump(all_movie_ratings, f, indent=4)

            time.sleep(1)  # Add delay to respect rate limits

        elif response.status_code in {429, 500, 503}:
            print(f'Rate limit hit or server error on page {page}. Retrying in 10 seconds...')
            time.sleep(10)  # Longer wait on error
        else:
            print(f'Failed to retrieve data from page {page}: {response.status_code}')
            break
    print(f'Total movies processed: {len(all_movie_ratings)}')

if __name__ == '__main__':
    get_rating_data()
