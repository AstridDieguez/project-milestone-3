## Technologies, Frameworks, Libraries and APIs Used
* Visual Studio Code (VSCode)
* Git + Github
* Python
* Pylint
* Python Flask
* Flask Login
* SQLAlchemy
* HTML/CSS
* TMDB API
* Wikipedia API
* React/Javascript

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

6. This project uses the **React** library. Please make sure you have React installed on your local machine.

7. Once app.py can run with all the required packages, your terminal should show the location of the program. Open the URL on your browser.

   Example: `Running on http://172.24.4.0:8080/`

8. On the browser, use this flask app to search for information about any movies via TMDB API, leave and view comments and ratings, edit/delete your ratings, and see a Wikipedia link to more relevant information about a movie. You will need to sign up for an account with a unique username.

## Questions
1. *Describe three techincal problems in detail*

   **a.** The first technical issue I encountered was how to connect my Javascript/React code with my Python Flask application. I did not realize that calling the react code was just a matter of setting up a blueprint in the Flask app to point to the location of the react code, and then calling that route in the react code. 

   **b.** The second technical issue I had was using the Javascript fetch function to get data from the server. I tried to use the function as if it was synchronous and it resulted in errors or unwanted results. I figured out that I had to access the data retrieved inside the fetch function since, the data would not be immediately available, and thus could not be set to a variable in a higher scope.

   **c.** The third technical issue of this project was using state variables. I had an issue where I would try to get the value of a state variable in a render, but the result would be inconsistent or null. I looked online and saw that state variables' values are not consistent throughout different renders. If I wanted a variable for this purpose, I had to use a "useRef" variable.

2. *Describe the hardest part and most valuable learning portion of the overall project*

   The hardest part of this project was learning React without any prior knowledge about it. It took me a while to get used to how the React library worked with HTML and Javascript to create a webpage using state variables. Also loading and fetching data from the server was challenging to do using the fetch function. I did not realize that it was asynchronous, and that data had to be handled within the function. I think that the most valuable learning portion of this project was learning React because of how useful it is in creating web apps.