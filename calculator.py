"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8089/multiply/3/5   => 15
  http://localhost:8089/add/23/42      => 65
  http://localhost:8089/subtract/23/42 => -19
  http://localhost:8089/divide/22/11   => 2
  http://localhost:8089/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
def divide(x,y):
    try:
        #suppose that number2 is a float
        return x/y
    except ZeroDivisionError:
        return "Cannot divide by 0"

calc_options = {'add': lambda x, y: x + y,
            'subtract': lambda x, y: x - y,
            'multiply': lambda x, y: x * y,
            'divide': lambda x, y:divide(x,y),
           }


def landing():
    """ TODO: copy description above or add some description """

    landing_page = """<html>
    <head>
    <title>WSGI Calculator</title>
    </head>
    <body>
    The WSGI calculator supports the following operations:<br>
    Addition<br>
    Subtraction<br>
    Multiplication<br>
    Division<br>
    <br>
    Examples:<br>
    http://localhost:8089/multiply/3/5  => 15<br>
    http://localhost:8089/add/23/42     => 65<br>
    http://localhost:8089/divide/6/0    => HTTP "400 Bad Request"<br>
    </body>
    </html>"""

    return landing_page


def math_proc(operator, operands):
    """ Perform math operation specified by 'operator' on 'operands' """
    
    result_page = """<html>
    <head>
    <title>WSGI Calculator</title>
    </head>
    <body>
    Answer: {}
    </body>
    </html>"""

    try:
        results = calc_optinos[operator.lower()](operands[0], operands[1])
    except:
        raise ValueError

    return result_page.format(answer)

    
def resolve_path(path):
    """ Resolve the path and return body """

    parts = path.strip('/').split('/')
    if not parts[0]:
        return landing()

    elif len(parts) == 3:
        return math_proc(parts[0], [int(i) for i in parts[1:]])

    else:
        raise NameError

def application(environ, start_response):
    """ A WSGI application for doing basic math via the url """

    import pprint
    pprint.pprint(environ)

    headers = [("Content-type", "text/html")]

    try:
        path = environ.get('PATH_INFO', None)
        body = resolve_path(path)
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
        body += landing()

    except ValueError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>"
        body += landing()

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        body += landing()

    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)

        return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
