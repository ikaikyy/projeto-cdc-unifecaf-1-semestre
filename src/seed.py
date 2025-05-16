import mysql.connector


def seed_database(connection: mysql.connector.MySQLConnection):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, phone_number, cpf) VALUES
        ('Ana Souza', 'ana@example.com', '11912345678', '12345678901'),
        ('Carlos Lima', 'carlos@example.com', '11987654321', '23456789012'),
        ('Beatriz Melo', 'bia@example.com', '11911223344', '34567890123'),
        ('Daniel Rocha', 'daniel@example.com', '11922334455', '45678901234'),
        ('Elisa Martins', 'elisa@example.com', '11933445566', '56789012345'),
        ('Fabio Oliveira', 'fabio@example.com', '11944556677', '67890123456'),
        ('Gustavo Silva', 'gustavo@example.com', '11955667788', '78901234567'),
        ('Helena Costa', 'helena@example.com', '11966778899', '89012345678'),
        ('Igor Ramos', 'igor@example.com', '11977889900', '90123456789'),
        ('Juliana Ferreira', 'juliana@example.com', '11988990011', '01234567890');
    """)

    cursor.execute("""
        INSERT INTO addresses (state, city, cep, 1st_line, 2nd_line, 3rd_line, user_id) VALUES
        ('SP', 'São Paulo', '01001000', 'Rua A, 100', NULL, NULL, 1),
        ('RJ', 'Rio de Janeiro', '20040002', 'Av. B, 200', 'Bloco 2', NULL, 2),
        ('MG', 'Belo Horizonte', '30140071', 'Rua C, 300', NULL, NULL, 3),
        ('RS', 'Porto Alegre', '90010000', 'Av. D, 400', 'Ap. 101', NULL, 4),
        ('BA', 'Salvador', '40020000', 'Rua E, 500', NULL, NULL, 5),
        ('PR', 'Curitiba', '80010000', 'Av. F, 600', 'Bloco B', 'Ap. 204', 6),
        ('SC', 'Florianópolis', '88010000', 'Rua G, 700', NULL, NULL, 7),
        ('PE', 'Recife', '50010000', 'Av. H, 800', NULL, NULL, 8),
        ('CE', 'Fortaleza', '60010000', 'Rua I, 900', NULL, 'Casa 3', 9),
        ('DF', 'Brasília', '70000000', 'Quadra J, Lote 10', NULL, NULL, 10);
    """)

    cursor.execute("""
        INSERT INTO products (name, description, price, available_on_stock) VALUES
        ('Notebook', 'Notebook i5 com 8GB RAM', 3500.00, 20),
        ('Mouse', 'Mouse óptico USB', 50.00, 100),
        ('Teclado', 'Teclado mecânico RGB', 250.00, 50),
        ('Monitor', 'Monitor 24" Full HD', 800.00, 30),
        ('Impressora', 'Impressora multifuncional', 600.00, 25),
        ('Webcam', 'Webcam Full HD', 150.00, 40),
        ('Fone de Ouvido', 'Headset Gamer', 200.00, 35),
        ('HD Externo', 'HD 1TB USB 3.0', 400.00, 15),
        ('Pen Drive', 'Pen Drive 64GB', 70.00, 60),
        ('Cadeira Gamer', 'Cadeira com apoio lombar', 1200.00, 10);
    """)

    cursor.execute("""
        INSERT INTO carts (id) VALUES
        (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);
    """)

    cursor.execute("""
        INSERT INTO orders (total_price, created_at, user_id, address_id) VALUES
        (500.00, NOW(), 1, 1),
        (1500.00, NOW(), 2, 2),
        (750.00, NOW(), 3, 3),
        (1000.00, NOW(), 4, 4),
        (1250.00, NOW(), 5, 5),
        (250.00, NOW(), 6, 6),
        (320.00, NOW(), 7, 7),
        (990.00, NOW(), 8, 8),
        (430.00, NOW(), 9, 9),
        (1800.00, NOW(), 10, 10);
    """)

    cursor.execute("""
        INSERT INTO orders_products (quantity, order_id, product_id) VALUES
        (1, 1, 1),
        (2, 2, 2),
        (1, 3, 3),
        (3, 4, 4),
        (1, 5, 5),
        (1, 6, 6),
        (2, 7, 7),
        (1, 8, 8),
        (4, 9, 9),
        (1, 10, 10);
    """)

    cursor.execute("""
        INSERT INTO carts_products (quantity, product_id, cart_id) VALUES
        (1, 1, 1),
        (2, 2, 2),
        (1, 3, 3),
        (1, 4, 4),
        (2, 5, 5),
        (3, 6, 6),
        (1, 7, 7),
        (1, 8, 8),
        (2, 9, 9),
        (1, 10, 10);
    """)

    cursor.execute("""
        INSERT INTO categories (name) VALUES
        ('Eletrônicos'),
        ('Acessórios'),
        ('Informática'),
        ('Periféricos'),
        ('Móveis'),
        ('Áudio'),
        ('Armazenamento'),
        ('Imagem'),
        ('Impressão'),
        ('Jogos');
    """)

    cursor.execute("""
        INSERT INTO products_categories (product_id, category_id) VALUES
        (1, 1),
        (2, 2),
        (3, 4),
        (4, 8),
        (5, 9),
        (6, 8),
        (7, 6),
        (8, 7),
        (9, 7),
        (10, 5);
    """)

    connection.commit()
    print("Database seeded successfully.")
