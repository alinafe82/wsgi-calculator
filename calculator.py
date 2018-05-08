#!/usr/bin/env python

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
application at `http://localhost:8090/multiple/3/5' then the response
body in my browser should be `15`.
Consider the following URL/Response body pairs as tests:
```
  http://localhost:8090/multiply/3/5   => 15
  http://localhost:8090/add/23/42      => 65
  http://localhost:8090/subtract/23/42 => -19
  http://localhost:8090/divide/22/11   => 2
  http://localhost:8090/               => <html>Here's how to use this page...</html>
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

html_text = """<html>
<head>
<title>WSGI Calulator </title>
</head>
<body>
<h1>{print_op_a} {print_op_sign} {print_op_b}
= {print_result}</h1>
<hr>
<h3>Try links below</h3>
<p><a href="http://localhost:8090/add/2/10">add/2/10</a></p>
<p><a href="http://localhost:8090/divide/4/0">divide/4/0</a></p>
<p><a href="http://localhost:8090/subtract/1300/30">subtract/1300/30</a></p>
<p><a href="http://localhost:8090/multiply/4/7">multiply/4/7</a></p>
<p><a href="http://localhost:8090/divide/42/6">divide/42/6</a></p>
<p><a href="http://localhost:8090/subtract/12/0">subtract/12/0</a></p>
<hr>
<p>Path Info: {print_path} Entries: {print_no_entries}</p>
<p>Operation: {print_op} First Op: {print_op_a}
Second Op: {print_op_b}</p>
</body>
</html>"""


def app(environ, start_response):
    import pprint
    pprint.pprint(environ)
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError

        args = resolve_path(path)

        if len(args) != 3:
            op_sign = "f"
        else:
            pass

        ops = ["multiply", "divide", "add", "subtract"]

        if args[0].strip() in ops:
            oper = args[0].strip()
        else:
            oper = "failed"
            op_sign = "f"

        try:
            op_a = int(args[1])
        except:
            op_a = "error"

        try:
            op_b = int(args[2])
        except:
            op_b = "error"

        if oper == "multiply":
            result = op_a * op_b
            op_sign = "*"
        elif oper == "divide":
            if op_b == 0:
                result = "can't divide by zero"
                op_sign = "/"
            else:
                result = op_a / op_b
                op_sign = "/"
        elif oper == "add":
            result = op_a + op_b
            op_sign = "+"
        elif oper == "subtract":
            result = op_a - op_b
            op_sign = "-"
        elif oper == "failed":
            result = "error - please try again"
            op_sign = "f"
        else:
            result = "failed"

        body = html_text.format(
            print_path=path,
            print_no_entries=len(args),
            print_op=oper,
            print_op_sign=op_sign,
            print_op_a=op_a,
            print_op_b=op_b,
            print_result=result
        )
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"

    except ValueError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>"

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error, check the code!</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def resolve_path(path):
    args = path.strip("/").split("/")
    return args


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8090, app)
    srv.serve_forever()
