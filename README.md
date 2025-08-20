# Motus - A ride share application #

## Structure ##

The application provides an onboarding page that allows the user to login to the database. The database is made up of the following tables and allows the user to access their own rides, personalised page. The user can add their own rides, delete and edit their experience with the dark mode button in the setting route.

```sql
CREATE TABLE motus_users (
    user_id serial PRIMARY KEY,
    username TEXT UNIQUE,
    hash_pw TEXT,
    email TEXT UNIQUE,
    created_on TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP DEFAULT NOW()
);

CREATE TABLE rides (
    ride_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    ride_description TEXT,
    ride_start TEXT,
    ride_end TEXT,
    FOREIGN KEY(user_id) REFERENCES motus_users(user_id)
);
```

The users table contains all the information required to add a user to the database. The rides table contains all the information required to add a ride to the database. The two tables are linked together by using a foreign key referencing the user_id in the user table.

## Setting up the development environment ##

Create and activate the virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Now you can install the required packages:

```bash
brew install postgresql
pip install psycopg2 bcrypt flask
```

After activating the virtual environment, need to create a database. To create
the database on heroku, you need to follow the steps below:

```bash
brew install heroku/brew/heroku
heroku addons:create heroku-postgresql:hobby-dev
```

## Generating a random secret key ##

To generate a value for `SECRET_KEY` in production, run the following in a
python shell:

```python
import secrets
secrets.token_hex(16)
```

## Technologies Used ##

- PostgreSQL
- Heroku
- Flask
- Python
- HTML
- CSS
- Javascript
- Figma

## Design ##
I used figma to edit all images and creative features, such as the logo, buttons and colour palette for the application.

![Screen Shot 2022-05-07 at 10 35 43 am](https://user-images.githubusercontent.com/99164498/167231743-ec021a16-019d-4893-a01e-24b0cd2a6311.png)

![Screen Shot 2022-05-07 at 10 35 49 am](https://user-images.githubusercontent.com/99164498/167231746-c0491af3-a120-4acb-9fb5-0f40c5de5b1e.png)

![Screen Shot 2022-05-07 at 10 35 55 am](https://user-images.githubusercontent.com/99164498/167231750-f3ec54ed-58e5-44a6-bcaa-fa73e4be7536.png)

![Screen Shot 2022-05-07 at 10 36 02 am](https://user-images.githubusercontent.com/99164498/167231753-eebf69bb-92ba-49e8-8cf9-722f82480d0f.png)

![Screen Shot 2022-05-07 at 11 10 00 am](https://user-images.githubusercontent.com/99164498/167232013-d9385426-bbf2-4146-8644-2622987c6d82.png)


## Unresolved issues ##

I want to add the following features to the application:
- A more personalised user profile. Allowing the user to add an avatar and
  update and change their username.
- The option to edit rides.
- A loading page.
- A GPS tracking system that would allow the user to track their ride in real
  time rather than add the locations later.
- The incorporation of a weather API to allow the user to revisit their ride
  and see the weather for their selected location and date.

## URL for the application ##

- https://motus-0dc97e914926.herokuapp.com
