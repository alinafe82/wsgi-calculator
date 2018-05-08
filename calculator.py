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
application at `http://localhost:8080/multiple/3/5' then the response
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
<h1>{print_operand_a} {print_operation_sign} {print_operand_b}
= {print_result}</h1>
<hr>
<h3>Some Examples</h3>
<p><a href="http://localhost:8090/multiply/3/5">multiply/3/5</a></p>
<p><a href="http://localhost:8090/add/23/42">add/23/42</a></p>
<p><a href="http://localhost:8090/divide/6/0">divide/6/0</a></p>
<p><a href="http://localhost:8090/subtract/126/21">subtract/126/21</a></p>
<p><a href="http://localhost:8090/divide/4223/17">divide/4223/17</a></p>
<p><a href="http://localhost:8090/subtract/123/0">subtract/123/0</a></p>
<hr>
<p>Path Info: {print_path_info} Entries: {print_no_entries}</p>
<p>Operation: {print_operation} First Operand: {print_operand_a}
Second Operand: {print_operand_b}</p>
</body>
</html>"""


def application(environ, start_response):
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
            operation = args[0].strip()
        else:
            operation = "failed"
            op_sign = "f"

        try:
            op_a = int(args[1])
        except:
            op_a = "error"

        try:
            op_b = int(args[2])
        except:
            op_b = "error"

        if operation == "multiply":
            result = op_a * op_b
            op_sign = "*"
        elif operation == "divide":
            if op_b == 0:
                result = "can't divide by zero"
                op_sign = "/"
            else:
                result = op_a / op_b
                op_sign = "/"
        elif operation == "add":
            result = op_a + op_b
            op_sign = "+"
        elif operation == "subtract":
            result = op_a - op_b
            op_sign = "-"
        elif operation == "failed":
            result = "error - please try again"
            op_sign = "f"
        else:
            result = "failed"

        body = html_text.format(
            print_path_info=path,
            print_no_entries=len(args),
            print_operation=operation,
            print_operation_sign=op_sign,
            print_operand_a=op_a,
            print_operand_b=op_b,
            print_result=result
        )
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"

    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def resolve_path(path):
    args = path.strip("/").split("/")
    return args


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8090, application)
    srv.serve_forever()
