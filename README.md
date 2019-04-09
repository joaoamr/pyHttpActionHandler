# pyHttpActionHandler
A python hypertext preprocessor HttpHandler class

The handler enables to embed Python codes in html pages, just like PHP, ASP, C#, etc. 
To use this feature the file must be a .pyhtml file.
The pyhtml file structure is partitioned in two sections:

## Server action: 

Here is where we place Python codes to run in its server. The commands must be inside the structure:

```
<.py

'''Python commands'''

.>
```

This structure is sensitive to line breakers, as well as Python codes. 
It is also able to handle GET and POST requests. These params are stored in two dictionaries: _POST_ for POST requests and _GET_ for GET 
requests. For exemple:

```
<.py

'''Bind POST param name'''

name = POST['name']

.>
```
```
<.py

'''Bind GET param name'''

name = GET['name']

.>
```

## Hypertext response:

Anything outside the structure mentioned that embeds Python codes is sent to client as response. To bind a variable to its section it is necessary to use .py(varname). For instance:

```
<.py

msg = 'hello'

.>

Python says .py(msg) to you!
```

If the variable name does not exists, for exemple, .py(invalid), the programs binds the directive as it is, that is .py(invalid).

## Echo:

You may also send data dinamically using the _echo_ function. For example:

```
<.py

echo('Python says hello to you!')

.>
```

## Try it:
The program httpserver_example.py runs an example of a Python Http server with pyHttpActionHandler. Try it!
