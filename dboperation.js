const sql = require('mssql');
const config = require('./dbconfig');

// Create a pool and connect to the database
let poolPromise = sql.connect(config)
  .then(pool => {
    console.log('Connected to SQL Server');
    return pool;
  })
  .catch(err => {
    console.error('Database connection failed: ', err);
    process.exit(1); // Exit if connection fails
  });

// Test connection
async function getdata() {
  try {
    const pool = await poolPromise;
    return pool; // Return pool if needed later
  } catch (error) {
    console.error('Error connecting to SQL Server: ', error);
    throw error;
  }
}

// Execute a query to fetch data
async function getdata_withQuery() {
  try {
    const pool = await poolPromise;
    const query = `
/****** Script for SelectTopNRows command from SSMS  ******/
SELECT  [cmpNo]
      ,[cmpDate]
      ,[currentStatus]
      ,[usedPeriod]
      ,[issueinMattress]
      ,[city]
      ,[fromUser]
      ,[complaintLatestRemarks]
      ,[equalQuality]
      ,[brandName]
      ,[zones]
      ,[territory]
      ,[user_no]
	    ,[status]
	    ,[level-type]
      ,[khi/lhr?]
      ,[using???? Yes/No]
	    ,FullName
      ,LoginName
      ,LoginPassword
      ,[pendingSinceDays]
      ,[closeOpen]
      ,[currentStatusLevelType]
  FROM [Rizwan].[dbo].[Vw_AllComplaintForDashboard] aa
  left join vw_userreferencetable bb on aa.user_no = bb.code
`;
    const result = await pool.request().query(query);
    return result.recordset; // Return fetched data
  } catch (error) {
    console.error('Error during query execution: ', error);
    throw error;
  }
}

module.exports = {
  getdata,
  getdata_withQuery
};
