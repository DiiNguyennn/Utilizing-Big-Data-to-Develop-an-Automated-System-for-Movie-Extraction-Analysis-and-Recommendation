import json
import csv

# Đường dẫn đến file JSON và file CSV
json_file_path = '/opt/airflow/DE_project/data/JSON/movie_ratings.json'
csv_file_name = '/opt/airflow/DE_project/data/CSV/ratings.csv'
# Load dữ liệu từ file JSON
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    movie_data = json.load(json_file)

# Ghi dữ liệu vào file CSV
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['movie_title', 'movie_id', 'user_id', 'author', 'rating', 'timestamp'])

    # Lặp qua dữ liệu JSON và ghi vào file CSV
    for movie in movie_data:
        title = movie.get('title', 'N/A')  # Lấy tiêu đề phim, giá trị mặc định là 'N/A' nếu không có
        movie_id = movie.get('id', 'N/A')  # Lấy ID phim
        if movie.get('ratings'):
            for rating in movie['ratings']:
                userid = rating.get('userID', 'N/A')  # ID người dùng
                author = rating.get('author', 'N/A')  # Tác giả đánh giá
                review_rating = rating.get('rating', 'N/A')  # Điểm đánh giá
                timestamp = rating.get('timestamp', 'N/A')  # Thời gian đánh giá
                # Ghi dòng dữ liệu
                csv_writer.writerow([title, movie_id, userid, author, review_rating, timestamp])
        else:
            # Nếu không có đánh giá, ghi dòng chỉ chứa thông tin phim
            csv_writer.writerow([title, movie_id, '', '', '', ''])

print(f"Dữ liệu đã được ghi thành công vào {csv_file_name}")
