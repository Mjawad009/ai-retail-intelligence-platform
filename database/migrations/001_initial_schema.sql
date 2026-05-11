-- Database initialization script
-- Create the retail database and tables

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    unit_cost FLOAT DEFAULT 0.0,
    holding_cost_rate FLOAT DEFAULT 0.2,
    order_cost FLOAT DEFAULT 50.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_id ON products(product_id);
CREATE INDEX idx_category ON products(category);

-- Create sales_data table
CREATE TABLE IF NOT EXISTS sales_data (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    date TIMESTAMP NOT NULL,
    quantity_sold FLOAT NOT NULL,
    revenue FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_date ON sales_data(product_id, date);

-- Create inventory_levels table
CREATE TABLE IF NOT EXISTS inventory_levels (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) UNIQUE NOT NULL,
    current_stock FLOAT NOT NULL DEFAULT 0.0,
    reserved_stock FLOAT DEFAULT 0.0,
    available_stock FLOAT DEFAULT 0.0,
    last_restock_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create forecasts table
CREATE TABLE IF NOT EXISTS forecasts (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    forecast_date TIMESTAMP NOT NULL,
    forecast_days INTEGER DEFAULT 7,
    hybrid_forecast TEXT,
    arima_forecast TEXT,
    gb_forecast TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_forecast_date ON forecasts(product_id, forecast_date);

-- Create risk_analysis table
CREATE TABLE IF NOT EXISTS risk_analysis (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    analysis_date TIMESTAMP NOT NULL,
    current_stock FLOAT,
    safety_stock FLOAT,
    reorder_point FLOAT,
    stockout_risk_score FLOAT,
    stockout_risk_level VARCHAR(20),
    recommended_order_qty FLOAT,
    days_to_stockout FLOAT,
    reorder_recommended BOOLEAN DEFAULT FALSE,
    critical_alert BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_analysis_date ON risk_analysis(product_id, analysis_date);

-- Create reorder_recommendations table
CREATE TABLE IF NOT EXISTS reorder_recommendations (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    recommendation_date TIMESTAMP NOT NULL,
    category VARCHAR(50),
    reason VARCHAR(255),
    suggested_quantity FLOAT,
    priority INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_date_status ON reorder_recommendations(product_id, recommendation_date, status);

-- Create analytics_queries table
CREATE TABLE IF NOT EXISTS analytics_queries (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    query_type VARCHAR(50),
    result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
