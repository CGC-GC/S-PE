from flask import render_template, redirect, url_for, request, session
from core.controller import Controller
from models.category_model import CategoryModel
from models.product_model import ProductModel
from models.user_model import UserModel
from models.order_model import OrderModel
from lib.cart import Cart

class CartController(Controller):
    def index_action(self):
        model = {
            'categories': CategoryModel.get_categories_list(),
            'subcategories': CategoryModel.get_subcategories_list(),
            'products': ''
        }
        
        # Получаем массив: ключ - id товара, значение - количество товаров
        products_in_cart = Cart.get_products()
        
        # Если в корзине есть товары, получаем полную информацию о товарах для списка
        if products_in_cart:
            # Получаем массив только с идентификаторами товаров
            products_ids = list(products_in_cart.keys())
            # Получаем массив с полной информацией о необходимых товарах
            model['products'] = ProductModel.get_products_by_ids(products_ids)
            
        # Получаем общую стоимость товаров
        model['totalPrice'] = Cart.get_total_price(model['products'])
        
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Корзина', model=model, var=products_in_cart)
    
    def add_action(self):
        # Добавляем товар в корзину
        product_id = self.route[2]
        Cart.add_product(product_id)
        
        # Возвращаем пользователя на страницу с которой он пришел
        return redirect(request.referrer)
    
    def delete_action(self):
        # Удаляем заданный товар из корзины
        product_id = self.route[2]
        Cart.delete_product(product_id)
        
        # Возвращаем пользователя в корзину
        return redirect(url_for('cart.index'))
    
    def checkout_action(self):
        model = {
            'categories': CategoryModel.get_categories_list(),
            'subcategories': CategoryModel.get_subcategories_list()
        }
        
        # Получаем данные из корзины
        products_in_cart = Cart.get_products()
        var = {
            'userName': '',
            'userPhone': '',
            'userComment': '',
            'errorUserName': '',
            'errorUserPhone': '',
            'orderAccepted': False,
            'result': False
        }
        
        if products_in_cart:
            # Находим общую стоимость
            products_ids = list(products_in_cart.keys())
            products = ProductModel.get_products_by_ids(products_ids)
            var['totalPrice'] = Cart.get_total_price(products)
            # Количество товаров
            var['totalQuantity'] = Cart.count_items()
        
        # Проверяем является авторизован ли пользователь
        if session.get('auth'):
            user_id = session['id']
            user = UserModel.get_user_by_id(user_id)
            var['userName'] = user['name']
        else:
            return redirect(url_for('user.login'))
        
        if request.method == 'POST':
            var['userName'] = request.form.get('userName', '')
            var['userPhone'] = request.form.get('userPhone', '')
            var['userComment'] = request.form.get('userComment', '')
            
            if not UserModel.check_name(var['userName']):
                var['errorUserName'] = 'Неправильное имя'
            if len(var['userPhone']) >= 10:
                var['errorUserPhone'] = 'Неправильный телефон'
            
            # Если нет ошибок
            if not var['errorUserName'] and not var['errorUserPhone']:
                error = OrderModel.save(
                    var['userName'],
                    var['userPhone'],
                    var['userComment'],
                    user_id,
                    products_in_cart
                )
                
                # Если заказ успешно сохранен
                if not error:
                    admin_email = 'manager@mail.ru'
                    message = f"Поступил заказ от клиента: {var['userName']} с идентификатором {user_id}"
                    subject = 'Новый заказ!'
                    
                    # Отправка email администратору
                    send_mail(subject, message, admin_email)
                    
                    var['orderAccepted'] = True
                    Cart.clear()
        
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Оформление заказа', model=model, var=var) 