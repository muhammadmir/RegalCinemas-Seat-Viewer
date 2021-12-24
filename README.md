# RegalCinemas-Seat-Viewer
View all the seatings in an ASCII table for all screening types of a specific movie at a specific Regal Cinemas location.

Three inputs are required:

Movie ID
- The id of the specific movie

Obtaining Movie ID
1. Go to viewing page of the screening types of the specifc movie
2. From the URL (https://www.regmovies.com/movies/spider-man-no-way-home/ho00010969#/buy-tickets-by-film-for-cinemas?at=2021-12-24&for-movie=ho00010969&view-mode=list), the alphanumeric Movie ID is (ho00010969)

Movie Name
- Any name the user gives

Date
- The date must be in the format of (YYYY-MM-DD) and should be the current date or one in the future when the movie is also playing

Output
- All results are outputted in files. The results are stored in Movies -> (Name of Movie) -> (Screening Format) (Time).txt
The text files contain additional information including a direct link to schedule seats, an ASCII table matching the one seen when choosing seats online, and a legend for the table.

Running
- Launch .py file, and then select an option to locate a cinema from zip, city, or state. The cinema data is from Locations.json file. Once selected, enter the Movie ID, Movie Name, and Date. Results will be in the Movies folder.
