from flask import session
from models.product_model import ProductModel
from models.category_model import CategoryModel

class MainController:
    def __init__(self, view):
        self.view = view

    def home_action(self):
        model = {
            'productsList': ProductModel.get_latest_products(4),
            'recommendedList': ProductModel.get_recommended_products()
        }

        # Определяем шаблон в зависимости от авторизации
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        
        return self.view.render('Главная', model, 'main', template) 