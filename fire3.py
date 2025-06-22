from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
import time


def animated_text(text, delay=1):
    put_html(f"<div class='animated-text'>{text}</div>")
    time.sleep(delay)

    put_html('<button id="navigateBtn" style="padding: 10px 20px; font-size: 30px; border: none; background-color: #CAE0BC; color:#541212 ; cursor: pointer;">Home</button>')
def main_page():
    clear()
    put_html("""
    <style>
        body { text-align: center; direction: rtl; font-family: 'Arial', sans-serif; background-color: #CAE0BC; }
         h1 { color: #541212; font-family: 'Verdana', sans-serif; }
 
        .container { padding: 20px; }
        .animated-text { font-size: 22px; color: #333; font-weight: bold; opacity: 0; transform: translateY(30px); transition: opacity 1s ease-in-out, transform 1s ease-in-out; }
        .feature, .team-member { background-color: #fff; border-radius: 10px; padding: 15px; margin: 10px auto; text-align: right; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: transform 0.3s ease; }
        .feature:hover, .team-member:hover { transform: scale(1.05); }
    </style>
    """)
    
    


    put_html("<h1> روبوت مكافحة الحرائق</h1>")

    put_image("https://files.fm/f/zsqk7atb49.jpg", width='70%')
    put_html("<div class='container'><h2>🔥 ميزات الروبوت</h2></div>")
    put_html("<div class='feature'>🚀 التنقل الذاتي: يستخدم الذكاء الاصطناعي لتحديد المسار الأمثل.</div>")
    put_html("<div class='feature'>🌊 نظام إطفاء متطور: مجهز بفوهة مياه قوية تصل إلى 4800 لتر/دقيقة.</div>")
    put_html("<div class='feature'>📷 كاميرات حرارية: يساعد في اكتشاف الحرائق حتى في الدخان الكثيف.</div>")
    put_html("<div class='feature'>🎮 تحكم عن بعد: يمكن تشغيله عبر جهاز تحكم لاسلكي لمسافات طويلة.</div>")
    put_buttons(['🔍 عرض المزيد عن الذكاء الاصطناعي'], [ai_page])

def ai_page():
    clear()
    put_html("<h1>🤖 الذكاء الاصطناعي في الروبوت</h1>")
    put_html("<div class='container'><h2>كيف يعمل الروبوت؟</h2></div>")
    put_html("<div class='feature'>📡 يستخدم مستشعرات وكاميرات ذكية لتحديد مواقع الحرائق بدقة.</div>")
    put_html("<div class='feature'>🚜 يتحرك تلقائيًا عبر التضاريس المختلفة للوصول إلى الحريق.</div>")
    put_html("<div class='feature'>💦 يضخ الماء أو الرمل حسب نوع الحريق المكتشف.</div>")
    put_html("<div class='container'><h2>👥 فريق العمل</h2></div>")
    put_html("<div class='team-member'>أحمد خالد - مهندس روبوتات</div>")
    put_html("<div class='team-member'>سارة محمد - خبيرة ذكاء اصطناعي</div>")
    put_html("<div class='team-member'>علي حسن - مبرمج أنظمة</div>")
    put_buttons(['⬅️ العودة'], [main_page])

if __name__ == "__main__":
    #start_server(main_page, port=8080, debug=True)
  #start_server(main_page, port=8080)
