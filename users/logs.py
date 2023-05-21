import os , requests
def log(message):
    bot_token = os.environ.get("bot_token")
    groub_id = os.environ.get('groub_id')
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={groub_id}&parse_mode=Markdown&text={message}"
    requests.get(url)

