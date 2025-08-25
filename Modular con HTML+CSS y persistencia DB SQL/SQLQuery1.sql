CREATE DATABASE parqueo;
GO
USE parqueo;
GO

CREATE TABLE Vehiculos (
    Placa VARCHAR(20) PRIMARY KEY,
    Tipo VARCHAR(10),
    Marca VARCHAR(100),
    Modelo VARCHAR(100),
    Color VARCHAR(50)
);

CREATE TABLE EspaciosAutos (
    Clave VARCHAR(10) PRIMARY KEY,
    Placa VARCHAR(20) NULL
);

CREATE TABLE EspaciosMotos (
    Clave VARCHAR(10) PRIMARY KEY,
    Placa VARCHAR(20) NULL
);

CREATE TABLE EspaciosValet (
    Clave VARCHAR(10) PRIMARY KEY,
    Placa VARCHAR(20) NULL
);

CREATE TABLE ValetOrder (
    Pos INT PRIMARY KEY,
    Placa VARCHAR(20)
);

CREATE TABLE EspaciosCola (
    Clave VARCHAR(10) PRIMARY KEY,
    Placa VARCHAR(20) NULL
);

CREATE TABLE ColaOrder (
    Pos INT PRIMARY KEY,
    Placa VARCHAR(20)
);

CREATE TABLE Calle (
    Clave VARCHAR(20) PRIMARY KEY,
    Placa VARCHAR(20) NULL,
    OrigSlot VARCHAR(20) NULL
);

CREATE TABLE Historial (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Placa VARCHAR(20),
    Tipo VARCHAR(10),
    Marca VARCHAR(100),
    Modelo VARCHAR(100),
    Color VARCHAR(50),
    HoraEntrada DATETIME,
    HoraSalida DATETIME,
    TotalPagado FLOAT,
    Ubicacion VARCHAR(50)
);

CREATE TABLE Config (
    [Key] VARCHAR(50) PRIMARY KEY,
    [Value] VARCHAR(200)
);



