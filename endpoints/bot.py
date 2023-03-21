import os
import random
import requests
import json

from datetime import datetime, timedelta

from dotenv import load_dotenv
from faker import Faker

load_dotenv()

fake = Faker()


class Bot:
    sign_up_api_link = 'http://127.0.0.1:8000/api/users'
    login_link = 'http://127.0.0.1:8000/api/login'
    users_count_link = 'http://127.0.0.1:8000/api/users/count'
    post_link = 'http://127.0.0.1:8000/api/posts'
    posts_count_link = 'http://127.0.0.1:8000/api/posts/count-by-user'
    likes_link = 'http://127.0.0.1:8000/api/likes/'
    users: list = []
    number_of_users = int(os.getenv('NUMBER_OF_USERS'))
    max_posts_per_user = int(os.getenv('MAX_POSTS_PER_USER'))
    max_likes_per_user = int(os.getenv('MAX_LIKES_PER_USER'))
    super_user_credentials: dict = {}

    def super_user_login(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.super_user_credentials = {
            "username": os.getenv('FIRST_SUPERUSER_EMAIL'),
            "password": os.getenv('FIRST_SUPERUSER_PASSWORD')
        }
        response = requests.request("POST", self.login_link, headers=headers,
                                    data=self.super_user_credentials)
        self.super_user_credentials['headers'] = {
            'Authorization': f"Bearer {json.loads(response.content)['access_token']}",
            'Content-Type': 'application/json'}

        print('Superuser authenticated')
        self.create_users()

    def create_users(self):
        number_of_users_in_db = self.get_number_of_users()
        while number_of_users_in_db < self.number_of_users:
            payload = {
                "email": fake.email(),
                "password": fake.password(),
            }
            headers = {
                'Content-Type': 'application/json',
            }
            response = requests.request("POST", self.sign_up_api_link, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                self.users.append(payload)
            number_of_users_in_db = self.get_number_of_users()

        print('Users are created')

        self.login_users()

    def login_users(self):

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        for user in self.users:
            user['username'] = user.pop('email')
            response = requests.request("POST", self.login_link, headers=headers, data=user)

            user['headers'] = {'Authorization': f"Bearer {json.loads(response.content)['access_token']}",
                               'Content-Type': 'application/json'}

        self.create_post()

        print('Users are loggen in')

    def create_post(self):
        for user in self.users:
            max_posts = random.randint(1, self.max_posts_per_user)
            while self.number_of_posts_per_user(user) != max_posts:
                post_data = {
                    "title": fake.sentence(nb_words=6, variable_nb_words=True),
                    "content": fake.paragraph(nb_sentences=random.randint(5, 10)),
                    "created_at": self.get_random_date(from_year=2023, to_year=2024, date=True)
                }
                requests.request("POST", self.post_link, headers=user['headers'],
                                 data=json.dumps(post_data, indent=4, sort_keys=True, default=str))

        self.like_post()

        print('Posts are created')

    def like_post(self):
        posts = self.get_posts()
        for user in self.users:
            max_likes = random.randint(1, self.max_likes_per_user)
            liked_posts = random.sample(posts, max_likes)
            for liked_post in liked_posts:
                like_data = {"post_id": liked_post['id'],
                             "created_at": self.get_random_date(from_year=2024, to_year=2025,
                                                                date=True)}
                requests.request("PATCH", self.likes_link, headers=user['headers'],
                                 data=json.dumps(like_data, indent=4,
                                                 sort_keys=True, default=str))

        print('Posts are liked')

    def get_number_of_users(self):
        response = requests.request("GET", self.users_count_link, headers=self.super_user_credentials['headers'])
        users_count = (json.loads(response.content))
        return users_count

    def get_posts(self):
        response = requests.request("GET", self.post_link, headers=self.super_user_credentials['headers'])
        posts = (json.loads(response.content))
        return posts

    def number_of_posts_per_user(self, user):
        response = requests.request("GET", self.posts_count_link, headers=user['headers'])
        count = (json.loads(response.content))
        return count

    @staticmethod
    def get_random_date(from_year, to_year, date):

        # Define the start and end datetime values for the random range
        start_date = datetime(from_year, 3, 25)
        end_date = datetime(to_year, 12, 31)

        # Calculate the total number of seconds in the range
        total_seconds = (end_date - start_date).total_seconds()

        # Generate a random number of seconds within the range
        random_seconds = random.randrange(int(total_seconds))

        # Create a datetime value by adding the random number of seconds to the start date
        random_datetime = start_date + timedelta(seconds=random_seconds)
        if date:
            return random_datetime.date()
        # Print the random datetime value
        return random_datetime


bot = Bot()
bot.super_user_login()
