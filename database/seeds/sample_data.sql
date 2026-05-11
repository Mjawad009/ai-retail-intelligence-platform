-- Sample data seed script
-- Insert sample products
INSERT INTO products (product_id, name, description, category, unit_cost, holding_cost_rate, order_cost)
VALUES
    ('SKU001', 'Laptop', 'High-performance laptop for professionals', 'Electronics', 500, 0.2, 50),
    ('SKU002', 'Mouse', 'Wireless ergonomic mouse', 'Accessories', 15, 0.25, 30),
    ('SKU003', 'Keyboard', 'Mechanical keyboard with RGB lighting', 'Accessories', 50, 0.2, 40),
    ('SKU004', 'Monitor', '27" 4K display monitor', 'Electronics', 200, 0.18, 45),
    ('SKU005', 'Headphones', 'Noise-cancelling wireless headphones', 'Audio', 80, 0.22, 35),
    ('SKU006', 'USB Cable', 'USB-C charging cable', 'Cables', 5, 0.3, 20),
    ('SKU007', 'Power Bank', '20000mAh portable power bank', 'Accessories', 30, 0.2, 30),
    ('SKU008', 'Webcam', '1080p HD webcam', 'Electronics', 60, 0.2, 35);

-- Insert sample inventory levels
INSERT INTO inventory_levels (product_id, current_stock, reserved_stock, available_stock)
VALUES
    ('SKU001', 45, 5, 40),
    ('SKU002', 120, 10, 110),
    ('SKU003', 85, 8, 77),
    ('SKU004', 35, 3, 32),
    ('SKU005', 60, 6, 54),
    ('SKU006', 250, 20, 230),
    ('SKU007', 95, 10, 85),
    ('SKU008', 50, 5, 45);

-- Insert sample sales data (30 days)
INSERT INTO sales_data (product_id, date, quantity_sold, revenue)
SELECT 
    product_id,
    CURRENT_DATE - (generate_series % 30)::integer,
    (RANDOM() * 20 + 10)::int as quantity_sold,
    ((RANDOM() * 20 + 10) * 
     CASE 
        WHEN product_id = 'SKU001' THEN 500
        WHEN product_id = 'SKU002' THEN 15
        WHEN product_id = 'SKU003' THEN 50
        WHEN product_id = 'SKU004' THEN 200
        WHEN product_id = 'SKU005' THEN 80
        WHEN product_id = 'SKU006' THEN 5
        WHEN product_id = 'SKU007' THEN 30
        WHEN product_id = 'SKU008' THEN 60
     END) as revenue
FROM 
    (SELECT DISTINCT product_id FROM products),
    (SELECT generate_series(1, 30)) as t
WHERE RANDOM() > 0.3;
