# Motus_project
## A ride share application 
- Add `.DS_store` to the `.gitignore` file
- add a short description to the README file
### motus is a ride share application
The application provides a onboarding page that allows the  user to login to the database. The database is made up of the follwing tables and allows the user to access their own rides, personalised page.The user can add their own rides, delete and edit their experience with the darkmode button in the setting route. 

 ``` CREATE TABLE motus_users (
	user_id serial PRIMARY KEY,
	username TEXT UNIQUE,
	hash_pw TEXT,
	email TEXT UNIQUE,
	created_on TIMESTAMP DEFAULT NOW(),
 last_login TIMESTAMP 
);

CREATE TABLE rides (
 ride_id SERIAL PRIMARY KEY,
	user_id INTEGER,
 ride_description TEXT,
 ride_start TEXT,
	ride_end TEXT,
	FOREIGN KEY(user_id) 
		REFERENCES motus_users(user_id)
);
```
The users table contains all the information required to add a user to the database.The rides table contains all the information required to add a ride to the database. the two tables are linked together by using a foreign key refrencing the user_id in the user table. 

# Setting up the the vertual enviroment

- python -m venv venv
--creates the venv(virtual enviroment) directory
- source venv/bin/activate
--This should add (venv)to your terminal prompt.

after activating the virtual enviroment, need to create a database. 

To create the database you need to follow the steps below:
- pip install psql
- pip install bcrypt
- pip install flask
- brew install heroku/brew/heroku
- heroku addons:create heroku-postgresql:hobby-dev

to see the whole heroku cheat sheet, click the url bellow:

https://gist.git.generalassemb.ly/katie/2b04e662ffc32713aad1b07747aceed9
#### Generating a random secret key with python
>>> import secrets
>>> secrets.token_hex(16)


# Technologies Used 

- PSQL 
- API
- HEROKU 
- Flask 
- Python
- HTML 
- CSS
- Javascript
- FIGMA 

# DESIGN 
 I used figma to edit all images and creative features, such as the logo, buttons and colour palette for the application. 
 
 ![Screen Shot 2022-05-07 at 10 35 43 am](https://user-images.githubusercontent.com/99164498/167231743-ec021a16-019d-4893-a01e-24b0cd2a6311.png)
![Screen Shot 2022-05-07 at 10 35 49 am](https://user-images.githubusercontent.com/99164498/167231746-c0491af3-a120-4acb-9fb5-0f40c5de5b1e.png)

![Screen Shot 2022-05-07 at 10 35 55 am](https://user-images.githubusercontent.com/99164498/167231750-f3ec54ed-58e5-44a6-bcaa-fa73e4be7536.png)
![Screen Shot 2022-05-07 at 10 36 02 am](https://user-images.githubusercontent.com/99164498/167231753-eebf69bb-92ba-49e8-8cf9-722f82480d0f.png)



https://user-images.githubusercontent.com/99164498/167231810-33a7af31-1f16-4df5-b42e-9268587b1edc.mov


- https://www.figma.com/file/jI6Knt0x8QCmzcPMcGCtZ9/UXDesign_StudentTemplate?node-id=1%3A6219
# Unresolved issues 
i wanted the to add the following features to the application.

- a more personalised user profile. allowing the user to add a avatar and update and chage their username. 

- the option to edit rides. 

- a loading page 

- a gsp trackering sytem that would allow the user to to track their ride in real tie rather than add the track location later. 

- the incorperation of a weather api to allow the user to revisit their ride and see the weather for their selected location and date. 

# URL for the application 
- https://mysterious-plains-73351.herokuapp.com/show_rides
