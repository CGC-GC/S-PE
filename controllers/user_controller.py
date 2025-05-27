from flask import render_template, redirect, url_for, request, session, make_response
from core.controller import Controller
from models.user_model import UserModel

class UserController(Controller):
    def __init__(self, route):
        super().__init__(route)
        self.form_params = {}
        self.remember = False
        self.error_flag = True
    
    def register_action(self):
        self.form_params = {
            'name': '',
            'email': '',
            'nameError': '',
            'emailError': '',
            'passwordErrorMatch': '',
            'passwordErrorLength': '',
            'regSuccessfully': ''
        }
        
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
            
            # Регистрация
            if self.error_flag:
                user_data = {
                    'name': self.form_params['name'],
                    'email': self.form_params['email'],
                    'password': request.form.get('password1'),
                    'remember': self.remember
                }
                self.form_params['regSuccessfully'] = UserModel.register_user(user_data)
        
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Регистрация', model='', var=self.form_params)
    
    def logout_action(self):
        # Если переменная auth из сессии не пуста и равна true
        if session.get('auth'):
            session.clear()  # Очищаем сессию
            
            # Удаляем куки авторизации
            response = make_response(redirect(url_for('main.index')))
            response.delete_cookie('email')
            response.delete_cookie('key')
            return response
            
        return redirect(url_for('main.index'))
    
    def login_action(self):
        self.form_params = {
            'userOK': '',
            'passwordErrorLength': '',
            'email': '',
            'emailError': ''
        }
        
        if request.method == 'POST':
            # Проверка: забанен или нет
            email = request.form.get('email', '')
            if UserModel.check_ban(email):
                return 'Доступ запрещен. Вы забанены'
            
            if len(request.form.get('password', '')) < 2:
                self.form_params['passwordErrorLength'] = 'Пароль должен быть не менее двух символов'
                self.error_flag = False
            
            email_check = UserModel.check_email(email)
            if email_check:
                self.form_params['email'] = email_check
            else:
                self.form_params['emailError'] = 'Не правильный email'
                self.error_flag = False
            
            if self.error_flag:
                # Проверяем существует ли пользователь
                user_data = UserModel.check_user_data(
                    self.form_params['email'],
                    request.form.get('password', '')
                )
                
                if user_data:
                    return redirect(url_for('main.index'))
                else:
                    self.form_params['userOK'] = 'Не совпал логин или пароль'
        
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Вход', model='', var=self.form_params) 