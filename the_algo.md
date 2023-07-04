# Planning the Spotify Scoring Algorithm

Now that I've finished the data scraping, cleaning, and analyzing, it's time to create
the algorithm I'll use to score my taste in music.

But before I start typing away, I have to prepare.

So I'm using this markdown file and my good ole whiteboard at home to do the math and 
figure out what calculations I'll use in the algorithm.

This file is mainly a brain dump for my thoughts as I plan, but since I'm doing this
project for fun, why not let you into my mind to see my thought process. Anyway, here's
what I'm focusing on first:

1. Figuring out what calculations/math to do
2. Figuring out how to structure the code
3. Figuring out whether to put the data into the algo

Honestly, as I go along, I'll probably add to the list above. But for now, this is where I'm at.

## Calculations/Math to do

For scoring purposes, I'm creating multipliers to favor and give weight to certain metrics. For 
example, an artist's popularity will matter more for a song when the artists is Artist_1 vs
Artists_5.

Here are a few ideas I have:

1. Boost artists when they have a lower Artists number (aka Artist 1 is better than Artist 5)
2. Lower weight when an artist is featured as opposed to starring no the track
3. 2x multiplier when a song is in the artists top 10 tracks
4. Boost when an artist has a high ratio of "% of top track in playlist" to "total number of artist's songs in playlist"
5. Deboost (aka 0.6x multiplier) if an artists is **featured** in song

## How to structure the code

The only way to do this is to create multiple functions for some of thee multipliers then create
a `main()` function to put everything together.

Also I might make a `Class` or two if need be.

But overall, since this is my first long-form programming project, I'm trying to keep the code
as clean as possible and as easy to read as possible.

## How to enter data into the algorithm

This is the most overlooked yet most essential part of my algorithm. Because the way I decide to
put the data into the algorithm dictates how I actually write the code and what variable names
I choose.

The easiest choice would be to directly include the csv files I created and cleaned by putting
reading them at the top of the code.

But there's a problem with this...

If I choose this method, the algorithm won't be usable for other accounts or playlists. That's
why I intend to create `classes` that I'll import into the main algorithm file. These classes
would read csv or json files and allow my algorithm to use them.

This method will make my code most flexible (and usable) for data that's not mmine.