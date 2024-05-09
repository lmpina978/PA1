# CPSC-471 Programming Assignment
## Team Members: 
- Kyle Lee - ipark604@csu.fullerton.edu
- Daniel Currey - dcurrey@csu.fullerton.edu
- Brett Chiu - brettc@csu.fullerton.edu
- Luke Pina - lukepina@csu.fullerton.edu
- Jonathan Gaytan - jagaytan@csu.fullerton.edu

## Programming Language Used:
Python

## How To Execute Program:
Note: The `server.py` file needs to be ran in the same directory where the `files` folder is located. The uploads will be placed in the `files` directory.

1. Start the server
`python3 server.py {port number}`
`ex: python3 server.py 21`

2. Start the client(s)
`python3 client.py {server machine} {port numer}`
`ex: python3 client.py 127.0.0.1 21`

3. Input commands into the client terminal(s)

## Anything Special About Submission:
- Has unit tests using .txt files in order to reinforce data partitioning, three for client unit test, five for server unit test
- Running the `client.py` and `server.py` files will require being in the same directory where the `files` folder is located in order to properly retrieve and upload files
- Requires Python 3.9.6 or greater
