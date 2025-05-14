# Call Center API

A RESTful API for accessing call center report data from a SQL Server database.

## Overview

This API provides endpoints to retrieve call center complaint data for dashboard visualization. It connects to a SQL Server database and serves data through Express.js routes.

## Features

- SQL Server database integration
- RESTful API endpoints
- CORS support for cross-origin requests
- Error handling and logging

## Tech Stack

- Node.js
- Express.js
- SQL Server (MSSQL)
- Jade templating engine

## API Endpoints

### Test Connection
```
GET /callcenterreportdata/connect
```
Tests the database connection and returns a success message if connected.

### Get Call Center Data
```
GET /callcenterreportdata/getdata
```
Retrieves complaint data from the database including details such as complaint number, date, status, and other relevant information.

## Installation

1. Clone the repository
```
git clone https://github.com/imahmad00987655/Customer_service_api.git
```

2. Install dependencies
```
npm install
```

3. Configure database connection
   - Update the database configuration in `dbconfig.js` with your SQL Server credentials

4. Start the server
```
npm start
```
The server will start on port 3000 by default (or the port specified in your environment).

## Project Structure

- `app.js` - Main application file
- `bin/www` - Server startup script
- `routes/` - API route definitions
- `dboperation.js` - Database operations and queries
- `dbconfig.js` - Database configuration
- `views/` - Jade templates for rendering views
- `public/` - Static files

## GitHub Repository

The complete project is available at: [https://github.com/imahmad00987655/Customer_service_api](https://github.com/imahmad00987655/Customer_service_api)


