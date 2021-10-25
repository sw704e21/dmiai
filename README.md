# DM i AI
Welcome to the event <a href="https://dmiai.dk/">DM i AI</a> hosted by <a href="https://ambolt.io/">Ambolt ApS</a>.
In this GitHub repository, you will find all the necessary information needed for the event. Please read the entire information before proceeding to the use case, and please make sure to read the full description of all the use cases. You will be granted points for each use case based on how well you score in the respective use case.


<h2>Use cases</h2>
Below you can find the four different use cases for the  DM i AI event, the cases are listed by their difficulity. <br>
Within each use case, you find a description together with a template that can be used to setup an API endpoint. <br> 
The API endpoint will be used for submission and is required. <a href="https://github.com/amboltio/emily-cli">Emily</a> can help with setting up the API, but you should feel free to set them up on your own. The requirements for the API endpoints are specified in the respective use cases. <br> <br>
<a href="https://github.com/amboltio/DM-i-AI/tree/main/wheres-waldo">Case 1: Where's Waldo</a> <br>
<a href="https://github.com/amboltio/DM-i-AI/tree/main/movie-reviews">Case 2: Movie Rating Prediction</a> <br>
<a href="https://github.com/amboltio/DM-i-AI/tree/main/racing-game">Case 3: Racing Track Simulation</a> <br>
<a href="https://github.com/amboltio/DM-i-AI/tree/main/iq-test">Case 4: IQ Test Solver</a> <br> <br>

Clone this GitHub repository to download Emily templates for all four use cases.
```
git clone https://github.com/amboltio/DM-i-AI.git
```
Inside the DM-i-AI folder, you will find the four different use cases. To open a use case with Emily type `emily open <use-case>` e.g. `emily open wheres-waldo` to open the first use case.

<h2>Emily CLI</h2>
The <a href="https://ambolt.io/emily-ai/">Emily CLI</a> is built and maintained by <a href="https://ambolt.io/">Ambolt</a> to help developers and teams implement and run production ready machine learning powered micro services fast and easy. <br>
<a href="https://github.com/amboltio/emily-cli/wiki">Click here</a> for getting started with Emily. Emily can assist you with developing the required API endpoints for the use cases. Together with every use case a predefined and documented template is provided to ensure correct API endpoints for the specific use case. You can find the documentation of the entire framework <a href="https://amboltio.github.io/emily-cli-documentation-client/">here</a>. <br>
The use cases have been built on top of the <a href="https://fastapi.tiangolo.com/">FastAPI</a> framework, and should be used to specify endpoints in every use case.

<h2>Discord Channel</h2>
Come hang out and talk to other competitors of the event on our Discord channel. Discuss the use cases with each other or get in touch with any of the Ambolt staff, to solve eventual issues or questions that may arise during the competition. <a href="https://discord.gg/EPMjWgpJ">Join here!</a> <br>

<h2>Getting started without emily</h2>
You are not required to use Emily for competing in this event, however, we strongly recommend using Emily if you are not an expert in developing APIs and microservices. If you do not choose to use Emily, you should check the individual template and find the requirements for the different API endpoints. These have to be exactly the same for the evaluation service to work. Inside the `dtos` folder you can find information on the request and response models, describing the input and output requirements for your API. 

<h2>Submission</h2>
When you are ready for submission, <a href="https://amboltio.github.io/emily-intro/deploy/">click here</a> for instructions on how to deploy. Then, head over to the <a href="https://amboltio.github.io/DM-i-AI-client/">Submission Form</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!<br>
The number of submissions is specific for each use case, and you can find the maximum number of allowed submissions below: <br> <br>

* Case 1 - Where's Waldo: **1 time** <br>
* Case 2 - Movie Rating Prediction: **Unlimited** <br>
* Case 3 - Racing Track Simulation: **Unlimited** <br>
* Case 4 - IQ Test Solver: **1 time** <br>

Upon completion of the contest, the top 5 highest-ranking teams will be asked to submit their training code and the trained models for validation. The final ranking is announced on 30/11. 
