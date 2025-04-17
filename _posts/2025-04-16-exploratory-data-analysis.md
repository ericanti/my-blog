---
layout: post
title:  "Breaking Down the Secrets of Top Billboard Hits"
date: 2025-04-15
description: "An in-depth analysis of the factors contributing to the success of Billboard's top hits."
image: "/assets/img/guitar.jpg"
---

Welcome back! If you’ve been following along, you know we’ve been digging into the data behind Billboard’s biggest hits. Today, we’ll break down what makes a song chart-topping material, how musical trends have shifted, and how you can interactively explore these changes yourself.

---

## What You’ll Find in This Post

- A quick recap of our data sources and previous findings
- Visual breakdowns of genre and mood shifts from 1969 to 2019
- A hands-on walkthrough of our interactive Streamlit app
- Tips on how to explore the data for your own insights
- Live links to resources and further reading

---

## Recap: Setting the Stage

In our [last post](https://ericanti.github.io/my-blog/blog/api-usage/), we covered how to fetch acoustic features of Billboard Hot 100 hits from both 1969 and 2019 using API calls. We also introduced some basic exploratory data analysis (EDA) techniques. This time, we’re going deeper—looking at how features like tempo, key, and energy relate to chart performance, and how these features differ across genres and decades.

---

## How Has Music Changed Over Time?

### Key Takeaways

- Older hits (1969) tended to be happier and featured more male artists.
- Newer hits (2019) show greater artist diversity and lean sadder in mood.

### Genre Evolution

Let’s visualize how genre popularity has shifted:

<figure> <img src="{{site.url}}/{{site.baseurl}}/assets/img/genre_distribution.png" alt=""> <figcaption>Figure 1. Genre distribution over time</figcaption> </figure>

**What’s changed?**
- Jazz and classical genres have faded from the charts.
- Pop and hip-hop have surged, reflecting cultural shifts and new artist influences.

### Mood on the Charts

Now, let’s see how mood and chart success intersect:

<figure> <img src="{{site.url}}/{{site.baseurl}}/assets/img/peak_position_vs_weeks_on_chart.png" alt=""> <figcaption>Figure 2. Mood (happiness) vs. chart performance</figcaption> </figure>

**Observations:**
- In 2019, top-charting songs tend to be sadder, especially those with longer chart runs.
- In 1969, most hits were happier, but interestingly, the #1 songs were often sad.
- This pattern suggests that emotional resonance, not just cheerfulness, drives a song’s staying power.

---

## Try It Yourself: Interactive Data App

We built a [Streamlit app](https://ericanti-post3-streamlit-main-bzlgmr.streamlit.app/) to let you explore these trends hands-on.

### Getting Started

When you open the app, you’ll see a sidebar with filters:

- **Year Selector:** Focus on 1969, 2019, or both.
- **Genre Filter:** Zero in on specific genres.
- **Weeks on Chart:** Filter for songs with real staying power.

There’s also a handy “How To Use” section in the sidebar for quick guidance.

---

## 📊 Overview Tab

**What you’ll see:**
- **Total Songs Analyzed** and **Average Weeks on Chart** for your selected filters.
- **Genre Proportions by Year:** Instantly compare how genres stack up in each era.

---

## 😊 Mood Analysis Tab

**Choose your view:**
- **Year Comparison:** See what fraction of hits were “happy” in each year.
- **Genre Breakdown:** Drill down to see which genres are happiest (or saddest) by year.

---

## 👫 Gender Trends Tab

**Explore:**
- **Gender Proportions by Year:** How has artist gender representation changed?
- **Weeks on Chart by Gender:** Who’s staying on the charts longer?

---

## 🎵 Custom Analysis Tab

**Get creative:**
- Pick any two features (like “peak position” vs. “weeks on chart”) for the axes.
- Color points by mood, gender, or year.
- Optionally split the plot by year for side-by-side comparison.

---

## How to Get the Most Out of the App

1. **Adjust Filters:** Narrow down to specific years, genres, or chart longevity to spot patterns.
2. **Switch Tabs:** Each tab offers a different lens on the data—try them all!
3. **Customize Visuals:** Use the “Custom Analysis” tab to test your own hypotheses.

---

## Want to Dig Deeper?

- [Original API and EDA post](https://ericanti.github.io/my-blog/blog/api-usage/)
- [Streamlit app](https://ericanti-post3-streamlit-main-bzlgmr.streamlit.app/) for hands-on exploration
- GitHub repository for the and data: [GitHub Repo](https://github.com/ericanti/api-usage)

---

## Wrapping Up

The world of chart-topping music is always evolving. By exploring data on song features, genres, moods, and artist demographics, we can uncover the trends that define each era. Use the interactive app to find your own insights—and let us know what surprises you!

*What trends do you see? Share your findings or questions in the comments below!*

---