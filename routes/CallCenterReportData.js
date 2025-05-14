const express = require('express');
const router = express.Router();
const sql = require('../dboperation'); // Import SQL operations

// Test connection route
router.get('/connect', async (req, res) => {
  try {
    // Test DB connection
    await sql.getdata();
    res.status(200).json({ message: 'Connected to SQL Server successfully!' });
  } catch (error) {
    console.error("Connection Error: ", error);
    res.status(500).json({ error: 'Failed to connect to the database' });
  }
});

// Fetch data from the database
router.get('/getdata', async (req, res) => {
  try {
    // Fetch data using SQL query
    const result = await sql.getdata_withQuery();

    if (result.length > 0) {
      res.status(200).json(result); // Send fetched data as JSON
    } else {
      res.status(404).json({ error: "No data found" });
    }
  } catch (error) {
    console.error("API Error: ", error);
    res.status(500).json({ error: 'Error fetching data from the database' });
  }
});

module.exports = router;
