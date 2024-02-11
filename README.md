gemini (formerly bard) proxy

## Installation
- setup a venv
- install requirements
- replace the installed bardapi package `.venv/Lib/bardapi` with mine `bardapi.7z` found in this repo (latest official version is not yet updated to support gemini, do not skip this step)
- log into gemini with your google account in firefox/librewolf

## Usage
- run `python main.py` in the terminal
- select openai as your chat completion source in ST and set the proxy URL to `http://localhost:3000/v1`
- disable streaming and limit your context to 8-9k (i was getting errors with anything more, not sure why considering the model should be 32k)
- refresh the gemini page in your browser every 10-15 minutes so you rotate expired cookies

## Notes
- this will create a new conversation for each prompt.
- yes, you have to use a firefox based browser, unless you manually want to retrieve and set 4 cookies every 10 minutes. i don't. autofetching cookies no longer works on chromium based browsers without elevation since the cookie db is protected
