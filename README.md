## GrahamBot

The code in this repo is based heavily on the work of [@yukuku](http://github.com/yukuku)'s [telebot](https://github.com/yukuku/telebot). This starter kit will help you set your bot up and get it deployed on Google App Engine. My additions to the project were inspired by [@levelio](http://twitter.com/levelsio)'s work on [Taylor](http://taylorbot.com/).

My additions include admin user profiles, contact recording in a database, dynamic message setting with a database, conditional message forwarding and a few more things.

### Getting Started

1. Head over to [@yukuku's in-depth tutorial](https://github.com/yukuku/telebot) to get your bot set up and deployed on Google App Engine. Once you're done, come back here and clone this repo.

2. Copy the main.py file from this repo to your working repo based on telebot.

3. Create a file called private.py and fill it in as follows:
  
        token = 'YOUR_AUTH_TOKEN' # your token as a string, e.g. '174076690:AAGI8EJ55hdLepi...'
        admin = YOUR CHAT_ID      # your chat id as an int, e.g. 1098359

4. Customise the text in all of the areas with a `reply()` in main.py to make it personal to you.

5. That's pretty much it! Before this app I had written about 10 lines of Python so my code may not be the best – but that should give you an idea of how easy it is to work with the API.

### Try It Out

Log in to Telegram and message [@grahambot](http://telegram.me/grahambot) – see what he can do!

### About Graham

This project was created by Graham Macphee, a Designer and Front-end Developer from Scotland. You can follow him on Twitter [@gmph](http://twitter.com/gmph) to stay updated with little projects like this. Have a lovely day!
