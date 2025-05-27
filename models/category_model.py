from core.database import db

class CategoryModel:
    @staticmethod
    def get_categories_list():
        return db.session.query(Category)\
            .filter_by(status=1)\
            .order_by(Category.sort_order.asc())\
            .all()
    
    @staticmethod
    def get_categories_list_admin():
        return db.session.query(Category)\
            .order_by(Category.sort_order.asc())\
            .all()
    
    @staticmethod
    def get_subcategories_list():
        return db.session.query(Subcategory)\
            .order_by(Subcategory.category_id.asc())\
            .all() 