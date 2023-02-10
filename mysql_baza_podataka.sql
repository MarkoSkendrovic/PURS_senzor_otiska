DROP DATABASE IF EXISTS korisnici;
CREATE DATABASE korisnici;
USE korisnici;

CREATE TABLE korisnik(
	id INT PRIMARY KEY AUTO_INCREMENT,
    email CHAR(50) NOT NULL,
    username CHAR(50) NOT NULL,
    password BINARY(32) NOT NULL,
    fingerprint_id TINYINT NOT NULL,
    slika_profila CHAR(50) NOT NULL,
    id_uloge TINYINT
);

INSERT INTO korisnik(email, username, password, fingerprint_id, slika_profila,id_uloge) VALUES
	('mskendrov@gmail.com', 'Marko Skendrović', UNHEX(SHA2('dadada', 256)), '1', 'markoskendrovic','1'),
    ('ddutkovic@gmail.com', 'Dominik Dutković', UNHEX(SHA2('nenene', 256)), '2','dominikdutkovic','1'),
    ('jozajozic@gmail.com', 'Joza Jozic', UNHEX(SHA2('jjjjj', 256)), '3','korisnik','2'),
    ('peroperi@gmail.com', 'Pero Peric', UNHEX(SHA2('pppp', 256)), '4','korisnik','2'),
    ('matildamatildovic@gmail.com', 'Matilda Matildovic', UNHEX(SHA2('mmmm', 256)), '5','korisnik','2');
    
SELECT HEX(password) FROM korisnik;
SELECT username FROM  korisnik WHERE HEX(password) = '' AND email = '';

CREATE TABLE prisutnost(
	id INT PRIMARY KEY AUTO_INCREMENT,
    username CHAR(50) NOT NULL,
	vrijeme DATETIME default NOW()
    );
    
INSERT INTO prisutnost(username, vrijeme) VALUES
('Marko Skendrovic', '1999-09-21 13:21:15'),
('Joza Jozic', '1989-01-15 18:13:22');
