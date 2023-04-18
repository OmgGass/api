CREATE DATABASE api_pog;

USE api_pog;

CREATE TABLE site1_users(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    cpf VARCHAR(11) NOT NULL
);


CREATE TABLE cards_site1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    card_number VARCHAR(16),
    expiration_date DATE,
    cvv INT,
    FOREIGN KEY (user_id) REFERENCES site1_users(id)
);
