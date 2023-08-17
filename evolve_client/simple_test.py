from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simple Flask Frontend</title>
    </head>
    <body>
        <h1>Welcome to the Simple Flask Frontend!</h1>
        <p>This is a basic Flask application with a simple front end.</p>
    </body>
    </html>
    """
    
    return render_template_string(html_content)

@app.route('/about')
def about():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About Page</title>
    </head>
    <body>
        <h1>About Us</h1>
        <p>This is the about page for our simple Flask application.</p>
    </body>
    </html>
    """
    
    return render_template_string(html_content)


if __name__ == '__main__':
    app.run(debug=True)
