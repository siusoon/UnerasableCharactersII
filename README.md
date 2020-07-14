# Unerasable Characters II

![](unerasablecharactersII.gif)
*Unerasable Characters II: A fast forward illustration on how tweets are disappeared online*

[Click to RUN on your web browser](http://www.siusoon.net/projects/projects_mediaart/erasure/)

The project explores the temporality of voices and politics of erasure within the context of digital censorship via presenting the sheer scale of unheard voices and the endlessness of automation.

Unerasable Characters II: As part of the series Unerasable Characters, this version consists of a custom-software (written in python) that constantly scrapes the erased “tweets” from Weiboscope on a daily basis. Visually presenting the erased archives in a grid format, and each tweet is deconstructed into a character-by- character display (where each tweet with one character display at a time, and the installation can display around 500 tweets simultaneously). The duration of each ‘tweet’ is computed and translated from the original visible time online, which is calculated from subtracting erased time and created time on Weibo. As a result, the number of visible characters on the projected screens will decrease over time until all the text is fully disappeared. By then, the program will automatically pick up a new set of erased text and the cycle will be repeated. 

The project collects voices in the form of censored/erased (permission denied) text from Weibo via the platform called [weiboscope](https://weiboscope.jmsc.hku.hk/), developed by Dr. Fu, King Wa from Hong Kong University. Technically, it uses python to do the daily web scraping with limited data available (only past 7 days, max 200 records), and the front-end piece is written in p5.js. Based on experience, it will take the average of 18 hours for the  tweets to disapper on screen (which is also the time gap of the actual visibility of tweets)

*still in a fine-tuning stage: automate the daily data update, as well as replacing all the text with 🟥 except punctuation (it is not the matter of understanding the chinese characters)*

More info on the text from Weiboscope:  Fu, King-wa and Chan, Chung-hong and Chau, Michael, Assessing Censorship on Microblogs in China: Discriminatory Keyword Analysis and Impact Evaluation of the 'Real Name Registration' Policy (May 15, 2013). IEEE Internet Computing, Vol. 17, No. 3, pp. 42-50, May-June 2013, doi:10.1109/MIC.2013.28. Available at SSRN: https://ssrn.com/abstract=2265271

Proposed installation setup:

<img src="images/installation1.png" width="500">

running Unerasable Characters II at time T:

![](https://live.staticflickr.com/65535/49777309756_c10a86968d_c.jpg)

running Unerasable Characters II at time T + duration X 

![](https://live.staticflickr.com/65535/49777633092_f8e67dd414_c.jpg)


