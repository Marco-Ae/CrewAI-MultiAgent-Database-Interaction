--DROP TABLE utenti, prenotazioni 

CREATE TABLE utenti (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE prenotazioni (
    booking_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    flight_number VARCHAR(10) NOT NULL,
    departure_airport VARCHAR(50) NOT NULL,
    arrival_airport VARCHAR(50) NOT NULL,
    departure_date DATE NOT NULL,
    arrival_date DATE NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    baggage_included BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES utenti(user_id)
);

INSERT INTO utenti (first_name, last_name, email, phone) VALUES
('Luca','Rossi','luca.rossi@example.com','+390612345678'),
('Maria','Bianchi','maria.bianchi@example.com','+390612345679'),
('Giovanni','Verdi','giovanni.verdi@example.com','+390612345680'),
('Elena','Neri','elena.neri@example.com','+390612345681'),
('Marco','Gallo','marco.gallo@example.com','+390612345682'),
('Sara','Russo','sara.russo@example.com','+390612345683'),
('Paolo','Ferrari','paolo.ferrari@example.com','+390612345684'),
('Anna','Greco','anna.greco@example.com','+390612345685'),
('Matteo','Moretti','matteo.moretti@example.com','+390612345686'),
('Francesca','Costa','francesca.costa@example.com','+390612345687'),
('Alessandro','Marini','alessandro.marini@example.com','+390612345688'),
('Valentina','Fontana','valentina.fontana@example.com','+390612345689'),
('Simone','Barbieri','simone.barbieri@example.com','+390612345690'),
('Chiara','Conti','chiara.conti@example.com','+390612345691'),
('Davide','Pellegrini','davide.pellegrini@example.com','+390612345692'),
('Ilaria','Bianco','ilaria.bianco@example.com','+390612345693'),
('Riccardo','De Luca','riccardo.deluca@example.com','+390612345694'),
('Giulia','Sarti','giulia.sarti@example.com','+390612345695'),
('Federico','Villa','federico.villa@example.com','+390612345696'),
('Martina','Parisi','martina.parisi@example.com','+390612345697');

INSERT INTO prenotazioni (user_id, flight_number, departure_airport, arrival_airport, departure_date, arrival_date, price, baggage_included) VALUES
(1,'AZ123','FCO','JFK','2025-11-01','2025-11-01',450.00,TRUE),
(2,'LH456','MXP','FRA','2025-11-03','2025-11-03',120.50,FALSE),
(3,'BA789','LHR','CDG','2025-11-05','2025-11-05',85.75,TRUE),
(4,'AF321','CDG','FCO','2025-11-06','2025-11-06',150.00,TRUE),
(5,'KL654','AMS','JFK','2025-11-07','2025-11-07',400.00,FALSE),
(6,'IB987','MAD','FCO','2025-11-08','2025-11-08',180.00,TRUE),
(7,'AZ111','FCO','MXP','2025-11-09','2025-11-09',90.00,FALSE),
(8,'LH222','FRA','CDG','2025-11-10','2025-11-10',75.50,TRUE),
(9,'BA333','LHR','AMS','2025-11-11','2025-11-11',200.00,FALSE),
(10,'AF444','CDG','MAD','2025-11-12','2025-11-12',220.00,TRUE),
(11,'KL555','AMS','FCO','2025-11-13','2025-11-13',320.00,TRUE),
(12,'IB666','MAD','LHR','2025-11-14','2025-11-14',250.00,FALSE),
(13,'AZ777','FCO','JFK','2025-11-15','2025-11-15',450.00,TRUE),
(14,'LH888','MXP','FRA','2025-11-16','2025-11-16',130.00,FALSE),
(15,'BA999','LHR','CDG','2025-11-17','2025-11-17',95.50,TRUE),
(16,'AF000','CDG','FCO','2025-11-18','2025-11-18',155.00,TRUE),
(17,'KL101','AMS','JFK','2025-11-19','2025-11-19',410.00,FALSE),
(18,'IB202','MAD','FCO','2025-11-20','2025-11-20',185.00,TRUE),
(19,'AZ303','FCO','MXP','2025-11-21','2025-11-21',100.00,FALSE),
(20,'LH404','FRA','CDG','2025-11-22','2025-11-22',80.00,TRUE);