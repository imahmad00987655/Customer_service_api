module.exports = {
  server: "192.168.1.6",              // Use only the IP address
  database: "Rizwan",     // Database name
  options: {
    trustedConnection: false,
    enableArithAbort: true,
    encrypt: false,                      // Set to false if SSL is not configured
    trustServerCertificate: true,
    loginTimeout: 30,
    multisubnetfailover: true
  },
  driver: "mssql",
  port: 1433,                            // Explicitly specify the port
  user: "rizwan",
  password: "cs786"
};
