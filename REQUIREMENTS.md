# Coding Challenge

## Requirements:

### Provide all Python source code to perform the requested actions and answer any questions as follows:

- Use Python 3.8 as base version
- Create a class for all API interactions with methods for all interactions with the API
- Use pythonic practices as much as possible, including formatting matching PEP-8 standards
- Bonus Points - Include pytest based unit tests

## Scenario:

The JSONPlaceholder website allows for testing against a sample set of data, description here: http://jsonplaceholder.typicode.com/
Notice that examples are in JavaScript, you will have to translate what is expected to Python.
(Full endpoint API docs here: http://jsonplaceholder.typicode.com/guide.html)

### Using the API to interact with the JSONPlaceholder website, accomplish the following goals:

1. Print the value of the title for post number 99
2. Inject a field called time into the results for post number 100 and print the whole JSON record

    1. Use the datetime library to perform this action with a UTC timestamp matching the following format DD/MM/YYYY HH:MM:SS

3. Create a new /posts entry which the following values

    1. Title: Security Interview Post
    2. UserID: 500
    3. Body: This is an insertion test with a known API

4. Determine if your post was successful, and if it was, create a tuple of the 3 following values:

    1. The “id” field of the new record
    2. The status code returned from the POST
    3. The value of the “x-Powered-By” field in the headers

5. Print the tuple from #4
6. Delete the record you created in #3, by referencing the new “id”. Print the return status code and the x-content-type-options from the returned object

## Grading Aspects:

1. Code must function correctly. Syntax errors or other logic errors preventing code from full functionality is a failure.
2. Code should be formatted to PEP-8 standards
3. A class with methods for defining API interactions must be created and utilized
4. Naming, spacing, logic, should all be as pythonic as possible
5. Unit testing is a big bonus...full or mostly full coverage with effective testing should all but guarantee a pass