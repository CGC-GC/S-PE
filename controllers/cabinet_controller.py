from flask import render_template, session
from core.controller import Controller
from models.user_model import UserModel
from models.order_model import OrderModel

class CabinetController(Controller):
    def __init__(self, route):
        super().__init__(route)
        self.form_params = {}
        self.remember = False
        self.error_flag = True
    
    def index_action(self):
        template = 'layouts/main_authorized_tpl.html'
        model = ''
        var = ''
        return render_template(template, title='Кабинет', model=model, var=var)
    
    def edit_action(self):
        self.form_params = {
            'name': '',
            'email': '',
            'nameError': '',
            'emailError': '',
            'passwordErrorMatch': '',
            'passwordErrorLength': '',
            'regSuccessfully': ''
        }
        
        # Заносим данные в форму
        user_id = session['id']
        user = UserModel.get_user_by_id(user_id)
        self.form_params['name'] = user['name']
        self.form_params['email'] = user['email']
        
        if request.method == 'POST':
            # Получаем данные из формы
            result_check = UserModel.check_name(request.form.get('name', ''))
            if result_check:
                self.form_params['name'] = result_check
            else:
                self.form_params['nameError'] = 'Логин должен быть не менее 2-х символов'
                self.error_flag = False
            
            email_check = UserModel.check_email(request.form.get('email', ''))
            if email_check:
                self.form_params['email'] = email_check
            else:
                self.form_params['emailError'] = 'Не правильный email'
                self.error_flag = False
            
            if request.form.get('password1') != request.form.get('password2'):
                self.form_params['passwordErrorMatch'] = 'Не совпадают пароли'
                self.error_flag = False
            
            if len(request.form.get('password1', '')) < 2 or len(request.form.get('password2', '')) < 2:
                self.form_params['passwordErrorLength'] = 'Пароль должен быть не менее двух символов'
                self.error_flag = False
            
            if request.form.get('remember') == '1':
                self.remember = True
            
            # Изменение личных данных
            if self.error_flag:
                user_data = {
                    'name': self.form_params['name'],
                    'email': self.form_params['email'],
                    'password': request.form.get('password1'),
                    'remember': self.remember,
                    'user_id': user_id
                }
                self.form_params['regSuccessfully'] = UserModel.update_user(user_data)
        
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Личные данные', model='', var=self.form_params)
    
    def history_action(self):
        user_id = session['id']
        model = OrderModel.get_history_orders(user_id)
        
        template = 'layouts/main_authorized_tpl.html'
        return render_template(template, title='История покупок', model=model) 