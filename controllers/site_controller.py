from flask import render_template, session
from core.controller import Controller

class SiteController(Controller):
    def blog_action(self):
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Блог')
    
    def about_action(self):
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='О магазине')
    
    def contact_action(self):
        template = 'layouts/main_authorized_tpl.html' if session.get('auth') else 'layouts/main_tpl.html'
        return render_template(template, title='Контакты') 