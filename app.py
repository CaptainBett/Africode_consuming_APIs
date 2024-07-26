import requests
from flask import Flask, render_template, url_for

app = Flask(__name__)

BASE_URL = 'https://jsonplaceholder.typicode.com/'



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET'])
def get_users():
    response = requests.get(f"{BASE_URL}/users")
    users = response.json()
    users_data = []
    for user in users:
        users_data.append({
            'id': user['id'],
            'name': user['name'],
            'username': user['username'],
            'email': user['email'],
            'city': user['address']['city'],
            'street': user['address']['street'],
            'zipcode': user['address']['zipcode'],
            'phone': user['phone'],
            'website': user['website'],
            'company': user['company']['name']
            })
    return render_template("users.html", users=users_data, title='users')


@app.route('/posts', methods=['GET'])
def get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    posts = response.json()

    # Fetch users to map userId to username
    response_users = requests.get(f"{BASE_URL}/users")
    users = response_users.json()
    
    # Create a dictionary to map userId to username
    user_map = {user['id']: user['username'] for user in users}
    
    posts_data = []
    for post in posts:
        posts_data.append({
           'username': user_map.get(post['userId'], 'Unknown User'),
            'id': post['id'],
            'title': post['title'],
            'body': post['body']
            })
    return render_template('posts.html',posts=posts_data,title='posts')


@app.route('/comments', methods=['GET'])
def get_comments():
    # Fetch comments
    response_comments = requests.get(f"{BASE_URL}/comments")
    comments = response_comments.json()

    # Fetch users and posts to map userId and postId to username and title
    response_users = requests.get(f"{BASE_URL}/users")
    users = response_users.json()
    
    # Create a dictionary to map userId to username
    user_map = {user['id']: user['username'] for user in users}
    
    response_posts = requests.get(f"{BASE_URL}/posts")
    posts = response_posts.json()
    
    # Create a dictionary to map postId to userId and title
    post_map = {post['id']: {'userId': post['userId'], 'title': post['title']} for post in posts}

    # Create comments data with user, post, and comment details
    comments_data = []
    for comment in comments:
        post_info = post_map.get(comment['postId'], {})
        username = user_map.get(post_info.get('userId'), 'Unknown User')
        title = post_info.get('title', 'Unknown Post')
        comments_data.append({
            'id': comment['id'],
            'name': comment['name'],
            'email': comment['email'],
            'body': comment['body'],
            'username': username,
            'title': title,
        })
    
    return render_template('comments.html', comments=comments_data, title='Comments')


@app.route('/albums', methods=['GET'])
def get_albums():
    response = requests.get(f"{BASE_URL}/albums")
    albums = response.json()

    # Fetch users to map albumId to userId

    response_users = requests.get(f"{BASE_URL}/users")
    users = response_users.json()

    # Create a dictionary to map userId to username

    user_map = {user['id']: user['username'] for user in users}

    albums_data = []
    for album in albums:
        albums_data.append({
            'username': user_map.get(album['userId'], 'Unknown User'),
            'id': album['id'],
            'title': album['title'],
            'userId': album['userId']
            })
    return render_template('albums.html',albums=albums_data,title='albums')

@app.route('/photos', methods=['GET'])
def get_photos():
    response = requests.get(f"{BASE_URL}/photos")
    photos = response.json()

    # Fetch users to map albumId to userId
    response_users = requests.get(f"{BASE_URL}/users")
    users = response_users.json()
    
    # Create a dictionary to map userId to username
    user_map = {user['id']: user['username'] for user in users}
    
    photos_data = []
    for photo in photos:
        photos_data.append({
            'username': user_map.get(photo['albumId'], 'Unknown User'),
            'id': photo['id'],
            'title': photo['title'],
            'url': photo['url'],
            'thumbnailUrl': photo['thumbnailUrl']
            })
    return render_template('photos.html',photos=photos_data,title='photos')

@app.route('/todos', methods=['GET'])
def get_todos():
    response_todos = requests.get(f"{BASE_URL}/todos")
    todos = response_todos.json()

    response_users = requests.get(f"{BASE_URL}/users")
    users = response_users.json()

    # Create a dictionary to map userId to username
    user_map = {user['id']: user['username'] for user in users}

    todos_data = []
    for todo in todos:
        todos_data.append({
            'id': todo['id'],
            'username': user_map.get(todo['userId'], 'Unknown User'),
            'title': todo['title'],
            'completed': todo['completed']
        })

    return render_template('todos.html', todos=todos_data, title='todos')



if __name__ == '__main__':
    app.run(debug=True)
 