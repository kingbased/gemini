import browser_cookie3
from bardapi import SESSION_HEADERS, BardCookies
import requests
from flask import Flask, request

app = Flask(__name__)


def get_cookies_and_session():
    psid = '__Secure-1PSID'
    dts = '__Secure-1PSIDTS'
    dcc = '__Secure-1PSIDCC'
    nid = 'NID'

    try:
        cookers = browser_cookie3.firefox(domain_name='.google.com')
    except browser_cookie3.BrowserCookieError:
        cookers = browser_cookie3.librewolf(domain_name='.google.com')

    cookie_dict = {}
    session = requests.Session()
    session.headers = SESSION_HEADERS

    for cookie in cookers:
        if cookie.name in [psid, dts, dcc, nid]:
            cookie_dict[cookie.name] = cookie.value
            session.cookies.set(cookie.name, cookie.value)

    bard = BardCookies(session=session, cookie_dict=cookie_dict, timeout=60)
    return bard


def parse_messages(messages):
    return '\n\n'.join(f"{message['role']}: {message['content']}" for message in messages)


@app.route("/v1/models", methods=["GET"])
def models():
    return {"model": "Gemini Advanced"}


@app.route("/v1/chat/completions", methods=["POST"])
def complete():
    bard = get_cookies_and_session()
    try:
        prompt = parse_messages(request.json['messages'])
        response = bard.get_answer(prompt)
        conversation_id = response.get('conversation_id')
        data = str(response['content'])

        response = {
            "id": 0,
            "object": "chat.completion",
            "model": "Gemini Advanced",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": data
                    },
                    "logprobs": None,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(data.split()),
                "total_tokens": len(prompt.split()) + len(data.split())
            },
        }
        if conversation_id is None:
            return {"error": {"message": "Gemini returned an error (most likely too much context or cookies expired)"}}, 500
        print(data)
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return {"error": {"message": str(e)}}, 500


if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=False)
