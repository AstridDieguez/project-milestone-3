[View in Heroku](https://adieguez1-project-m2.herokuapp.com/)

## Technologies, Frameworks, Libraries and APIs Used
* Visual Studio Code (VSCode)
* Git + Github
* Python
* Pylint
* Python Flask
* Flask Login
* SQLAlchemy
* HTML/CSS
* Heroku
* TMDB API
* Wikipedia API

## How to Launch App Locally
1. Make sure you have git installed on your computer:

   **Linux**  
   `sudo apt-get update`  
   `sudo apt-get install git`

   Verify installation by checking the version:  
   `git --version`

2. Make sure you have python installed on your computer:

   **Linux**  
   `sudo apt-get install python3.8`

   Verify installiation by checking the version:  
   `python3 --version`

3. Clone this repository with `git clone git@github.com:csc4350-sp22/milestone2-adieguez1.git`

4. This repository does not clone the key for TMDB API. You'll have to use your own key, and set the variable in a .env file. 

   [TMDB API Documentation](https://developers.themoviedb.org/3/getting-started/authentication)   

5. You'll want to install any required packages (such as Flask) using *pip install {module-name}*. Try to run `python3 app.py` and an error message should show any module(s) that need to be installed.

   Example: `pip install flask`

You can also view *requirements.txt* to see all the required packages.

6. Once app.py can run with all the required packages, your terminal should show the location of the program. Open the URL on your browser.

   Example: `Running on http://172.24.4.0:8080/`

7. On the browser, use this flask app to search for information about any movies via TMDB API, leave and view comments and ratings, and see a Wikipedia link to more relevant information about a movie. You will need to sign up for an account with a unique username. 

## Questions
1. *How did implementing your project differ from your expectations during project planning?*

   I don't think my expectations for developing the project differed much from the actual implementation. I expected that the project would be using a database to store information about users and comments, and that I would have to implement a login system either via sessions or some other library to keep track of the current user. 

2. *Give a detailed description of 2+ technical issues and how you solved them (your process, what you searched, what resources you used)*

   **a.** One technical issue I had was trying to figure out how to implement the Flask Login library. I did not know how to use the decorators and that I had to implement certain class functions for the user. I solved this by looking at various online resources that showed how to implement the flask login library.

   **b.** Another technical issue I faced was trying to establish a relationship with the User table and the Comments table. It really came down to just not knowing the correct syntax for creating a foreign key, but after looking up documentation on it, I was able to connect the tables.