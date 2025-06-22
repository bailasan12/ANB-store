from pywebio.input import *
from pywebio import *
from pywebio.output import *
from pywebio.session import go_app
from pywebio import start_server
from pywebio import config
# دالة لإظهار الهيدر المحسن المتجاوب في كل الصفحات
def show_header():
    put_html("""
    <style>
        body { text-align: center; direction: rtl; font-family: 'Cairo', sans-serif; background-color: #F5F5F5; margin: 0; }

        /* تصميم الهيدر */
        .navbar {
            background-color: #541212; display: flex;
            align-items: center; justify-content: center; position: fixed;
            top: 0; width: 100%; z-index: 1500;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            padding: 15px 0;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .navbar button {
            background-color: transparent; border: 2px solid white; color: white;
            font-size: 18px; padding: 12px 20px; margin: 5px;
            cursor: pointer; transition: all 0.3s ease; font-weight: bold;
            border-radius: 10px; text-transform: uppercase;
        }
        
        .navbar button:hover {
            background-color: white; color: #541212; transform: scale(1.1);
        }

        /* لضبط المسافة بسبب الهيدر الثابت */
        .content { margin-top: 120px; padding: 10px; max-width: 1200px; margin-left: auto; margin-right: auto; }

        /* تصميم البطاقات */
        .feature, .team-member {
            background-color: white; border-radius: 12px; padding: 20px;
            margin: 15px auto; text-align: right; max-width: 90%;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2); transition: 0.3s;
        }
        
        .feature:hover, .team-member:hover { transform: scale(1.05); }
        
        /* تحسين التجاوب على الشاشات الصغيرة */
        @media screen and (max-width: 768px) {
            .navbar { flex-direction: column; align-items: center; width: 100%; }
            .navbar button { width: 90%; margin: 5px 0; font-size: 16px; }
            .content { margin-top: 160px; }
            .feature, .team-member { max-width: 95%; }
        }
    </style>
    """)

    # إضافة شريط التنقل بالأزرار مباشرة بداخله
    put_html("""
<div class='navbar'>
        <button onclick="location.href='/home'">🏠 الرئيسية</button>
        <button onclick="location.href='/ai'">🤖 الذكاء الاصطناعي</button>
        <button onclick="location.href='/team'">👥 فريق العمل</button>
    </div>
""")

# الصفحة الرئيسية
def home():
    clear()
    show_header()
    put_html("<div class='content'><h1>🔥 روبوت مكافحة الحرائق</h1></div>")
    put_image("https://files.fm/f/zsqk7atb49.jpg", width='70%')

    put_html("<div class='content'><h2>🔥 ميزات الروبوت</h2></div>")
    features = [
        "🚀 التنقل الذاتي: يستخدم الذكاء الاصطناعي لتحديد المسار الأمثل.",
        "🌊 نظام إطفاء متطور: مجهز بفوهة مياه قوية تصل إلى 4800 لتر/دقيقة.",
        "📷 كاميرات حرارية: يساعد في اكتشاف الحرائق حتى في الدخان الكثيف.",
        "🎮 تحكم عن بعد: يمكن تشغيله عبر جهاز تحكم لاسلكي لمسافات طويلة."
    ]
    for feature in features:
        put_html(f"<div class='feature'>{feature}</div>")

# صفحة الذكاء الاصطناعي
def ai_page():
    clear()
    show_header()
    put_html("<div class='content'><h1>🤖 الذكاء الاصطناعي في الروبوت</h1></div>")
    ai_features = [
        "📡 يستخدم مستشعرات وكاميرات ذكية لتحديد مواقع الحرائق بدقة.",
        "🚜 يتحرك تلقائيًا عبر التضاريس المختلفة للوصول إلى الحريق.",
        "💦 يضخ الماء أو الرمل حسب نوع الحريق المكتشف."
    ]
    for feature in ai_features:
        put_html(f"<div class='feature'>{feature}</div>")

# صفحة فريق العمل
def team_page():
    clear()
    show_header()
    put_html("<div class='content'><h1>👥 فريق العمل</h1></div>")
    team_members = [
        "بيلسان برابرة ",
        "مسك عزام",
        "جنى عُمر ",
        "سديل سائد"
    ]
    for member in team_members:
        put_html(f"<div class='team-member'>{member}</div>")

# تشغيل التطبيق مع تسجيل الصفحات
if __name__ == "__main__":
    start_server({"home": home, "ai": ai_page, "team": team_page}, port=5000, debug=True,host='0.0.0.0')
