from flask import Flask, request, render_template_string

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template_string('''
    <html>
    <head>
        <title>موقعي الاحترافي</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #F7F7F7; }
            header { background-color: #1C1C1B; padding: 5px; display: flex; align-items: center; justify-content: space-between; }
            .logo { display: flex; align-items: center; }
            .logo img { width: 50px; margin-right: 10px; }
            .logo h1 { color: white; margin: 0; font-size: 35px; font-family: "Playfair Display", serif; margin-left: 60px; /* يحدد بعده عن الحافة اليمنى */
}
            nav a { color: white; padding: 20px 50px; text-decoration: none; margin: 0 40px; background-color: #3F4F44; border-radius: 5px; }
            nav a:hover { background-color: #1C1C1B; }
            .content { text-align: center; margin-top: 50px; }
            .search-box { margin-top: 20px; }
            .search-box input { padding: 10px; width: 250px; border-radius: 5px; border: 1px solid #ddd; }
            .search-box button { padding: 10px; background-color: #3F4F44; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .search-box button:hover { background-color: #1C1C1B; }
                                  
            .search-box {
    text-align: right;
    display: flex;
    justify-content: flex-end;
    max-width: 70%; /* يمنع الامتداد الزائد */
    margin-right: 60px; /* يحدد بعده عن الحافة اليمنى */
}
        
action a { color: white; padding: 10px 50px; text-decoration: none; margin: 0 40px; background-color: #3F4F44; border-radius: 5px; }
            nav a:hover { background-color: #1C1C1B; }
/* تنسيق الأزرار التي تحت الصورة */
nav {
    margin-top: 30px; /* إضافة مسافة بين الصورة والأزرار */
    text-align: center;
}

nav a {
    padding: 15px 30px;
    background-color: #3F4F44;
    color: white;
    text-decoration: none;
    margin: 10px;
    border-radius: 5px;
    font-size: 18px;
}

nav a:hover {
    background-color: #1C1C1B;
}
                                  
        

        </style>
    </head>
    <body>
        <header>
           <div class="logo">
                <h1>Dress ID</h1>
            </div>
            
            <action>
                <a href="/store">المتجر</a>
                <a href="/services">الخدمات</a>
                <a href="/contact">اتصل بنا</a>
            </action>
                         <div class="search-box">
                <form action="/search" method="get">
                    <input type="text" name="query" placeholder="ابحث عن منتج...">
                    <button type="submit">بحث</button>
                </form>
            </div>
        </header>
        <div class="content">
            <h2>أهلاً بكِ سيدتي </h2>
            <p>لِتكوني الأجمل في مناسبتكِ !</p>
        

            <img src="https://tinypic.host/images/2025/03/21/485072341_1043538650944827_2361027716447636987_n.png"style="border-radius: 15px; width: 500px; height: 300px;">
                                  
              <nav>
                <a href="/" >فساتين محجبات </a>
                <a href="/store">فساتين سهرة </a>
                <a href="/services">شنط مناسبات</a>
                <a href="/contact">كماليات</a>
            </nav>
        </div>
    </body>
    </html>
    ''')

# صفحة المتجر
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
        </style>
    </head>
    <body>
        <header>
            <div class="logo">
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
                    <img src="https://tinypic.host/images/2025/03/21/485072341_1043538650944827_2361027716447636987_n.png" alt="منتج 1">
                    <h3>فستان أنيق</h3>
                    <p>السعر: $50</p>
                     <a href="#" class="buy-btn">عرض التفاصيل </a>
                    <a href="#" class="buy-btn">شراء الآن</a>
                    
                </div>
                <div class="product">
                    <img src="https://via.placeholder.com/150" alt="منتج 2">
                    <h3>بدلة رجالية</h3>
                    <p>السعر: $80</p>
                     <a href="#" class="buy-btn">عرض التفاصيل </a>
                    <a href="#" class="buy-btn">شراء الآن</a>
                </div>
                <div class="product">
                    <img src="https://via.placeholder.com/150" alt="منتج 3">
                    <h3>حذاء فاخر</h3>
                    <p>السعر: $60</p>
                     <a href="#" class="buy-btn">عرض التفاصيل </a>
                    <a href="#" class="buy-btn">شراء الآن</a>
                    
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

# صفحة البحث
@app.route('/search')
def search():
    query = request.args.get('query', '')
    return f"<h1>نتائج البحث عن: {query}</h1>"

# صفحات أخرى
@app.route('/services')
def services():
    return "<h1>صفحة الخدمات</h1>"

@app.route('/contact')
def contact():
    return "<h1>اتصل بنا</h1>"

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)
