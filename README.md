# SAME-Insurance
This project involves designing and implementing an insurance management system for a flight insurance company with the details of the database design and business rules. The task was to identify identities, relationships among entities, and create an efficient database system.

## Database Design
After carefully assessing the business constraints, we performed the necessary data normalization steps. Using Oracle Data Modeler, we designed logical and relational models to map out all the entities and their associative relationships. We then generated DDL scripts, added SQL constraints, and populated the MySQL database with meaningful data.

## Web Application
To provide a user-friendly interface for customers, we developed a full-stack web application using various tools and frameworks. The technologies used include:

* Flask: A Python web framework for building the backend of the application.
* jQuery: A JavaScript library for simplifying client-side scripting.
* HTML: The markup language used for structuring web pages.
* CSS: The style sheet language used for designing the appearance of the web pages.
* JavaScript: A programming language used for adding interactivity to web pages.
* Bootstrap: A CSS framework for creating responsive and visually appealing web pages.

The web application allows users to perform the following tasks:

* Register and log in via a secured authentication system.
* Browse and select insurance plans.
* Enter details related to their flights and insurance requirements.
* View a generated invoice based on their selections.

## Security and Testing
To ensure security and prevent SQL injection attacks, we utilized Stored Procedures in the database operations. Additionally, we used Postman to perform thorough testing of the RESTful APIs.

## Admin Panel
We incorporated an admin panel into the web application to provide managers with additional functionalities. The admin panel allows managers to edit the insurance plans and gain insights into the system.
