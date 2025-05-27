from core.view import View
from models.user_model import UserModel

class Controller:
    def __init__(self, route):
        self.route = route
        self.view = View(route)
    
    def check_admin(self):
        # Проверяем авторизирован ли пользователь
        if 'id' in session:
            user_id = session['id']
        else:
            return redirect(url_for('user.login'))
            
        # Получаем информацию о текущем пользователе
        user = UserModel.get_user_by_id(user_id)
        
        # Если роль текущего пользователя "admin", пускаем его в админпанель
        if user and user['role'] == 'admin':
            return True
            
        # Иначе завершаем работу с сообщением об закрытом доступе
        return False 