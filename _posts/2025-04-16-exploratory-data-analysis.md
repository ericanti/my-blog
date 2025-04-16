---
layout: post
title:  "Breaking Down the Secrets of Top Billboard Hits"
date: 2025-04-15
description: "An in-depth analysis of the factors contributing to the success of Billboard's top hits."
image: "/assets/img/guitar.jpg"
---

## Let's Get Caught Up

If you've been following along, you know that we've been diving into the world of music data analysis. In this post, we're going to take a closer look at the factors that contribute to the success of Billboard's top hits. We'll be using a dataset that includes various features of songs, such as tempo, key, and energy level, to see how they correlate with chart performance. We'll also explore the distribution of these features and how they vary across different genres. By the end of this post, you'll have a better understanding of what makes a song a hit and how you can explore these trends further.

In our previous blog post (check it out <a href="https://ericanti.github.io/my-blog/blog/api-usage/" target="_blank">here</a>), we discussed how to use API calls to get the acoustic features of Billboard Hot 100 hits from 1969 as well as 2019, we also briefly touched on some exploratory data analysis (EDA) techniques. In this post, we'll dive deeper into EDA and how it can help us understand the data better.

## How Has Music Evolved Over Time?

Previously, we looked at how music has evolved over the years. We found that older songs tend to be happier with more male artists, while newer songs have a more diverse range of artists and are generally sadder. Let's take a closer look at the shift in genres over the years. We'll use a bar plot to visualize the distribution of genres in our dataset. This will help us understand how the popularity of different genres has changed over time.

<figure> <img src="{{site.url}}/{{site.baseurl}}/assets/img/genre_distribution.png" alt=""> <figcaption>Figure 1. - Genres</figcaption> </figure>

What we see is that genres like jazz and classical have become less popular over the years, while genres like pop and hip-hop have seen a significant increase in popularity. This shift in genres is likely due to changes in cultural trends and the rise of new artists who are pushing the boundaries of traditional music styles.

Going back to happiness, we can also take a look at the top songs and their number of weeks on the Billboard Hot 100 chart. This is color coded by happiness. 

<figure> <img src="{{site.url}}/{{site.baseurl}}/assets/img/peak_position_vs_weeks_on_chart.png" alt=""> <figcaption>Figure 2. - Happiness</figcaption> </figure>

Looking at the visualization, we can see that in 2019 the majority of songs are sadder, especially those who peaked higher on the chart and stayed longer. This is a stark contrast to 1969, where the majority of songs were happier and had a shorter stay on the chart. This could be due to the fact that in 2019, the music industry is more competitive, and artists are trying to create songs that resonate with listeners on a deeper level. An interesting observation is that the number 1 songs in 1969 were majority sad, which could lead to the conclusion that people like music that resonates with them, even if it is sad. This is a common theme in music, where artists use their own experiences to create songs that connect with listeners on an emotional level.

## Exploring Deeper into the Data

