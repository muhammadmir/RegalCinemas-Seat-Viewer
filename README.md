# RegalCinemas-Seat-Viewer
View the seatings and the seat types for a specific movie at a specific theater for all screening types on a specific date.

Four inputs are required:

Cinema ID
- The id of the specifc cinema

Obtaining Cinema ID
1. Go to https://www.regmovies.com/theatres
2. Click on the name of your cinema
3. From the URL (https://www.regmovies.com/theatres/regal-union-square-screenx-4dx/1320#/buy-tickets-by-cinema?in-cinema=1320&at=2021-12-24&view-mode=list), the 4 digit number is is the Cinema ID (1320)

Movie ID
- The id of the specific movie

Obtaining Movie ID
1. Go to viewing page of the screening types of the specifc movie
2. From the URL (https://www.regmovies.com/movies/spider-man-no-way-home/ho00010969#/buy-tickets-by-film-for-cinemas?at=2021-12-24&for-movie=ho00010969&view-mode=list), the alphanumeric Movie ID is (ho00010969)

Movie Name
- Any name the user give

Date
- The date must be in the format of (YYYY-MM-DD) and should be the current date or one in the future when the movie is also playing

Output
All results are outputted in files. The results are stored in Movies -> (Name of Movie) -> (Screening Format) (Time).txt
The text files contain additional information including a direct link to schedule seats, an ASCII table matching the one seen when choosing seats online, and a legend for the table.
