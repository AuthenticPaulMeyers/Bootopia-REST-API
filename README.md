# Bootopia REST API

> ### Bootopia is a social network for book lovers.

## Idea
- The idea was to build a community of book lovers where they can interact with each other like a social network. Creating a community where users can share their feelings and moods thereby recommend and select books based on their mood for the day.

## Concept
1. Share their favorite books and what they’re currently reading.
2. Discover new books based on mood, interest, or popular trends.
3. Use an AI-powered summarizer to get the key points or chapter summaries while reading.
4. Share posts on the favorites book quotes and and insights.

## Core Features and use cases
### 1. Book Sharing & Discovery
Users can:
- Register and login
- Request password reset through email verification
- Share what they’re reading with personal thoughts or quotes.
- Tag books by genre, mood, or theme.
- Follow friends and influencers to see what they’re reading.
- “Book Feed” similar to a social feed where you see posts from people you follow.

### 2. AI Summarizer Assistant
Key Features:
- Summarize entire books or chapters.
- Extract key quotes, themes, and takeaways.

### 3. Smart Book Discovery Engine
Discover books based on:
- Mood (e.g., “inspirational”, “heartwarming”, “mind-bending”)
- AI-curated lists based on your reading history or interests.

### 4. Reading Journal
Private or public reading diary:
- Track thoughts by chapter.
- Log insights, and quotes.

## Target Users
### 1. The Bookworm Explorer
- Loves discovering new books.
- Wants mood-based suggestions.
- Will use AI summaries to quickly decide what to read.

### 2. The Social Reader
- Enjoys sharing thoughts and engaging in book discussions.
- Active in book clubs and online forums.
- Loves commenting and live read-alongs.
- The Student/Researcher
- Uses AI summaries to study faster.
- Tracks key insights and takes notes.
- Needs citation-ready summaries and quote extractions.

### 3. The Author/Influencer
- Wants to share book reviews or promote books.
- Engages with a fanbase and recommends books.

## User Flow
1. User signs up → Builds a profile with:
    - Favorite genres
    - Current reads
    - Mood preferences

2. Gets a personalized home feed of:
    - Book updates from friends
    - AI-curated book picks from user's mood

3. Selects a book to read:
    - Can read and save quotes
    - Can save book to reading list/bookmarks to read later.
    - Can launch AI summary for the book

4. Users interaction:
    - Follow an unfollow each other
    - Make a post
    - Comment on a post
    - Like and unlike post

5. Get notifications
    - Get notifications on posts, likes and comments
    - Mark notifications as read 
    - Clear notifications


## Tools used to build the API
1. Framework
-The API is a RESTful API built in Python using the [Flask](https://flask.palletsprojects.com/) framework. Flask is python's micro-framework for backend development. I think Flask is the best beginner friendly framework i would recommend every beginner python developer to use as they are getting started into backend development.

2. Database
- The API uses [PostgreSQL](https://www.postgresql.org/) to store the data. PostgreSQL is a relational database which stores data in tables arranged in rows and columns. It is one of the best relational databases out there used by many companies. I have used [SQLAlchemy](https://www.sqlalchemy.org/), an Object Relational Mapper to interact with the database in python files.

3. AI Integration
- I have used the [OpenAI](www.openai.com) models with `gpt-4` to generate book summaries and mood-based recommendations.

4. Documentation
- The documentation is running on [SwaggerUI](https://swagger.io/tools/swagger-ui/) which i found is easy to integrate in flask using the `flask-swagger-ui` library.

## Security
- When it comes to API development, security is the crucial part in this case. 
1. Password Hashing
- User passwords are stored in hashes using `MD5` hashing algorithm.

2. Token management
- Token management is the most important part of user authentication in backend development. I have used `JWT` in this project which i have found is easy to use. Users are given a `JWT Token` after login which will be stored in the users' cache memory in the browser to track login sessions. Tokens are used to track users when they are logged in to allow them to have access to secured endpoints.

3. Rate limiting
- I have applied limit on AI endpoints to limit how many times users can push requests to the server. Rate limiting is very important to control user traffic on most requested resource in the server, in this case AI endpoints and request password reset endpoint. A message will be displayed if users have reached limit for the day.

4. Email verification on password reset
- When a user requests a password reset using the registered email, a password reset link is sent to their email inbox as a way to verify if the user making the request is the actual owner of the account. In this endpoint, users are limited to make limited amounts of requests to reset their password in a day.

## Performance
- The database has been optmized using indexes to allow easy retrieval of data in tables. 

## How to run the API locally
- Make sure you have `python 3.1` or any latest version installed in your machine.
- Install and configure `PostgreSQL` to run the database models.

1. Clone the repository
> Use `git clone <repo URL>`

2. Install the dependencies
- There is a `requirements.txt` file in the project directory which contains all the dependencies used in this project.
- Open the terminal and navigate to the project directory. Then run `python -m venv venv` to create a virtual environment.
- Go inside the `venv` the install all the dependencies at once using `pip freeze > requirements.txt`.
- Run the program using `python run.py` or `flask run --debug`.

- To access the documentation for the routes make sure your local server is running, then go to the local server address where the app is being served, for example: `127.0.0.1:5000/docs` or `localhost:5000/docs`

## What i have learnt in this project
- Eh I had lots of challenges building this API I can't list them all. But all i can say is that i have learnt alot of backend concepts in this project. For example:
    - AI API integration
    - Rate limiting
    - Documentation
    - Email servers
    - And how to work with other python packages. 
- It has been a great experience and am looking forward to what i will build next with the concepts taken from this project.

## Improvements
- This API will continue being developed and improved. There are some uses cases which are going to be added or removed.

1. What to be added
- Admin route
- Email verification when user is registered to avoid garbage emails.
- Caching on frequently accessed routes like feeds and AI summaries.
- Real time chat section for users to interact with each other.
- Integrate AI voice assistant on reads and summaries.

2. What to be removed
- Am not sure yet.

## Final word
- The API is made public to all front-end developers who are looking for public APIs to use in their projects. I would love to see front-end projects that would come out of this repository.
- For those who want to contribute on this project i'd also love to review your pull requests.

> Happy coding!