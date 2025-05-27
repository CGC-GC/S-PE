from flask import render_template

class View:
    def __init__(self, params):
        self.params = params
        self.path = f"{self.params[0]}/{self.params[1]}_view"

    def render(self, title, model, var='', template):
        try:
            # В Flask мы используем render_template вместо прямого включения файлов
            return render_template(
                template,
                title=title,
                model=model,
                var=var,
                content=self.path
            )
        except Exception as e:
            return f'Вид не найден: {self.path}.html - {str(e)}' 