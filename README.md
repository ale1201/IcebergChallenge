# IcebergChallenge

## Part 1: Web Scrapping

The first part of this challenge is located in the repo, in 'Part1/main.py'. If you run this file, it is going to scrapping the information of all the Hotels in Bogota for the web page of tripadvisor. With this scrapping, a csv file is going to be created under the name 'data.csv', with the information of all the hotels; each row of the csv file has the following structure:

 *Name of the hotel, ID of the hotel, The url of the hotel page in tripadvisor, Address of the hotel, Phone of the hotel, Coded link of the webpage of the hotel, Has the hotel an email?, Calification (/50), Ranking of the hotel, Calification for different aspects of the hotel, Time stamp when the data was scraped*
 
 When you run the script, the name of the hotel is going to be printed in order to inform the user which hotel number the program is scrapping. It takes some time to finish the program.
 
 ## Part 2: Infrastructure
 
 The second part of this challenge is located in the repo, in 'Part2/'. Make sure you have Django installed in your computer. If not, you can install it using
 $ python -m pip install Django

In this part, you should go to the specified folder and run the **manage.py** file, you can run it using the command:

$ py manage.py runserver

After running the server, you can go to the url *http://localhost:8000/hotels/{city}*, where {city} can be either 'medellin' or 'bogota' (for example: http://localhost:8000/hotels/medellin). It is going to take some time before you can see the json




