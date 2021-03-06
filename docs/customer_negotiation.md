These are the requirements that have been provided from class.

## Minimum Spec:

* Allow users to create new accounts
* Allow users to 'post' content of interest
* Allow other users to rate, review, and comment on posts
* Search feature (what can be searched is up to your customer)
* Provide administrative users, moderators, and normal users
* Allow for user profiles
* Ensure security - make sure that users cannot edit other people's data through
  security holes, etc.

## Requirements to negotiate with your customer:

* What type of information will be posted; and how will it be posted?
* What type of information comprises user profiles?
* What will show up on the user profile page?
* What powers administrators, moderators, and users will have?
* How will the reviews and comments work?
* How the search will work?
* How will user reputation work?

## Implementation details (database, programming language, platform)

### PLEASE ADD TO THIS SECTION BEFORE THE MEETING WITH THE CUSTOMER

### EDIT AND REMOVE TOPICS AS YOU SEE FIT.

## Possible design and implementation details from the group:

* Use Flask as the development tool for the web app.

* Don't take the user away from the main content on the website. Any links
  should take the user to a new tab or window, but should not take them away
  from the social sharing site.

* Minimalize the amount of pages. Get as much as possible to fit on the main
  sharing page, and try to incorporate overlay windows instead of directing to
  a whole new screen.

* Use a tile based system. The front of the tile will have a preview or 
  thumbnail of the content. Selecting that tile will flip it and reveal more
  information on the other side. Possible it will have links, summaries,
  reviews, and so forth.

* The tiles wil fit into place based on a brick pattern.

* Use some kind of system to help distinguigh categories as quickly as possible.
  Color coded system might be best. Have default presets for categories, but
  allow the users to change these based on their preferences.

* When content is being shared publicly, make sure there is some way for all
  people to have their content shown, not just the most popular. The point of
  content sharing is to see and to share a wide range of material.
