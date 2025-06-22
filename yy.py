from pywebio import start_server
from pywebio.output import put_html, clear, put_buttons,put_text
def عرض_الشريط_العلوي():
    """ دالة لإنشاء شريط التنقل بتصميم أنيق """
    clear()
    put_html("""
        <div style="position: fixed; top: 0; left: 0; width: 100%; background-color: #3A3A3A; padding: 15px 0; text-align: center; 
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); z-index: 1000;">
            <span style="color: white; font-size: 30px; font-weight: bold; font-family: Arial;">👗 Dress ID</span>
        </div>
        <div style="margin-top: 70px;"></div>  <!-- لإبعاد المحتوى عن شريط التنقل -->
    """)
    
    put_html("""
        <style>
            .nav-button {
                background-color: #F0F0D7;
                color: #3A3A3A;
                padding: 15px 25px;
                font-size: 22px;
                font-weight: bold;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                margin: 10px;
                transition: all 0.3s ease-in-out;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
            }
            .nav-button:hover {
                background-color: #727D73;
                color: white;
                transform: scale(1.1);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            }
            .nav-button:active {
                transform: scale(1);
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
            }
        </style>
    """)
    
    put_buttons(
        [
            {"label": "🏠 Home", "value": "home","color": "primary", "style": "nav-button"},
            {"label": "🛒 Store", "value": "store","color": "secondary","style": "nav-button"},
            {"label": "📞 Contact Us", "value": "contact", "color": "warning", "style": "nav-button"},
        ],
        onclick=تغيير_الصفحة,
        style='text-align: center;'
    )

def تغيير_الصفحة(اسم_الصفحة):
    """ دالة لتغيير الصفحة بناءً على الزر الذي تم النقر عليه """
    if اسم_الصفحة == "home":
        الصفحة_الرئيسية()
    elif اسم_الصفحة == "store":
        صفحة_المتجر()
    elif اسم_الصفحة == "contact":
        صفحة_التواصل()

def الصفحة_الرئيسية():
    clear()
    عرض_الشريط_العلوي()
    put_html("<h1 style='text-align: center; color: #504B38;'>🏠 مرحبًا بك في Dress ID</h1>")

def صفحة_المتجر():
    clear()
    عرض_الشريط_العلوي()
    put_html("<h1 style='text-align: center; color: #727D73;'>🛒 متجر Dress ID</h1>")

def صفحة_التواصل():
    clear()
    عرض_الشريط_العلوي()
    put_html("<h1 style='text-align: center; color: #F03A47;'>📞 تواصل معنا</h1>")

#def home():

    #صفحة "عن المتجر"
   #put_html("<h1>عن متجرنا الإلكتروني</h1>")
    #put_text("نحن متجر إلكتروني متخصص في بيع أفضل المنتجات عبر الإنترنت. نحن نقدم منتجات عالية الجودة بأسعار منافسة.")
    #put_buttons(["العودة إلى الصفحة الرئيسية"], onclick=lambda: start_server(button_action))

# تشغيل التطبيق
start_server(الصفحة_الرئيسية, port=8080, debug=True)
