# Test project for STARNAVI

#### Project made by Elbek Bakiev for STARNAVI for knowledge and skills check purposes

### Start and check project

1. Make sure to have all required data in .env file in the main project directory.


2. Create virtual environment:

```bash
python -m venv /path/to/new/virtual/environment
```

3. Activate virtual environment:

```bash
source /path/to/new/virtual/environment/bin/activate
```

4. Install all requirements:

```bash
pip install -r requirements.txt
```

4. Create database and initial data:

```bash
alembic upgrade head
```

5. You can run the project choosing one of two following commands:

```bash
uvicorn main:app --reload
```

```bash
python main.py
```

6. Enjoy using `http://127.0.0.1:8000` link to test API in Swagger

### Bot

`bot.py` file located in `endpoints/bot.py`. There are two ways to use this bot:

Simply run command:

```bash
python endpoints/bot.py
```

Or follow the steps to run bot manually:

1. Comment following lines in `bot.py` file

```python
41 self.create_users()
58 self.login_users()
72 self.create_post()
85 self.like_post()
```

2. Call python console:

```bash
python
```

3. Import `class Bot` from `bot.py` file:

```pycon
from endpoints.bot import Bot
```

4. Create class object `Bot()` in python console:

```pycon
bot = Bot()
```

5. Login with superuser to know how many users are in database:

```pycon
bot.super_user_login()
```

6. Create users:

```pycon
bot.create_users()
```

7. Login users:

```pycon
bot.login_users()
```

8. Create posts by each user:

```pycon
bot.create_post()
```

9. Like random posts:

```pycon
bot.like_post()
```