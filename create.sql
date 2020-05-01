CREATE TABLE transactions (
    id int(10) NOT NULL AUTO_INCREMENT,
    timestamp varchar(50) NOT NULL,
    amount float NOT NULL,
    current_bal float NOT NULL,
    PRIMARY KEY(id)
);