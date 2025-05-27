from flask import render_template
from core.controller import Controller
from models.order_model import OrderModel

class AdminSaleController(Controller):
    def index_action(self):
        access = self.check_admin()  # Проверка доступа
        if not access:
            return 'Доступ запрещен'
            
        sum_by_month = OrderModel.get_sum_by_month_order()
        
        return render_template(
            'layouts/admin_tpl.html',
            title='Продажи',
            model=sum_by_month
        ) 