# A python script to shorten url with Bitly API
A python script that shortens provided url with Bitly service
or gives clicks summary if url is already shortened bitly link.

## Requirements
Python >= 3.5 required.  
Install dependencies with 
```bash
pip install -r requirements.txt
```
For better interaction is recommended to use [virtualenv](https://github.com/pypa/virtualenv).

For successful work script required [Bitly](https://bitly.com) OAuth access token. 
For more details please read following: 
1.  [Bitly authentication documentation.](https://dev.bitly.com/authentication.html)
2.  [Bitly support theme answer.](https://support.bitly.com/hc/en-us/articles/230647907-How-do-I-find-my-OAuth-access-token-)

## Usage
In same directory with script create .env file with auth_bitly_token variable inside.

Examples:
```bash
python main.py http://ccbv.co.uk/
Link has been generated: http://bit.ly/2RllTNG
```
```bash
python main.py http://bit.ly/2LYO7bi
Bitly link clicks total summary : 5
```

