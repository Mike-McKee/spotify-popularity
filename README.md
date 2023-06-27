# How is my music taste?
Do I listen to trendy arists and songs?

It's easy to guess "yes" or "no" on my own, but unless I actually look at the
data, I'll never know.

That's why I'm doing this project.

I'm accessing Spotify's API and pulling data to analyze my recently played
songs and which artists show up in my playslists the most.

Here's the plan...

## The Tools

For this project, I'm working with the following:

- Python
- Spotify API
- Pandas lib
- Requests lib

And as I do more, I'll figure out what else I need. But for the most part,
Python and working with the API matters most.

## What I'll collect

Since this is my first time working with APIs, I don't want to overwhelm
myself. So I'll be realistic and request only the data I need.

Looking over the Spotify API Documentation, I've got a good idea what I can
request and what I can do with it.

So, I'll collect the following data from my Spotify account:

- Total number of songs in my ***Canciones en Español*** playlist
- Artist popularity for all in my playlist
- The popularity of every track in my playlist

This is what I'm expecting to collect as of now.

But down the line, I may add or remove some items.

## What I'll do with my data

This is what you're here for. You don't care about me or my taste in music. You
probably only care about three things:

1. What my code looks like
2. What my data looks like
3. What I do with my data

Using my data, I'll create a scoring system that ranks the popularity of the songs 
and artists in my ***Canciones en Español*** playlist. And I'll figure out whether I
listen to trendy artists/songs or not.