from datetime import datetime
from core.database import db

class OrderModel:
    @staticmethod
    def save(user_name, user_phone, user_comment, user_id, products):
        error = False
        
        if products:
            for product_id, quantity in products.items():
                product = db.session.query(Product).filter_by(id=product_id).first()
                if product:
                    price = float(product.price)
                    sum_total = quantity * price
                    
                    order = ProductOrder(
                        user_name=user_name,
                        user_phone=user_phone,
                        user_comment=user_comment,
                        user_id=user_id,
                        product_id=product_id,
                        quantity_products=quantity,
                        sum=sum_total,
                        order_date=datetime.now()
                    )
                    db.session.add(order)
                    
            try:
                db.session.commit()
            except:
                db.session.rollback()
                error = True
                
        return error
    
    @staticmethod
    def get_history_orders(user_id):
        return db.session.query(
            ProductOrder.order_date,
            Product.name,
            ProductOrder.quantity_products,
            Product.price,
            Product.image
        ).join(Product, ProductOrder.product_id == Product.id)\
         .filter(ProductOrder.user_id == user_id)\
         .order_by(ProductOrder.order_date.desc())\
         .all()
    
    @staticmethod
    def get_sum_by_month_order():
        # Получаем минимальный год
        min_year = db.session.query(
            db.func.min(db.extract('year', ProductOrder.order_date))
        ).scalar()
        
        if not min_year:
            return False
            
        # Получаем максимальный год
        max_year = db.session.query(
            db.func.max(db.extract('year', ProductOrder.order_date))
        ).scalar()
        
        sums_by_month = {}
        current_year = min_year
        
        while current_year <= max_year:
            # Получаем месяцы текущего года
            months = db.session.query(
                db.func.distinct(db.extract('month', ProductOrder.order_date))
            ).filter(
                db.extract('year', ProductOrder.order_date) == current_year
            ).all()
            
            for month in months:
                month_sum = db.session.query(
                    db.func.sum(ProductOrder.sum)
                ).filter(
                    db.extract('year', ProductOrder.order_date) == current_year,
                    db.extract('month', ProductOrder.order_date) == month[0]
                ).scalar()
                
                if month_sum:
                    sums_by_month[f"{current_year}/{month[0]}"] = float(month_sum)
                    
            current_year += 1
            
        return sums_by_month if sums_by_month else False 