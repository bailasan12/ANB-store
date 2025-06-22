# صفحة المتجر
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/store')
def store():
    return render_template_string('''
    <html>
    <head>
        <title>المتجر</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }
            header { background-color: #1abc9c; padding: 15px; display: flex; align-items: center; justify-content: space-between; }
            .logo { display: flex; align-items: center; }
            .logo img { width: 50px; margin-right: 10px; }
            .logo h1 { color: white; margin: 0; font-size: 24px; }
            nav a { color: white; padding: 10px 20px; text-decoration: none; margin: 0 5px; background-color: #16a085; border-radius: 5px; }
            nav a:hover { background-color: #1abc9c; }
            .content { text-align: center; margin-top: 50px; }
            .store-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 30px; }
            .product { border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; width: 200px; background: #fff; }
            .product img { width: 100%; border-radius: 10px; }
            .buy-btn { display: block; margin-top: 10px; background-color: #16a085; color: white; padding: 10px; border: none; border-radius: 5px; text-decoration: none; }
            .buy-btn:hover { background-color: #1abc9c; }
            .details-btn { display: block; margin-top: 10px; background-color: #f39c12; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
            .details-btn:hover { background-color: #e67e22; }
        </style>
    </head>
    <body>
        <header>
            <div class="logo">
                <img src="https://via.placeholder.com/50" alt="شعار">
                <h1>Dress ID</h1>
            </div>
            <nav>
                <a href="/">الصفحة الرئيسية</a>
                <a href="/store">المتجر</a>
                <a href="/services">الخدمات</a>
                <a href="/contact">اتصل بنا</a>
            </nav>
        </header>
        <div class="content">
            <h2>المتجر</h2>
            <p>تصفح أحدث منتجاتنا المميزة!</p>
            <div class="store-container">
                <div class="product">
                    <img src="https://via.placeholder.com/150" alt="منتج 1">
                    <h3>فستان أنيق</h3>
                    <p>السعر: $50</p>
                    <a href="#" class="buy-btn">شراء الآن</a>
                    <button class="details-btn" onclick="alert('تفاصيل عن الفستان الأنيق...')">إظهار التفاصيل</button>
                </div>
                <div class="product">
                    <img src="https://via.placeholder.com/150" alt="منتج 2">
                    <h3>بدلة رجالية</h3>
                    <p>السعر: $80</p>
                    <a href="#" class="buy-btn">شراء الآن</a>
                    <button class="details-btn" onclick="alert('تفاصيل عن البدلة الرجالية...')">إظهار التفاصيل</button>
                </div>
                <div class="product">
                    <img src="https://via.placeholder.com/150" alt="منتج 3">
                    <h3>حذاء فاخر</h3>
                    <p>السعر: $60</p>
                    <a href="#" class="buy-btn">شراء الآن</a>
                    <button class="details-btn" onclick="alert('تفاصيل عن الحذاء الفاخر...')">إظهار التفاصيل</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')
if __name__ == '__main__':
    app.run(debug=True)
