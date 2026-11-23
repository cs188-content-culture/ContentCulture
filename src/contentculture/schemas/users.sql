IF OBJECT_ID(N'dbo.Users', N'U') IS NULL
CREATE TABLE dbo.Users (
  userid INT IDENTITY(1,1) PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL,
  display_name VARCHAR(50) NOT NULL
);

IF OBJECT_ID(N'dbo.Media', N'U') IS NULL
CREATE TABLE dbo.Media (
  mediaid INT IDENTITY(1,1) PRIMARY KEY,
  userid INT NOT NULL FOREIGN KEY REFERENCES dbo.Users(userid),
  title VARCHAR(255) NOT NULL,
  medium VARCHAR(50) NOT NULL,
  rating INT NOT NULL,
  genre VARCHAR(50) NOT NULL,
  commentary VARCHAR(255) NOT NULL
);