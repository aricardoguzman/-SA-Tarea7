from flask import Flask

app = Flask(__name__)

def wrap_html(message):
    html = """
        <html>
        <body>
            <div style='font-size:120px;'>
            <center>
                <image height="600" width="800" src="https://www.akamai.com/es/es/multimedia/images/article/akamai-dev-ops-overview-image.jpg?imwidth=1366">
                <br>
                {0}<br>
            </center>
            </div>
        </body>
        </html>""".format(message)
    return html

@app.route('/')
def hello_world():
    message = 'Hola T7 - SA!'
    html = wrap_html(message)
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
