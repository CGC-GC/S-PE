import random
import string
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from core.database import db

class UserModel:
    ITEMS_PER_PAGE = 10  # количество пользователей на страницу
    count_items = 0  # количество всех пользователей в БД
    
    @staticmethod
    def auth():
        if not session.get('auth'):
            # Проверяем куки в браузере
            email = request.cookies.get('email')
            key = request.cookies.get('key')
            
            if email and key:
                user = db.session.query(User).filter_by(email=email, rend_key=key).first()
                if user:
                    session['auth'] = True
                    session['id'] = user.id
                    session['login'] = user.name
    
    @staticmethod
    def check_name(name):
        if len(name) >= 2:
            return name
        return False
    
    @staticmethod
    def check_email(email):
        if '@' in email and '.' in email:
            return email
        return False
    
    @staticmethod
    def register_user(data):
        name = data['name']
        email = data['email']
        password = generate_password_hash(data['password'])
        remember = data.get('remember', False)
        
        # Проверяем, не занят ли email
        existing_user = db.session.query(User).filter_by(email=email).first()
        if not existing_user:
            user = User(name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            
            session['auth'] = True
            session['login'] = name
            session['id'] = user.id
            
            if remember:
                random_str = UserModel._generate_random_string(8)
                response = make_response(redirect(url_for('main.index')))
                response.set_cookie('email', email, max_age=30*24*60*60)
                response.set_cookie('key', random_str, max_age=30*24*60*60)
                
                user.rend_key = random_str
                db.session.commit()
                
                return response
                
            return 'Вы успешно зарегистрированы!'
        return '<span class="error">Email занят!</span>'
    
    @staticmethod
    def check_user_data(email, password):
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['auth'] = True
            session['id'] = user.id
            session['login'] = user.name
            
            if request.form.get('remember'):
                random_str = UserModel._generate_random_string(8)
                response = make_response(redirect(url_for('main.index')))
                response.set_cookie('email', email, max_age=30*24*60*60)
                response.set_cookie('key', random_str, max_age=30*24*60*60)
                
                user.rend_key = random_str
                db.session.commit()
                
                return response
                
            return user
        return False
    
    @staticmethod
    def get_user_by_id(user_id):
        return db.session.query(User).filter_by(id=user_id).first()
    
    @staticmethod
    def update_user(data):
        name = data['name']
        email = data['email']
        password = generate_password_hash(data['password'])
        remember = data.get('remember', False)
        user_id = data['user_id']
        
        existing_user = db.session.query(User).filter_by(email=email).first()
        if not existing_user or existing_user.id == user_id:
            user = UserModel.get_user_by_id(user_id)
            user.name = name
            user.email = email
            user.password = password
            db.session.commit()
            
            session['auth'] = True
            session['login'] = name
            
            if remember:
                random_str = UserModel._generate_random_string(8)
                response = make_response(redirect(url_for('main.index')))
                response.set_cookie('email', email, max_age=30*24*60*60)
                response.set_cookie('key', random_str, max_age=30*24*60*60)
                
                user.rend_key = random_str
                db.session.commit()
                
                return response
                
            return 'Личные данные обновлены!'
        return '<span class="error">Email занят!</span>'
    
    @staticmethod
    def get_users_list(admin_id):
        UserModel.count_items = db.session.query(User).count()
        
        page = request.args.get('pagin', 1, type=int)
        per_page = UserModel.ITEMS_PER_PAGE
        
        users = db.session.query(User).filter(User.id != admin_id)\
            .order_by(User.id.asc())\
            .paginate(page=page, per_page=per_page)
            
        return users.items
    
    @staticmethod
    def user_disable(ban_id):
        user = UserModel.get_user_by_id(ban_id)
        user.ban = 'да'
        db.session.commit()
    
    @staticmethod
    def user_enable(ban_id):
        user = UserModel.get_user_by_id(ban_id)
        user.ban = 'нет'
        db.session.commit()
    
    @staticmethod
    def admin_disable(admin_id):
        user = UserModel.get_user_by_id(admin_id)
        user.role = 'user'
        db.session.commit()
    
    @staticmethod
    def admin_enable(admin_id):
        user = UserModel.get_user_by_id(admin_id)
        user.role = 'admin'
        db.session.commit()
    
    @staticmethod
    def check_ban(email):
        user = db.session.query(User).filter_by(email=email).first()
        return user and user.ban == 'да'
    
    @staticmethod
    def _generate_random_string(length=6):
        chars = string.ascii_letters + string.digits + '!=?&-+'
        return ''.join(random.choice(chars) for _ in range(length)) 