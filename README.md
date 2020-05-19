# Movies API

## Overview

Movies API provides full information according to movie title fetched from external database and saves it on server.
It also allows to post comments to movies already fetched and sets ranking based on amount of comments.

## Setup

API is dockerized and can be setup on local machine using commands:
* docker-compose build
* docker-compose up

## /movies:

POST:
Request body should contain only movie title
Response includes full movie object, along with all data fetched from external API.


GET:
Fetches list of all movies already present in application database
Movies can be filtered by id, title, year and genre
**/movies/?{id}
**/movies/?{title}
**/movies/?{year}
**/movies/?{genre}

## /comments:

POST:
Request body should contain ID of movie already present in database, and comment text body.

GET:
Fetch list of all comments present in application database.
Comment can be filtered by movie id
**/comments/?{movie_id}

## /top:

GET:
Should return top movies already present in the database
Ranking based on a number of comments added to the movie during specified date range. Required parameters are start_date and end_date
**/top/?{start_date}&{end_date}

