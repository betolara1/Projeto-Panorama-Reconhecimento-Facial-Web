CREATE DATABASE cadastro;

USE cadastro;

CREATE TABLE IF NOT EXISTS usuario(
    cod INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome CHAR(50) NOT NULL,
    telefone VARCHAR(11) NOT NULL,
    endereco VARCHAR (100) NOT NULL,
    cidade VARCHAR (20) NOT NULL,
    nome_foto VARCHAR(255),
    foto LONGBLOB,
    data_captura DATETIME
);