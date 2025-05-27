import os
from flask import current_app
from core.database import db

class ProductModel:
    LATEST = 6
    RECOMMENDED = 6
    ITEMS_PER_PAGE = 3
    PRODUCTS_PER_PAGE = 16
    
    count_items = 0
    count_products = 0
    
    @staticmethod
    def get_latest_products(count=LATEST):
        return db.session.query(Product)\
            .filter_by(status=1)\
            .order_by(Product.id.desc())\
            .limit(count)\
            .all()
    
    @staticmethod
    def get_recommended_products(count=RECOMMENDED):
        return db.session.query(Product)\
            .filter_by(is_recommended=1)\
            .order_by(Product.id.desc())\
            .limit(count)\
            .all()
    
    @staticmethod
    def get_product_by_id(product_id):
        return db.session.query(
            Product.id,
            Product.name,
            Product.code,
            Product.price,
            Product.brand,
            Product.image,
            Product.description,
            Product.is_new,
            Category.name.label('cat_name'),
            Subcategory.name.label('subcat_name')
        ).join(Category, Product.category_id == Category.id)\
         .join(Subcategory, Product.subcategory_id == Subcategory.id)\
         .filter(Product.id == product_id)\
         .first()
    
    @staticmethod
    def get_products_by_ids(ids_array):
        return db.session.query(Product)\
            .filter(
                Product.status == 1,
                Product.id.in_(ids_array)
            ).all()
    
    @staticmethod
    def get_subcategory_products(subcategory_id):
        # Получаем количество товаров
        ProductModel.count_items = db.session.query(Product)\
            .filter_by(
                status=1,
                subcategory_id=subcategory_id
            ).count()
            
        page = request.args.get('pagin', 1, type=int)
        per_page = ProductModel.ITEMS_PER_PAGE
        
        return db.session.query(
            Product.id,
            Product.name,
            Product.price,
            Product.image,
            Product.is_new,
            Category.name.label('cat_name'),
            Subcategory.name.label('subcat_name')
        ).join(Category, Product.category_id == Category.id)\
         .join(Subcategory, Product.subcategory_id == Subcategory.id)\
         .filter(
             Product.status == 1,
             Product.subcategory_id == subcategory_id
         ).order_by(Product.id.desc())\
         .paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_products_list():
        # Получаем общее количество товаров
        ProductModel.count_products = db.session.query(Product).count()
        
        page = request.args.get('pagin', 1, type=int)
        per_page = ProductModel.PRODUCTS_PER_PAGE
        
        return db.session.query(Product)\
            .order_by(Product.id.asc())\
            .paginate(page=page, per_page=per_page)
    
    @staticmethod
    def add_product_by_admin():
        options = {
            'name': '',
            'code': '',
            'price': '',
            'brand': '',
            'description': ''
        }
        
        if request.method == 'POST':
            options['name'] = request.form.get('name', '')
            options['code'] = request.form.get('code', '')
            options['price'] = request.form.get('price', '')
            options['category_id'] = request.form.get('category_id')
            options['subcategory_id'] = request.form.get('subcategory_id', 0)
            options['brand'] = request.form.get('brand', '')
            options['description'] = request.form.get('description', '')
            
            error = any(not value for value in options.values())
            options['error'] = error
            
            options['is_new'] = request.form.get('is_new')
            options['is_recommended'] = request.form.get('is_recommended')
            options['status'] = request.form.get('status')
            
            if not error:
                # Проверяем, не занят ли артикул
                existing_product = db.session.query(Product)\
                    .filter_by(code=options['code'])\
                    .first()
                    
                if not existing_product:
                    product = Product(
                        name=options['name'],
                        category_id=options['category_id'],
                        subcategory_id=options['subcategory_id'],
                        code=options['code'],
                        price=options['price'],
                        brand=options['brand'],
                        image='/public/images/no-image.png',
                        description=options['description'],
                        is_new=options['is_new'],
                        is_recommended=options['is_recommended'],
                        status=options['status']
                    )
                    db.session.add(product)
                    db.session.commit()
                    
                    # Обработка загруженного изображения
                    if 'image' in request.files:
                        file = request.files['image']
                        if file and file.filename:
                            product_id = product.id
                            filename = f"{product_id}.jpg"
                            file_path = os.path.join(
                                current_app.config['UPLOAD_FOLDER'],
                                filename
                            )
                            file.save(file_path)
                            
                            product.image = f"/upload/{filename}"
                            db.session.commit()
                    
                    options['product_added'] = '<p class="good">Товар добавлен в БАЗУ ДАННЫХ</p>'
                else:
                    options['product_added'] = '<p class="error">Такой артикул имеется в БАЗЕ ДАННЫХ</p>'
                    
        return options
    
    @staticmethod
    def update_product_by_admin(product_id):
        if request.method != 'POST':
            return db.session.query(
                Product.name,
                Product.code,
                Product.price,
                Product.brand,
                Product.image,
                Product.description,
                Product.is_new,
                Product.is_recommended,
                Product.status,
                Category.name.label('cat_name'),
                Subcategory.name.label('subcat_name')
            ).join(Category, Product.category_id == Category.id)\
             .join(Subcategory, Product.subcategory_id == Subcategory.id)\
             .filter(Product.id == product_id)\
             .first()
             
        options = {
            'name': request.form.get('name', ''),
            'code': request.form.get('code', ''),
            'price': request.form.get('price', ''),
            'category_id': request.form.get('category_id'),
            'subcategory_id': request.form.get('subcategory_id', 0),
            'brand': request.form.get('brand', ''),
            'description': request.form.get('description', '')
        }
        
        # Получаем текущие данные продукта
        product_data = db.session.query(
            Product.image,
            Category.name.label('cat_name'),
            Subcategory.name.label('subcat_name')
        ).join(Category, Product.category_id == Category.id)\
         .join(Subcategory, Product.subcategory_id == Subcategory.id)\
         .filter(Product.id == product_id)\
         .first()
         
        options['cat_name'] = product_data.cat_name
        options['subcat_name'] = product_data.subcat_name
        options['image'] = product_data.image
        
        error = any(not value for value in options.values())
        options['error'] = error
        
        options['is_new'] = request.form.get('is_new')
        options['is_recommended'] = request.form.get('is_recommended')
        options['status'] = request.form.get('status')
        
        if not error:
            # Проверяем, не занят ли артикул
            existing_product = db.session.query(Product)\
                .filter(
                    Product.code == options['code'],
                    Product.id != product_id
                ).first()
                
            if not existing_product:
                product = ProductModel.get_product_by_id(product_id)
                
                # Обработка загруженного изображения
                if 'image' in request.files:
                    file = request.files['image']
                    if file and file.filename:
                        filename = f"{product_id}.jpg"
                        file_path = os.path.join(
                            current_app.config['UPLOAD_FOLDER'],
                            filename
                        )
                        file.save(file_path)
                        options['image'] = f"/upload/{filename}"
                
                # Обновляем данные продукта
                product.name = options['name']
                product.category_id = options['category_id']
                product.subcategory_id = options['subcategory_id']
                product.code = options['code']
                product.price = options['price']
                product.brand = options['brand']
                product.image = options['image']
                product.description = options['description']
                product.is_new = options['is_new']
                product.is_recommended = options['is_recommended']
                product.status = options['status']
                
                db.session.commit()
                options['product_added'] = '<p class="good">Товар изменен в БАЗЕ ДАННЫХ</p>'
            else:
                options['product_added'] = '<p class="error">Такой артикул имеется в БАЗЕ ДАННЫХ</p>'
                
        return options
    
    @staticmethod
    def delete_product_by_admin(product_id):
        product = ProductModel.get_product_by_id(product_id)
        if product:
            db.session.delete(product)
            db.session.commit() 