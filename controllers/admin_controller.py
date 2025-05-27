from flask import render_template
from core.controller import Controller

class AdminController(Controller):
    def index_action(self):
        var = self.check_admin()  # Проверка доступа
        model = ''
        
        if var:
            template = 'layouts/admin_tpl.html'
        else:
            template = 'layouts/main_authorized_tpl.html'
            
        return render_template(template, title='Админпанель', model=model, var=var) 