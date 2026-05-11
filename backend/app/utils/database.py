"""Database configuration and utilities"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Database connection string
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://retail_user:retail_password@localhost:5432/retail_db'
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def seed_sample_data():
    """Seed sample data for demo"""
    from app.models import Product, InventoryLevel
    from datetime import datetime
    import random
    
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(Product).count() > 0:
            print("Database already seeded")
            return
        
        # Create sample products
        products_data = [
            {'product_id': 'SKU001', 'name': 'Laptop', 'category': 'Electronics', 'unit_cost': 500},
            {'product_id': 'SKU002', 'name': 'Mouse', 'category': 'Accessories', 'unit_cost': 15},
            {'product_id': 'SKU003', 'name': 'Keyboard', 'category': 'Accessories', 'unit_cost': 50},
            {'product_id': 'SKU004', 'name': 'Monitor', 'category': 'Electronics', 'unit_cost': 200},
            {'product_id': 'SKU005', 'name': 'Headphones', 'category': 'Audio', 'unit_cost': 80},
            {'product_id': 'SKU006', 'name': 'USB Cable', 'category': 'Cables', 'unit_cost': 5},
            {'product_id': 'SKU007', 'name': 'Power Bank', 'category': 'Accessories', 'unit_cost': 30},
            {'product_id': 'SKU008', 'name': 'Webcam', 'category': 'Electronics', 'unit_cost': 60},
        ]
        
        products = []
        for p_data in products_data:
            product = Product(
                product_id=p_data['product_id'],
                name=p_data['name'],
                category=p_data['category'],
                unit_cost=p_data['unit_cost'],
                holding_cost_rate=0.2,
                order_cost=50
            )
            db.add(product)
            products.append(product)
        
        db.commit()
        
        # Create inventory levels
        for product in products:
            inventory = InventoryLevel(
                product_id=product.product_id,
                current_stock=random.randint(10, 100),
                reserved_stock=random.randint(0, 20),
                available_stock=random.randint(5, 80)
            )
            db.add(inventory)
        
        db.commit()
        print("Sample data seeded successfully")
    
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()
