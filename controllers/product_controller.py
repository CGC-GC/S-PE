from flask import render_template, session
from core.controller import Controller
from models.product_model import ProductModel
from models.category_model import CategoryModel

class ProductController(Controller):
    def view_action(self):
        product_id = self.view.params[2]  # id товара
        
        model = {
            'categories': CategoryModel.get_categories_list(),
            'subcategories': CategoryModel.get_subcategories_list(),
            'product': ProductModel.get_product_by_id(product_id)
        }
        
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Товар', model=model) 