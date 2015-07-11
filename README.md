## GrahamBot

The main features of this bot are admin user profiles, contact recording in a database, dynamic message setting with a database, conditional message forwarding, and integration with Twitter and Yo.

I've set up a little Gumroad page so you can donate $2 if you have fun with the project:

<script type="text/javascript" src="https://gumroad.com/js/gumroad.js"></script>
#### <a class="gumroad-button" href="https://gumroad.com/l/lyjsM">Donate</a>

### Getting Started

1. Head over to [@yukuku's in-depth tutorial](https://github.com/yukuku/telebot) to get your bot set up and deployed on Google App Engine. Once you're done, come back here and clone this repo.

2. Copy the main.py file from this repo to your working repo based on telebot.

3. Create a file called private.py and fill it in as follows:
  
        token = 'YOUR_AUTH_TOKEN'                                  # e.g. '174076690:AAG5Lepi...'
        admin = YOUR CHAT_ID                                       # e.g.  1098359
        consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'                 # e.g. 'WAJllHDXx6t...'
        consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET'           # e.g. 'MropkLmPhdmcPhy...'
        access_token_key = 'YOUR_TWITTER_ACCESS_TOKEN_KEY'         # e.g. '86261335-36vazzj...'
        access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'   # e.g. 's91bJcLjSZ7Nt...'
        yo_api_token = 'YOUR_YO_API_TOKEN'                         # e.g. 'el2S594a-bc13-4n...'



4. Customise the text in all of the areas with a `reply()` in main.py to make it personal to you.

5. That's pretty much it! Before this app I had written about 10 lines of Python so my code may not be the best – but that should give you an idea of how easy it is to work with the API.

### Try It Out

Log in to Telegram and message [@grahambot](http://telegram.me/grahambot) – see what he can do!

### Licence 

GrahamBot is provided under an [Apache 2.0 licence](https://raw.githubusercontent.com/gmph/grahambot/master/LICENSE). You may use the code as you wish under the same open licence, provided you give attribution, make your changes clear, and keep all copyright notices. Go and tinker with it!

### Resources

The code in this repo is based heavily on the work of [@yukuku](http://github.com/yukuku)'s [telebot](https://github.com/yukuku/telebot). This starter kit will help you set your bot up and get it deployed on Google App Engine. My additions to the project were inspired by [@levelio](http://twitter.com/levelsio)'s work on [Taylor](http://taylorbot.com/). Integration with Twitter was done with the help of [Python Twitter](https://github.com/bear/python-twitter) and [Twtter API](https://dev.twitter.com/rest/public), and Yo integration with the [Yo API](http://docs.justyo.co/docs/getting-started).

### About Graham

This project was created by Graham Macphee, a Designer and Front-end Developer from Scotland. You can follow him on Twitter [@gmph](http://twitter.com/gmph) to stay updated with little projects like this. Have a lovely day!
