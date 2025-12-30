# Generate Synthetic Data
## 📊 Overview 
This project uses Python and Faker to generate relationally consistent synthetic data for an E-commerce OLTP system, following predefined schema and business logic. The data supports PostgreSQL, MySQL, and SQL Server for testing and learning purposes.
## 🎯 Objectives
- Design and implement a **relational E-commerce OLTP database schema** covering core business entities such as brands, categories, sellers, products, orders, and promotions.
- Generate **synthetic but realistic transactional data** that reflects real E-commerce operations, including product listings, customer orders, inventory levels, and promotional campaigns.
- Ensure **full referential integrity** across all tables, with valid foreign key relationships and logically consistent data flows.
- Support **hierarchical structures** (e.g., category levels) and **many-to-many relationships** (e.g., promotions applied to multiple products).
## 📂 Project Structure
```
├── config/          # Database connection and environment configuration
├── docs/            # Project documentation 
├── etl/             # ETL scripts 
├── schema/          # Database schema definitions (DDL)
├── src/             # Core source code for data generation using Faker
├── tests/           # Unit tests and data validation tests
│
├── .gitignore       # Git ignore rules
├── README.md       
├── poetry.lock      
└── pyproject.toml   
```
## 🛠️ Tech Stack
- **Programming Language**: Python 3.12 
- **Data Generation**: Faker  
- **Database Systems**: PostgreSQL
- **Dependency Management**: Poetry    
- **Version Control**: Git  
## 📈 Expected Data Volume
- **brand**: 20 records  
- **category**: 10 records  
- **seller**: 25 records  
- **product**: 200 records  
- **promotion**: 10 records  
- **promotion_product**: 100 records  
- **order**: 100,000 records  
- **order_item**: 1,000,000 records   
## 🚀 Getting Started
### 1. Clone the repository
```bash
git clone <repository-url>
cd <project-name>
```
### 2. Install dependencies
```bash
poetry install
```
### 3. Run commands using Poetry
```bash 
poetry run python -m src.main
```
### 4. Configure database
Update database connection settings in the ```config/``` directory.
### 5. Generate and load data
```bash
poetry run python -m src.main
```
