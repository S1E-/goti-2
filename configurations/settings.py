# coding: utf-8
import os

TOKEN = "1306636984:AAHLxSJGshHgsS5fotUB0wGLJ_ayeTLMnWg"
NAME = "goti-3"
PORT = int(os.environ.get('PORT', '8443'))
WEBHOOK = True
## The following configuration is only needed if you setted WEBHOOK to True ##
WEBHOOK_OPTIONS = {
    'listen': '0.0.0.0',  # IP
    'port': PORT,
    'url_path': TOKEN,  # This is recommended for avoiding random people
                        # making fake updates to your bot
}
WEBHOOK_URL = "https://{}.herokuapp.com/{}".format(NAME, WEBHOOK_OPTIONS["url_path"])