from flask import render_template, redirect, url_for
from core.controller import Controller
from models.product_model import ProductModel
from models.category_model import CategoryModel
from core.pagination import Pagination

class AdminProductController(Controller):
    def index_action(self):
        access = self.check_admin()  # Проверка доступа
        if not access:
            return 'Доступ запрещен'
            
        products_list = ProductModel.get_products_list()
        items_per_page = ProductModel.PRODUCTS_PER_PAGE
        count_posts = ProductModel.count_products
        
        pagination = Pagination()
        pagination_html = pagination.show_pagination(count_posts, items_per_page)
        
        return render_template(
            'layouts/admin_tpl.html',
            title='Управление товарами',
            model=products_list,
            pagination=pagination_html
        )
    
    def create_action(self):
        access = self.check_admin()  # Проверка доступа
        if not access:
            return 'Доступ запрещен'
            
        # Получаем список категорий для выпадающего списка
        model = {
            'categories': CategoryModel.get_categories_list_admin()
        }
        
        # Добавляем товар
        model['options'] = ProductModel.add_product_by_admin()
        
        return render_template(
            'layouts/admin_tpl.html',
            title='Добавить товар',
            model=model
        )
    
    def update_action(self):
        access = self.check_admin()  # Проверка доступа
        if not access:
            return 'Доступ запрещен'
            
        # Получаем список категорий для выпадающего списка
        model = {
            'categories': CategoryModel.get_categories_list_admin()
        }
        
        # Обновляем товар
        product_id = self.route[2]
        model['options'] = ProductModel.update_product_by_admin(product_id)
        
        return render_template(
            'layouts/admin_tpl.html',
            title='Редактировать товар',
            model=model
        )
    
    def delete_action(self):
        access = self.check_admin()  # Проверка доступа
        if not access:
            return 'Доступ запрещен'
            
        # Удаляем товар
        product_id = self.route[2]
        
        if request.method == 'POST':
            ProductModel.delete_product_by_admin(product_id)
            return redirect(url_for('admin.product.index'))
            
        return render_template(
            'layouts/admin_tpl.html',
            title='Удалить товар',
            model='',
            var=product_id
        ) 