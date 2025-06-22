from flask import Flask, request, render_template_string

app = Flask(__name__)

header_template = '''
    <header>
        <div class="logo">
            <img src="https://via.placeholder.com/50" alt="شعار المتجر">
            <h1>Dress ID</h1>
        </div>
        <nav>
            <a href="/">الصفحة الرئيسية</a>
            <a href="/store">المتجر</a>
            <a href="/services">الخدمات</a>
            <a href="/contact">اتصل بنا</a>
        </nav>
    </header>
'''

@app.route('/')
def home():
    return render_template_string(f'''
    <html>
    <head>
        <title>متجر الفساتين</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f9f9f9; }}
            header {{ background-color: #d63384; padding: 15px; display: flex; align-items: center; justify-content: space-between; position: fixed; width: 100%; top: 0; left: 0; z-index: 1000; }}
            .logo {{ display: flex; align-items: center; }}
            .logo img {{ width: 50px; margin-right: 10px; border-radius: 50%; }}
            .logo h1 {{ color: white; margin: 0; font-size: 24px; }}
            nav {{ display: flex; gap: 15px; }}
            nav a {{ color: white; padding: 10px 20px; text-decoration: none; background: #c2185b; border-radius: 5px; font-size: 16px; transition: 0.3s; }}
            nav a:hover {{ background-color: #e91e63; }}
            .banner {{ text-align: center; padding: 100px 20px 50px; margin-top: 70px; background: url('https://source.unsplash.com/1600x600/?dress,fashion') no-repeat center center/cover; color: white; }}
            .banner h2 {{ font-size: 36px; margin: 0; }}
            .banner p {{ font-size: 18px; margin-top: 10px; }}
        </style>
    </head>
    <body>
        {header_template}
        <div class="banner">
            <h2>أجمل الفساتين لأجمل اللحظات</h2>
            <p>تسوقي الآن واكتشفي أحدث الصيحات</p>
        </div>
    </body>
    </html>
    ''')

@app.route('/store')
def store():
    return render_template_string(f'''
    <html>
    <head>
        <title>المتجر</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f9f9f9; }}
            .store-section {{ text-align: center; margin-top: 100px; }}
        </style>
    </head>
    <body>
        {header_template}
        <div class="store-section">
            <h2>أحدث الفساتين</h2>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
