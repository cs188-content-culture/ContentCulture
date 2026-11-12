IF OBJECT_ID(N'dbo.Users', N'U') IS NULL
CREATE TABLE dbo.Users (
  userid INT IDENTITY(1,1) PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
);

IF OBJECT_ID(N'dbo.Media', N'U') IS NULL
CREATE TABLE dbo.Media (
  mediaid INT IDENTITY(1,1) PRIMARY KEY,
  userid INT FOREIGN KEY REFERENCES Users(userid),
  title VARCHAR(255) NOT NULL,
  medium VARCHAR(50) NOT NULL,
  rating INT NOT NULL,
  genre VARCHAR(50), NOT NULL,
  commentary VARCHAR(255), NOT NULL,
);

Driver={ODBC Driver 18 for SQL Server};Server=tcp:sql-server-cs188-mccarron-richie.database.windows.net,1433;Database=content-culture-prod;Uid=sql-server-admin;Pwd=CS188_fall_2026;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;