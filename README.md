# Realtime Auction System

A simple CLI tool that simulates a realtime auction system between multiple clients and a central server using TCP sockets.

## Todo

- Client :

  - [x] Configuration
  - [x] Async Communication
  - [x] Auction logic + Messages Exchange
  - [x] Find a solution to stopping the Sending Thread when "END" input is accepted

- Server :
  - [x] Configuration
  - [x] Async Communication
  - [x] Starting the auction session + Auction logic + Messages Exchange
  - [x] Writing logs to text files
  - [x] Managing concurrent writing to text files
  - [x] Sending reciepts
  - [x] Find a solution to close the session after finishing
