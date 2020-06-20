# Announce Web App - something like simple olx 
Flask, sqlite, CSS/HTML, requests, postman

Web Application with multiple subsystems like management, logging , registration.
Allows user to create and post announcements like math private lessons or some items like old books etc
Each user can have multiple(1...*) announcements and can check others and contact them if they are interested in.
They are also  permitted to edit their own profile, own announcements and delete them whenever they want.
Client app made with requests and browser supports templates were created in HTML and CSS. Announces and users are stored in 
sqlite database.

REST-API fulfills Richardson second criteria
- create announce
- delete announce
- read announce
 - update announce (edit)
 
 All functionalities were tested with Postman.

