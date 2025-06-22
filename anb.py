from flask import Flask, render_template_string, redirect, url_for, session, request, jsonify, render_template
from waitress import serve
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

if not os.path.exists("orders.txt"):
    with open("orders.txt", "w", encoding="utf-8") as f:
        f.write("")

app = Flask(__name__)
app.secret_key = 'secret123'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'database.db')


@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Font Awesome CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700&display=swap" rel="stylesheet">  <meta charset="UTF-8">
  <title>الرئيسية - متجري</title>
  <style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

   body, button, input, select, textarea {
      font-family: 'Cairo', sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f1f1f1;
        overflow-x: hidden; /* يمنع أي تمرير أفقي */
    }

    header {
      background-color: #f1f1f2;
      box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
      color: #51122F;
      padding: 15px 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .header-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
    }

    .logo {
      font-size: 28px;
      font-weight: bold;
      color: #51122F;
    }

    .search-form {
      display: flex;
      align-items: center;
      background-color: #fff;
      padding: 5px 10px;
      border-radius: 20px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      margin: 0 20px;
    }

    .search-form i {
      color: #888;
      margin-left: 8px;
      font-size: 16px;
    }

    .search-form input[type="text"] {
      padding: 8px 15px;
      border: none;
      border-radius: 20px;
      font-size: 16px;
      outline: none;
      width: 200px;
      background: transparent;
      color: #333;
    }

    nav a {
      color: #51122F;
      margin: 0 15px;
      text-decoration: none;
      font-size: 18px;
    }

    nav a:hover {
      text-decoration: underline;
    }

    .banner {
      background-image: url('https://i.postimg.cc/SR2vtpPk/Untitled-3.png');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      height: 400px;
      display: flex;
      justify-content: center;
      align-items: center;
      color: white;
      text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8);
      font-size: 40px;
      font-weight: bold;
      text-align: center;
      padding: 0 20px;
      transition: background 0.5s ease;
    }

    .banner:hover {
      background: rgba(0, 0, 0, 0.5);
    }

    .sections {
      text-align: center;
      margin: 50px 20px;
    }

    .sections button {
      padding: 15px 30px;
      margin: 20px;
      font-size: 18px;
      background-color: #51122F;
      color: white;
      border: none;
      border-radius: 25px;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .sections button:hover {
      transform: scale(1.05);
    }

    .welcome {
      text-align: center;
      margin: 40px 20px;
      font-size: 24px;
      color: #444;
    }

.fa, .fas, .far, .fal {
  font-family: "Font Awesome 6 Free" !important;
  font-weight: 900;
}

.fab {
  font-family: "Font Awesome 6 Brands" !important;
  font-weight: 400; /* أو  normal */
}
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }

  .logo {
    text-align: center;
    width: 100%;
    font-size: 22px;
  }

  .search-form {
    width: 100%;
    justify-content: center;
  }

  .search-form input[type="text"] {
    width: 100%;
  }

  nav {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    width: 100%;
    gap: 10px;
  }

  nav a {
    font-size: 20px;
  }
}

  .sections form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .sections button {
    width: 80%;
    max-width: 300px;
    margin: 10px auto;
  }

  .banner {
    font-size: 24px;
    height: 250px;
    padding: 0 10px;
  }

  .welcome {
    font-size: 18px;
    padding: 0 10px;
  }

  footer div {
    align-items: center !important;
    text-align: center !important;
  }

  footer a {
    margin: 0 10px;
  }
}

  </style>
</head>
<body>

  <header>
    <div class="header-container">
      <div class="logo">ANB store</div>
<form class="search-form" onsubmit="searchRedirect(event)">
  <i class="fas fa-search"></i>
  <input type="text" id="searchInput" name="q" placeholder="ابحث عن منتج...">
</form>

      <nav>
        <a href="/" title="الرئيسية"><i class="fas fa-home"></i></a>
        <a href="/cart" title="السلة"><i class="fas fa-shopping-cart"></i></a>
        <a href="/favorites" title=" المفضلة"><i class="fas fa-heart"></i></a>

      </nav>
    </div>
  </header>

  <div class="banner">
    مرحباً بك في عالم التسوق!
  </div>

  <div class="sections">
    <form action="/products" method="get">
      <button name="section" value="clothes">هوديز</button>
      <button name="section" value="couples">هوديز كابلز</button>
      <button name="section" value="T-SHIRT">بلايز صيفي</button>
      <button name="section" value="orood">عروضنا !</button>
    </form>
  </div>

  <div class="welcome">
    يسعدنا تواجدك معنا، اكتشف تشكيلتنا الواسعة من المنتجات المميزة!
  </div>

<script>
  function searchRedirect(event) {
    event.preventDefault(); // يمنع إعادة تحميل الصفحة

    const query = document.getElementById("searchInput").value;
    if (query.trim() !== "") {
      window.location.href = "/search?q=" + encodeURIComponent(query);
    }
  }
</script>

  <footer id="footer" style="
  position: relative; /* عادي */
  width: 100%;
  background-color: #51122F;
  padding: 15px 20px;
  color: white;
  font-family: 'Cairo', sans-serif;
  box-shadow: 0 -4px 15px rgba(81, 18, 47, 0.5);
  opacity: 0;  /* مخفي في البداية */
  transition: opacity 0.5s ease;
">
  <div style="
    max-width: 1200px;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: right;
  ">
    <h3 style="margin-bottom: 8px; font-size: 18px;"> تواصل معنا</h3>

    <a href="https://wa.me/972599663279" target="_blank"
       style="
         background-color: white;
         color: #51122F;
         padding: 8px 20px;
         border-radius: 30px;
         font-size: 14px;
         text-decoration: none;
         margin-bottom: 12px;
         transition: transform 0.3s, box-shadow 0.3s;
         box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
       ">
      إرسال رسالة واتساب
    </a>

    <p style="margin: 8px 0 15px; font-size: 14px; color: #f4f4f4;">
      نحن متجر متخصص في بيع الهوديز والملابس بتصاميم مميزة وجودة عالية.
    </p>

    <div style="font-size: 22px; display: flex; gap: 15px;">
      <a href="https://www.instagram.com/anbstore9?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" target="_blank" title="Instagram"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-instagram"></i>
      </a>
      <a href="https://www.facebook.com/profile.php?id=100083607621116&mibextid=ZbWKwL" target="_blank" title="Facebook"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-facebook"></i>
      </a>
      <a href="https://www.tiktok.com/@anbstore9?fbclid=IwY2xjawK-tkVleHRuA2FlbQIxMABicmlkETEzR1l6YVdSM2dydUx4Zm1lAR7g6BJCqbnkGvy9JFTU6T9l0u2Kqg4EYYPPq92KMGMZ_YchKAXPuEaZ9iwtrQ_aem_DKcG3GyDqUnxEM_AIkiTNQ" target="_blank" title="TikTok"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-tiktok"></i>
      </a>
    </div>
    <p style="font-size: 12px; color: #ccc; margin-top: 20px;">
  © جميع الحقوق محفوظة - <strong>Bailasan Riyad</strong> 2025
    </p>
  </div>
</footer>

<style>
  footer a:hover {
    transform: translateY(-4px) scale(1.05);
  }
</style>

<script>
  window.addEventListener('scroll', function() {
    const footer = document.getElementById('footer');
    const scrollPosition = window.scrollY + window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;

    if (scrollPosition >= pageHeight - 100) { 
      // عندما تكون قريب من نهاية الصفحة بـ 100 بكسل
      footer.style.opacity = '1';
    } else {
      footer.style.opacity = '0';
    }
  });
</script>
</body>
</html>
""")


@app.route('/products')
#صفحة الهوديز
def products_page():
    section = request.args.get("section", "")
    pid = request.args.get("pid")  # أضف هذا السطر
    query = request.args.get("q", "").strip()
    all_products = [
        {
            "pid": "1",
            "name": "هودي 'دكتور'",
            "price": 69.99,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc81a667676.png",
            "description": "هودي دكتور"
        },
        {
            "pid": "2",
            "name": "هودي 'المهندس'",
            "price": 69.99,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_66843b0e55998.jpg",
            "description": "هودي المهندس"
        },
        {
            "pid": "3",
            "name": "هودي 'بتضلي أنتِ العنوان'",
            "price": 49.99,
            "old_price": 80,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc4a8eba036.png",
            "description": "هودي العنوان"
        },
        {
            "pid": "4",
            "name": "هودي 'معادلة التوجيهي'",
            "price": 49.99,
            "old_price": 80,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc493bd98f0.png",
            "description": "هودي توجيهي"
        },
        {
            "pid": "5",
            "name": "هودي 'الحياة مشوار'",
            "price": 59.99,
            "old_price": 80,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_66843c98479db.jpg",
            "description": "هودي الحياة"
        },
        {
            "pid": "6",
            "name": "هودي 'Why always me'",
            "price": 69.99,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc7dd71fcb5.png",
            "description": "هودي why"
        },
        {
            "pid": "7",
            "name": "هودي 'أنا ما زلت على قيد الحياة'",
            "price": 59.99,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc7e7a28d72.png",
            "description": "هودي الحياة"
        },
        {
            "pid": "8",
            "name": "هودي 'أنا عزيز الروح'",
            "price": 49.99,
            "old_price": 80,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc7c8e1646b.png",
            "description": "هودي عزيز الروح"
        },
        {
            "pid": "9",
            "name": "هودي 'فلسطين مزروعة بالقلب'",
            "price": 59.99,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc42a07fbf4.png",
            "description": "هودي فلسطين"
        },
        {
            "pid": "10",
            "name": "هودي 'الأمور تحت السيطرة'",
            "price": 59.99,
            "old_price": 80,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc7c4862ef1.png",
            "description": "هودي السيطرة"
        },
        {
            "pid": "11",
            "name": "توم & جيري",
            "price": 139.99,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc7b5b607f9.png",
            "description": "هودي زوجي بتصميم توم وجيري"
        },
        {
            "pid": "12",
            "name": "تاريخ مميز باللاتيني",
            "price": 119.99,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_66844047797b4.jpg",
            "description": "هودي تاريخ مميز"
        },
        {
            "pid": "13",
            "name": "لك جناح و لي جناح",
            "price": 129.99,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_66843f625e9e4.jpg",
            "description": "هودي جناح"
        },
        {
            "pid": "14",
            "name": "إلى متى يا لوز",
            "price": 139.99,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_66843fcd06af6.jpg",
            "description": "هودي لوز"
        },
        {
            "pid": "15",
            "name": "القلب و التاريخ",
            "price": 129.99,
            "image":
            "https://images.cdn-files-a.com/uploads/6243106/400_65fc46647bcc2.png",
            "description": "هودي قلب"
        },
        {
            "pid": "16",
            "name": "تحقق ما كان بالأمس حلماً",
            "price": 49.99,
            "old_price": 70,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_6684418364991.jpg",
            "description": "هودي حلم"
        },
        {
            "pid": "17",
            "name": "cristiano",
            "price": 44.99,
            "old_price": 70,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_668441cae61ae.jpg",
            "description": "هودي كريستيانو"
        },
        {
            "pid": "18",
            "name": "درسنا لنعمرها",
            "price": 39.99,
            "old_price": 60,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_66a90c56065cd.jpg",
            "description": "هودي لنعمرها"
        },
        {
            "pid": "19",
            "name": "فكر خارج الصندوق",
            "price": 39.99,
            "old_price": 60,
            "image":
            "https://files.cdn-files-a.com/uploads/6243106/400_6684411d02014.jpg",
            "description": "هودي الصندوق"
        },
    ]
    print("Query:", query)
    print("Products:", products)

    filtered_products = products
    if query:
        query_lower = query.lower()
        filtered_products = [
            p for p in all_products if query_lower in p["name"].lower()
        ]
    # ترسل للصفحة المنتجات (المفلترة أو كاملة)
    print("Section:", section)

    if section == "clothes":

        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700&display=swap" rel="stylesheet">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <meta charset="UTF-8">
        <title>الرئيسية - متجري</title>
        <style>
        body, button, input, select, textarea {
          font-family: 'Cairo', sans-serif;
          margin: 0;
          padding: 0;
          background-color: #E0E0E0; 
          overflow-x: hidden; 
        }
@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
  }

  .logo {
    text-align: center;
    width: 100%;
    font-size: 22px;
  }

  nav {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    width: 100%;
    gap: 10px;
  }

  nav a {
    font-size: 20px;
  }
}

        header {
          background-color: #f1f1f2;
          box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
          color: #51122F;
          padding: 15px 30px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }

        .logo {
          font-size: 28px;
          font-weight: bold;
          color: #51122F;
        }

        .search-form {
          display: flex;
          align-items: center;
          background-color: #fff;
          padding: 5px 10px;
          border-radius: 20px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          margin: 0 20px;
        }

        .search-form i {
          color: #888;
          margin-left: 8px;
          font-size: 16px;
        }

        .search-form input[type="text"] {
          padding: 8px 15px;
          border: none;
          border-radius: 20px;
          font-size: 16px;
          outline: none;
          width: 200px;
          background: transparent;
          color: #333;
        }

        nav a {
          color: #51122F;
          margin: 0 15px;
          text-decoration: none;
          font-size: 18px;
        }

        nav a:hover {
          text-decoration: underline;
        }
        .sections {
          text-align: center;
          margin: 50px 20px;
          color:#51122F;
        }

        .sections button {
          padding: 15px 30px;
          margin: 20px;
          font-size: 18px;
          background-color: #51122F;
          color: white;
          border: none;
          border-radius: 25px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .sections button:hover {
          transform: scale(1.05);
        }
        .price {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 10px;
          margin-top: 10px;
        }

        .old-price {
          text-decoration: line-through;
          color: #888;
          font-size: 16px;
        }

        .new-price {
          color: #b3003b;
          font-size: 20px;
          font-weight: bold;
        }

        .welcome {
          text-align: center;
          margin: 40px 20px;
          font-size: 24px;
          color: #444;
        }
        .content { text-align: center; margin-top: 50px; }
        .store-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 30px; }
        .product {   margin: 25px;border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center;  width: 300px; /* أو أي عرض تريده */
  height: 520px; /* نفس الارتفاع لكل البطاقات */ background:  #fff;  font-size: 16px;}
        .product img { width: 100%;  height: 200px; /* اضبط حسب طول الصور */
  object-fit: cover; /* يمنع الصورة من التشوه */ border-radius: 10px; }
        .buy-btn { display: block; margin-top: 10px; background-color: #51122F; color: white; padding: 10px; border: none; border-radius: 5px; text-decoration: none; }
        .buy-btn:hover { background-color:  #51122F; }   
        .sub-bar {
          background-color: #51122F;
          color: white;
          text-align: center;
          padding: 10px;
          font-size: 14px;
          margin: 0;           /* إزالة أي هامش علوي */
          border-top: 1px solid #ffffff22; /* إن أردت حدود خفيفة */
        }                                         

        .modal {
          display: none; /* تكون مخفية بالبداية */
          position: fixed; /* تبقى فوق الصفحة */
          z-index: 1000; /* فوق كل العناصر */
          left: 0; top: 0;
          width: 100%; height: 100%;
          background: rgba(0, 0, 0, 0.5); /* خلفية شفافة سوداء */

        }
    .modal-content {
      font-family: 'Cairo', sans-serif; /* خط عربي جميل */
      font-size: 20px;
      color: #333;
      font-weight: 500;
      line-height: 1.6;
      text-align: center;
      margin: 10% auto;
      margin-top: 20px;
      padding: 20px;
      width: 80%;
      max-width: 500px;
      top: 5vh; /* يجعل البطاقة ترتفع لأعلى (تقدري تعدلي النسبة حسب ما تحبي) */
      border-radius: 10px;
      position: relative;
      background: white;
      max-height: 90vh; /* لا يتعدى 90% من ارتفاع الشاشة */
      overflow-y: auto; /* إضافة تمرير عمودي عند الحاجة */
    }
        .close {
          float: right;
          font-size: 28px;
          cursor: pointer;
        }
          button,
          .details-btn {
            background-color: #4b002f; /* البنفسجي الغامق */
            color: white;
            border: none;
            border-radius: 8px; /* الزوايا ناعمة */
            padding: 10px 15px;
            margin-top: 10px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: 0.3s ease;
          }

          button:hover,
          .details-btn:hover {
            background-color: #6a0044; /* لون أفتح عند المرور */
          }


          .product-options {
            margin-top: 15px;
            text-align: right;
            font-family: 'Cairo', sans-serif;
          }

          .color-options {
            display: flex;
            gap: 10px;
            margin: 10px 0;
            justify-content: right;
          }

    .color-swatch {
      width: 25px;
      height: 25px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid #fff;
      box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
      transition: 0.2s;
    }

    .color-swatch:hover {
      transform: scale(1.1);
      border-color: #4b002f;
    }

    .size-options {
      display: flex;
      gap: 10px;
      justify-content: right;
    }

    .size-btn {
      background-color: #4b002f;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 5px 10px;
      cursor: pointer;
      font-size: 14px;
      transition: 0.3s;
    }

    .size-btn:hover {
      background-color: #4b002f;
      color: white;
      border-color: #4b002f;
    }
     .buy-btn {
        padding: 10px 20px;
        background-color: #4b002f;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      }

      button:hover, .buy-btn:hover {
        background-color: #7a1f4d;
      }

    .favorite-icon {
      background:none;
      border: none;
      cursor: pointer;
      font-size: 22px;
      color: #333; /* اللون الأساسي للقلب */
      transition: color 0.3s ease;
    }

    .favorite-icon.active {
      color: #4b002f; /* بنفسجي عند التفعيل */
    }

    .favorite-icon {
      background: transparent;   /* بدون خلفية */
      border: none;              /* بدون إطار */
      cursor: pointer;
      padding: 0;                /* بدون حواف */
      font-size: 22px;
      transition: color 0.3s;
       margin-top: 16px;  /* عدّلي الرقم حسب المسافة اللي بدك إياها */
    }
    .favorite-icon:hover,
    .favorite-icon:focus,
    .favorite-icon:active {
      box-shadow: none;                    /* يمنع أي ظل */
      outline: none;                       /* لا يظهر إطار عند التحديد */
    }
    .favorite-icon.favorited {
    color: #4b002f;
    }


    .products-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  align-items: flex-start
}

.product {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 250px;
  text-align: center;
   font-size: 13px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

* {
  box-sizing: border-box;
}


  </style>
</head>

<script>
function toggleFavorite(icon) {
  // ✅ يبدّل شكل القلب بين مملوء وفارغ
  icon.classList.toggle('fa-regular'); // القلب الفارغ
  icon.classList.toggle('fa-solid');   // القلب المملوء

  // ✅ يضيف أو يزيل كلاس favorited
  icon.classList.toggle('favorited');

  // ✅ تحديد المنتج من HTML
  const product = icon.closest('.product');
  const pid = product.getAttribute('data-pid');

  // ✅ إذا كان مفضل أو لا (بعد التبديل)
  const isFavorited = icon.classList.contains('favorited');

  // ✅ إرسال طلب إلى السيرفر حسب الحالة
  fetch(isFavorited ? '/add-to-favorites' : '/remove-from-favorites', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ pid: pid })
  }).then(response => {
    if (!response.ok) {
      alert('حدث خطأ أثناء تعديل حالة المفضلة.');
    } else {
      // ✅ إذا المستخدم في صفحة المفضلات ونزع المنتج من المفضلة، احذفه من الواجهة
      if (!isFavorited && window.location.pathname === '/favorites') {
        product.remove();
      }
    }
  });
}
</script>

<body>

      <header>
      <div class="header-container">
      <div class="logo">ANB store</div>

      <nav>
        <a href="/" title="الرئيسية"><i class="fas fa-home"></i></a>
        <a href="/cart" title="السلة"><i class="fas fa-shopping-cart"></i></a>
        <a href="/favorites" title=" المفضلة"><i class="fas fa-heart"></i></a>

      </nav>
      </div>
      </header>

      <div class="side-box">
      <div class="sub-bar"> التوصيل مجاني للطلبات فوق 300 شيكل !</div>
      </div>
      </div>
      <div class="content">

        <h2>HOODES</h2>
        <p>تصفح أحدث منتجاتنا المميزة!</p>
        <div class="store-container">

<form id="addToCartForm" action="/add-to-cart" method="post" style="display: none;">
  <input type="hidden" name="pid" id="cartPid">
  <input type="hidden" name="color" id="cartColor">
  <input type="hidden" name="size" id="cartSize">
  <input type="hidden" name="quantity" value="1">

</form>

<div class="products-container">
<div class="product" 
     data-pid="1"
     data-title="هودي 'دكتور'" 
     data-description="هودي شتوي دافئ بتصميم مميز 'دكتور'" 
     data-price-new="₪69.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc81a667676.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc81a667676.png" alt="منتج">
  <h3>هودي " دكتور "</h3>
  <div class="price">
    <span class="new-price">₪69.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this, '1')"></i>

</div>

<div class="product" 
     data-pid="2"
     data-title="هودي 'المهندس'" 
     data-description="هودي شتوي دافئ بتصميم مميز 'المهندس'" 
     data-price-new="₪69.99"
     data-colors="black,#183B4E,pink,white"  
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_66843b0e55998.jpg">

  <img src="https://files.cdn-files-a.com/uploads/6243106/400_66843b0e55998.jpg" alt="منتج">
  <h3>هودي " المهندس "</h3>
  <div class="price">
    <span class="new-price">₪69.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'2')"></i>

</div>

<div class="product" 
     data-pid="3"
     data-title="هودي 'بتضلي أنتِ العنوان'" 
     data-description="هودي شتوي دافئ بتصميم مميز 'بتضلي أنتِ العنوان'" 
     data-price-old="₪80" 
     data-price-new="₪49.99" 
     data-colors="black,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc4a8eba036.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc4a8eba036.png" alt="منتج">
  <h3>هودي " بتضلي أنتِ العنوان "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪49.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'3')"></i>

</div>

<div class="product" 
     data-pid="4"
     data-title="هودي '  معادلة التوجيهي'" 
     data-description="هودي شتوي دافئ بتصميم مميز خاص بطلبة الثانوية العامة' معادلة التوجيهي'"
     data-price-old="₪80" 
     data-price-new="₪49.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc493bd98f0.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc493bd98f0.png" alt="منتج">
  <h3>هودي "معادلة التوجيهي "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪49.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'4')"></i>

</div>                                             

<div class="product"
     data-pid="5" 
     data-title="هودي ' الحياة مشوار '" 
     data-description=" هودي شتوي دافئ بتصميم مميز 'الحياة مشوار '"
     data-price-old="₪80" 
     data-price-new="₪59.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_66843c98479db.jpg">

  <img src="https://files.cdn-files-a.com/uploads/6243106/400_66843c98479db.jpg" alt="منتج">
  <h3>هودي "الحياة مشوار  "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪59.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'5')"></i>

</div>  

<div class="product"
     data-pid="6" 
     data-title="هودي '  Why always me?  '" 
     data-description= "هودي شتوي دافئ بتصميم مميز ' Why always me ' "
     data-price-new="₪69.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc7dd71fcb5.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc7dd71fcb5.png" alt="منتج">
  <h3>هودي " Why always me?   "</h3>
  <div class="price">
    <span class="new-price">₪69.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'6')"></i>

</div>                                                  


<div class="product" 
     data-pid="8"
     data-title="هودي '  أنا عزيز الروح  '" 
     data-description= "هودي شتوي دافئ بتصميم مميز من كلمات أغنية الفنان الفلسطيني أنس أبو سنينة' أنا عزيز الروح'"
     data-price-old="₪80" 
     data-price-new="₪49.99" 
     data-colors="black,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c8e1646b.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c8e1646b.png" alt="منتج">
  <h3>هودي " أنا عزيز الروح "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪49.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'8')"></i>

</div>                                     
<div class="product"
     data-pid="10" 
     data-title="هودي 'الأمور تحت السيطرة '" 
     data-description= "هودي شتوي دافئ بتصميم 'الأمور تحت السيطرة'"
     data-price-old="₪80" 
     data-price-new="₪59.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c4862ef1.png" >

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c4862ef1.png" alt="منتج">
  <h3>هودي "الأمور تحت السيطرة "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪59.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'10')"></i>

</div>     
<div class="product"
     data-pid="9" 
     data-title="هودي 'فلسطين مزروعة بالقلب '" 
     data-description= "هودي شتوي دافئ بتصميم فلسطيني بامتياز 'فلسطين مزروعة بالقلب'"
     data-price-new="₪59.99" 
     data-colors="black,#183B4E,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc42a07fbf4.png" >

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc42a07fbf4.png" alt="منتج">
  <h3>هودي "فلسطين مزروعة بالقلب "</h3>
  <div class="price">
    <span class="new-price">₪59.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'9')"></i>

</div> 

<div class="product"
     data-pid="7" 
     data-title="هودي '  أنا ما زلت على قيد الحياة  '" 
     data-description= "هودي شتوي دافئ بتصميم مميز فيه شيء من الفُكاهة ' أنا ما زلت على قيد الحياة'"
     data-price-new="₪59.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc7e7a28d72.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc7e7a28d72.png" alt="منتج">
  <h3>هودي " أنا ما زلت على قيد الحياة "</h3>
  <div class="price">
    <span class="new-price">₪59.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'7')"></i>

</div>                                                                  
</div>     

<div id="universalModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="document.getElementById('universalModal').style.display='none'">&times;</span>
    <h2 id="modalTitle"></h2>
    <img id="modalImg" style="width: 100%; max-width: 200px;" />
    <p id="modalDesc"></p>
    <div id="modalExtra"></div> <!-- نغير محتواه حسب نوع المودال -->

    <!-- مثال على الألوان -->
    <div class="product-options">
      <label>الألوان المتوفرة:</label>
      <div class="color-options">
        <span class="color-swatch" style="background-color: black;"></span>
        <span class="color-swatch" style="background-color: #183B4E;"></span>
        <span class="color-swatch" style="background-color: pink;"></span>
        <span class="color-swatch" style="background-color: white; border: 1px solid #ccc;"></span>
      </div>

      <label>الأحجام:</label>
      <div class="size-options">
        <button class="size-btn">S</button>
        <button class="size-btn">M</button>
        <button class="size-btn">L</button>
        <button class="size-btn">XL</button>
        <button class="size-btn">2XL</button>
        <button class="size-btn">3XL</button>
        <!-- بعد أزرار الأحجام -->
        <input type="hidden" id="selectedSize" />
        <input type="hidden" id="selectedColor" />

      </div>
    </div>
  </div>
</div>

<script>
function openModal(button, type) {
  const product = button.closest('.product');
  const title = product.getAttribute('data-title');
  const desc = product.getAttribute('data-description');
  const img = product.getAttribute('data-img');
  const priceOld = product.getAttribute('data-price-old');
  const priceNew = product.getAttribute('data-price-new');
  const pid = product.getAttribute('data-pid');
  const colors = product.getAttribute('data-colors');

  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalDesc').textContent = desc;
  document.getElementById('modalImg').src = img;
  document.getElementById('cartPid').value = pid;

  // توليد ألوان حسب المنتج
  if (colors) {
    const colorArray = colors.split(',');
    const colorContainer = document.querySelector('.color-options');
    colorContainer.innerHTML = ''; // حذف الألوان القديمة

    colorArray.forEach(color => {
      const span = document.createElement('span');
      span.classList.add('color-swatch');
      span.style.backgroundColor = color.trim();

      if (color.trim().toLowerCase() === 'white') {
        span.style.border = '1px solid #ccc'; // لتوضيح الأبيض
      }

      span.addEventListener('click', () => {
        document.getElementById('selectedColor').value = color;
        document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
        span.classList.add('selected');
        document.getElementById('cartColor').value = color; // أضف هذا السطر 👈

      });

      colorContainer.appendChild(span);
    });
  }
// ربط أزرار الحجم
document.querySelectorAll('.size-btn').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    button.classList.add('active');
    document.getElementById('selectedSize').value = button.textContent.trim();
    document.getElementById('cartSize').value = button.textContent.trim(); // 👈 مهم جداً
  });
});

  // محتوى السعر والزر
  const modalExtra = document.getElementById('modalExtra');
  if (type === 'buy') {
    modalExtra.innerHTML = `
      <p><strong>السعر القديم:</strong> ${priceOld}</p>
      <p><strong>السعر الجديد:</strong> ${priceNew}</p>
      <button type="button" onclick="addToCart('${pid}')" style="background: green; color: white;">أضف إلى السلة</button>
    `;
  } else {
    modalExtra.innerHTML = '';
  }

  document.getElementById('universalModal').style.display = 'block';
}

</script>
<style>
.size-btn.active,
.color-swatch.selected {
  outline: 2px solid #4b002f;
}
</style>



<script>
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');

  // نتحقق إذا المستخدم أتى من المفضلة
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(`.product[data-pid="${pid}"]`);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    // نحذف العلامة بعد الفتح، حتى لا تفتح عند التحديث
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>
<script>
function addToCart(pid) {
  const size = document.getElementById('cartSize').value;
  const color = document.getElementById('cartColor').value;

  if (!size || !color) {
    alert("يرجى اختيار اللون والحجم أولاً.");
    return;
  }

  document.getElementById("addToCartForm").submit();
}
</script>

</body>
<footer id="footer" style="
  position: relative; /* عادي */
  width: 100%;
  background-color: #51122F;
  padding: 15px 20px;
  color: white;
  font-family: 'Cairo', sans-serif;
  box-shadow: 0 -4px 15px rgba(81, 18, 47, 0.5);
  opacity: 0;  /* مخفي في البداية */
  transition: opacity 0.5s ease;
">
  <div style="
    max-width: 1200px;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: right;
  ">
    <h3 style="margin-bottom: 8px; font-size: 18px;"> تواصل معنا</h3>

    <a href="https://wa.me/972599663279" target="_blank"
       style="
         background-color: white;
         color: #51122F;
         padding: 8px 20px;
         border-radius: 30px;
         font-size: 14px;
         text-decoration: none;
         margin-bottom: 12px;
         transition: transform 0.3s, box-shadow 0.3s;
         box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
       ">
      إرسال رسالة واتساب
    </a>

    <p style="margin: 8px 0 15px; font-size: 14px; color: #f4f4f4;">
      نحن متجر متخصص في بيع الهوديز والملابس بتصاميم مميزة وجودة عالية.
    </p>

    <div style="font-size: 22px; display: flex; gap: 15px;">
      <a href="https://www.instagram.com/anbstore9?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" target="_blank" title="Instagram"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-instagram"></i>
      </a>
      <a href="https://www.facebook.com/profile.php?id=100083607621116&mibextid=ZbWKwL" target="_blank" title="Facebook"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-facebook"></i>
      </a>
      <a href="https://www.tiktok.com/@anbstore9?fbclid=IwY2xjawK-tkVleHRuA2FlbQIxMABicmlkETEzR1l6YVdSM2dydUx4Zm1lAR7g6BJCqbnkGvy9JFTU6T9l0u2Kqg4EYYPPq92KMGMZ_YchKAXPuEaZ9iwtrQ_aem_DKcG3GyDqUnxEM_AIkiTNQ" target="_blank" title="TikTok"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-tiktok"></i>
      </a>
    </div>
    <p style="font-size: 12px; color: #ccc; margin-top: 20px;">
  © جميع الحقوق محفوظة - <strong>Bailasan Riyad</strong> 2025
    </p>
  </div>
</footer>

<style>
  footer a:hover {
    transform: translateY(-4px) scale(1.05);
  }
</style>

<script>
  window.addEventListener('scroll', function() {
    const footer = document.getElementById('footer');
    const scrollPosition = window.scrollY + window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;

    if (scrollPosition >= pageHeight - 100) { 
      // عندما تكون قريب من نهاية الصفحة بـ 100 بكسل
      footer.style.opacity = '1';
    } else {
      footer.style.opacity = '0';
    }
  });
</script>
        </html>
    ''',
                                      pid=pid,
                                      query=query,
                                      section=section,
                                      products=filtered_products)

# صفحة هوديز كابلز
    elif section == "couples":

        return render_template_string('''

        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
           <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700&display=swap" rel="stylesheet">  <meta charset="UTF-8">
        <meta charset="UTF-8">
        <title>الرئيسية - متجري</title>
        <style>
        *,
        *::before,
        *::after {
          box-sizing: border-box;
        }
        @media (max-width: 768px) {
          .header-container {
            flex-direction: column;
            align-items: stretch;
            gap: 15px;
          }

          .logo {
            text-align: center;
            width: 100%;
            font-size: 22px;
          }

          nav {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            width: 100%;
            gap: 10px;
          }

          nav a {
            font-size: 20px;
          }
        }

        body, button, input, select, textarea {
          font-family: 'Cairo', sans-serif;
          margin: 0;
          padding: 0;
          background-color: #E0E0E0;
          width: 100%;
          overflow-x: hidden;
        }

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.carousel {
  display: flex;
  overflow-x: auto; /* التمرير أفقي */
  overflow-y: hidden;
  width: 100%;
  scroll-behavior: smooth;
  gap: 20px;
  padding: 20px 10px;
}

.arrow,
.arrow:hover,
.arrow:focus,
.arrow:active {
  background: transparent !important;  /* يمنع أي خلفية */
  box-shadow: none !important;         /* يمنع الظلال */
  outline: none !important;            /* يمنع الإطار الخارجي */
}
.product {
    min-width: 250px;
    min-height: 550px;
    text-align: center;
    border-radius: 10px;
    padding: 15px;
    background-color: transparent; /* خلي الخلفية شفافة */
    box-shadow: none; /* إزالة الظل */
}

.product img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    border-radius: 8px;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-80%);
  background: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  font-size: 20px;
  cursor: pointer;
  border-radius: 50%;
  padding: 5px 10px;
  z-index: 5;
}

.arrow.left {
  left: 100px;
}

.arrow.right {
  right: 100px;
}
.image-wrapper {
  position: relative;
  width: 100%;
  height: 250px;
  overflow: hidden;
  border-radius: 8px;
}
        img {
          width: 100%;
          height: 250px; /* حجم موحد لكل الصور */
          object-fit: cover; /* يقص الصورة لتناسب الحجم */
          border-radius: 10px;
        }

        .product-card {
          background-color: white;
          border-radius: 12px;
          padding: 20px;
          text-align: center;
          box-shadow: 0 2px 6px rgba(0,0,0,0.1);
          width: 280px;
          justify-content: space-between; /* يوزع المحتوى بالتساوي */
          display: flex;
          flex-direction: column;
          min-height: 450px; /* لو حابة يكون عندك ارتفاع مبدئي لكن يسمح بالزيادة */
          height: 550px;
        }

        .container {
          position: relative;
        }
.carousel .product {
  flex: 0 0 auto;
  margin: 10px;
  width: 250px;
}

        header {
          background-color: #f1f1f2;
          box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
          color: #51122F;
          padding: 15px 30px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }

        .products-container {
          display: flex;
          justify-content: center;
          gap: 30px; /* المسافة بين المنتجات */
          flex-wrap: wrap; /* حتى لو صغر حجم الشاشة تصير المنتجات تحت بعض */
        }

        .logo {
          font-size: 28px;
          font-weight: bold;
          color: #51122F;
        }

        .search-form {
          display: flex;
          align-items: center;
          background-color: #fff;
          padding: 5px 10px;
          border-radius: 20px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          margin: 0 20px;
        }

        .search-form i {
          color: #888;
          margin-left: 8px;
          font-size: 16px;
        }

        .search-form input[type="text"] {
          padding: 8px 15px;
          border: none;
          border-radius: 20px;
          font-size: 16px;
          outline: none;
          width: 200px;
          background: transparent;
          color: #333;
        }

        nav a {
          color: #51122F;
          margin: 0 15px;
          text-decoration: none;
          font-size: 18px;
        }

        nav a:hover {
          text-decoration: underline;
        }

        .sections {
          text-align: center;
          margin: 50px 20px;
          color:#51122F;
        }

        .sections button {
          padding: 15px 30px;
          margin: 20px;
          font-size: 18px;
          background-color: #51122F;
          color: white;
          border: none;
          border-radius: 25px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .sections button:hover {
          transform: scale(1.05);
        }

        .welcome {
          text-align: center;
          margin: 40px 20px;
          font-size: 24px;
          color: #444;
        }

        .content { text-align: center; margin-top: 50px; }
        .store-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 30px; }
        .buy-btn { display: block; margin-top: 10px; background-color: #51122F; color: white; padding: 10px; border: none; border-radius: 5px; text-decoration: none; }
        .buy-btn:hover { background-color:  #51122F; }   
        .price {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 10px;
          margin-top: 10px;
        }

        .old-price {
          text-decoration: line-through;
          color: #888;
          font-size: 16px;
        }

        .new-price {
          color: #b3003b;
          font-size: 20px;
          font-weight: bold;
        }

        .sub-bar {
          background-color: #51122F;
          color: white;
          text-align: center;
          padding: 10px;
          font-size: 14px;
          margin: 0;           /* إزالة أي هامش علوي */
          border-top: 1px solid #ffffff22; /* إن أردت حدود خفيفة */
        }

        .favorite-icon {
          background:none;
          border: none;
          cursor: pointer;
          font-size: 22px;
          color: #333; /* اللون الأساسي للقلب */
          transition: color 0.3s ease;
        }

        .favorite-icon.active {
          color: #4b002f; /* بنفسجي عند التفعيل */
        }

        .favorite-icon {
          background: transparent;   /* بدون خلفية */
          border: none;              /* بدون إطار */
          cursor: pointer;
          padding: 0;                /* بدون حواف */
          font-size: 22px;
          transition: color 0.3s;
          margin-top: 10px;  /* عدّلي الرقم حسب المسافة اللي بدك إياها */
        }

        .favorite-icon:hover,
        .favorite-icon:focus,
        .favorite-icon:active {
          background: transparent !important;  /* يمنع أي خلفية عند التأشير أو الضغط */
          box-shadow: none;                    /* يمنع أي ظل */
          outline: none;                       /* لا يظهر إطار عند التحديد */
        }
        .favorite-icon.favorited {
        color: #4b002f;
        }                         
        .modal {
          display: none; /* تكون مخفية بالبداية */
          position: fixed; /* تبقى فوق الصفحة */
          z-index: 1000; /* فوق كل العناصر */
          left: 0; top: 0;
          width: 100%; height: 100%;
          background: rgba(0, 0, 0, 0.5); /* خلفية شفافة سوداء */

        }
    .modal-content {
      font-family: 'Cairo', sans-serif; /* خط عربي جميل */
      font-size: 20px;
      color: #333;
      font-weight: 500;
      line-height: 1.6;
      text-align: center;
      margin: 10% auto;
      margin-top: 20px;
      padding: 20px;
      width: 80%;
      max-width: 500px;
      top: 1vh; /* يجعل البطاقة ترتفع لأعلى (تقدري تعدلي النسبة حسب ما تحبي) */
      border-radius: 10px;
      position: relative;
      background: white;
      max-height: 85vh; /* لا يتعدى 90% من ارتفاع الشاشة */
      overflow-y: auto; /* إضافة تمرير عمودي عند الحاجة */
    }
        .close {
          float: right;
          font-size: 28px;
          cursor: pointer;
        }
          button,
          .details-btn {
            background-color: #4b002f; /* البنفسجي الغامق */
            color: white;
            border: none;
            border-radius: 8px; /* الزوايا ناعمة */
            padding: 10px 15px;
            margin-top: 10px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: 0.3s ease;
          }

          button:hover,
          .details-btn:hover {
            background-color: #6a0044; /* لون أفتح عند المرور */
          }

          .product-options {
            margin-top: 15px;
            text-align: right;
            font-family: 'Cairo', sans-serif;
          }

          .color-options {
            display: flex;
            gap: 10px;
            margin: 10px 0;
            justify-content: right;
            min-height: 40px; /* نفس الطول للجميع */

          }

    .color-swatch {
      width: 25px;
      height: 25px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid #fff;
      box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
      transition: 0.2s;
    }

    .color-swatch:hover {
      transform: scale(1.1);
      border-color: #4b002f;
    }

    .size-options {
      display: flex;
      gap: 10px;
      justify-content: right;
    }

    .size-btn {
      background-color: #4b002f;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 5px 10px;
      cursor: pointer;
      font-size: 14px;
      transition: 0.3s;
    }

    .size-btn:hover {
      background-color: #4b002f;
      color: white;
      border-color: #4b002f;
    }
     .buy-btn {
        padding: 10px 20px;
        background-color: #4b002f;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      }

      button:hover, .buy-btn:hover {
        background-color: #7a1f4d;
      }

        </style>

<script>
// ✅ اجمع toggleFavorite في واحدة فقط
function toggleFavorite(icon) {
  icon.classList.toggle('fa-regular');
  icon.classList.toggle('fa-solid');
  icon.classList.toggle('favorited');

  const product = icon.closest('.product');
  const pid = product.getAttribute('data-pid');
  const isFavorited = icon.classList.contains('favorited');

  fetch(isFavorited ? '/add-to-favorites' : '/remove-from-favorites', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pid: pid })
  }).then(response => {
    if (!response.ok) {
      alert('حدث خطأ أثناء تعديل حالة المفضلة.');
    } else if (!isFavorited && window.location.pathname === '/favorites') {
      product.remove();
    }
  });
}
</script>

<script>
function showImage(productId, direction) {
  let images = window["images_" + productId];
  let index = window["index_" + productId];

  index = (index + direction + images.length) % images.length;
  document.getElementById("img_" + productId).src = images[index];

  window["index_" + productId] = index;
}
</script>


    </head>
    <body>
    <header>
    <div class="header-container">
      <div class="logo">ANB store</div>

    <nav>
    <a href="/" title="الرئيسية"><i class="fas fa-home"></i></a>
    <a href="/cart" title="السلة"><i class="fas fa-shopping-cart"></i></a>
     <a href="/favorites" title=" المفضلة"><i class="fas fa-heart"></i></a>

    </nav>
    </div>
    </header>
    <div class="side-box">
    <div class="sub-bar"> التوصيل مجاني للطلبات فوق 300 شيكل !</div>
    </div>
    </div>
    <div class="content">

      <h2>COUPLES HOODES</h2>
      <p>تصفح أحدث منتجاتنا المميزة!</p>
<div class="products-container">

  <div class="product"
   data-pid="11"
   data-title="توم & جيري"
   data-description="هودي زوجي بتصميم مميز - قماش قطني عالي الجودة"
   data-price-new="₪139.99"
   data-colors="black,white" 
   data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc7b5b607f9.png">
    <div class="product-card">
      <div class="image-wrapper">
        <button class="arrow right" onclick="showImage('hoodie1', 1)">&#x276E;</button>
        <img id="img_hoodie1" src="/static/hoodie_black_1.jpg" alt="هودي توم وجيري">
        <button class="arrow left" onclick="showImage('hoodie1', -1)">&#x276F;</button>
      </div>
      <h3>هودي " توم & جيري "</h3>
      <div class="price">
        <span class="new-price">₪139.99</span>
      </div>
      <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
      <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
      <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'11')"></i>
    </div>
  </div>

  <div class="product"
   data-pid="12"
   data-title="تاريخ مميز باللاتيني"  
   data-colors="black,#183B4E,pink,white" 
   data-description="هودي زوجي بتصميم مميز - قماش قطني عالي الجودة" 
   data-price-new="₪119.99" 
   data-img="https://files.cdn-files-a.com/uploads/6243106/400_66844047797b4.jpg">
    <div class="product-card">
      <div class="image-wrapper">
        <button class="arrow right" onclick="showImage('hoodie2', 1)">&#x276E;</button>
        <img id="img_hoodie2" src="/static/hoodie_black_1.jpg" alt="هودي تاريخ مميز باللاتيني">
        <button class="arrow left" onclick="showImage('hoodie2', -1)">&#x276F;</button>
      </div>
      <h3>هودي " تاريخك المميز باللاتيني "</h3>
      <div class="price">
        <span class="new-price">₪119.99</span>
      </div>
      <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
      <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
      <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'12')"></i>
    </div>
  </div>

  <div class="product"
   data-pid="13" 
   data-title="لك جناح و لي جناح"
   data-colors="black,white" 
   data-description="هودي زوجي بتصميم مميز - قماش قطني عالي الجودة"
   data-price-new="₪129.99"
   data-img="https://files.cdn-files-a.com/uploads/6243106/400_66843f625e9e4.jpg">
    <div class="product-card">
      <div class="image-wrapper">
        <button class="arrow right" onclick="showImage('hoodie3', 1)">&#x276E;</button>
        <img id="img_hoodie3" src="/static/hoodie_black_1.jpg" alt="هودي لك جناح ولي جناح">
        <button class="arrow left" onclick="showImage('hoodie3', -1)">&#x276F;</button>
      </div>
      <h3>هودي " لك جناح ولي جناح "</h3>
      <div class="price">
        <span class="new-price">₪129.99</span>
      </div>
      <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
      <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
      <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'13')"></i>
    </div>
  </div>

  <div class="product"
   data-pid="14"
   data-title="هودي القلب و التاريخ"
   data-colors="black,#183B4E,pink,white" 
   data-description="هودي زوجي بتصميم مميز - قماش قطني عالي الجودة"
   data-price-new="₪129.99"
   data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc46647bcc2.png">
    <div class="product-card">
      <div class="image-wrapper">
        <button class="arrow right" onclick="showImage('hoodie4', 1)">&#x276E;</button>
        <img id="img_hoodie4" src="/static/hoodie_black_1.jpg" alt="هودي القلب والتاريخ">
        <button class="arrow left" onclick="showImage('hoodie4', -1)">&#x276F;</button>
      </div>
      <h3>هودي " القلب و التاريخ "</h3>
      <div class="price">
        <span class="new-price">₪129.99</span>
      </div>
      <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
      <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
      <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'14')"></i>
    </div>
  </div>

</div>

<div class="products-container">

  <div class="product"
       data-pid="15"
       data-title="هودي إلى متى يا لوز"
       data-description="هودي زوجي بتصميم مميز - قماش قطني عالي الجودة"
       data-price-new="₪139.99"
       data-colors="black" 
       data-img="https://files.cdn-files-a.com/uploads/6243106/400_66843fcd06af6.jpg">

    <div class="product-card">
      <div class="image-wrapper">
        <button class="arrow right" onclick="showImage('hoodie5', 1)">&#x276E;</button>
        <img id="img_hoodie5" src="/static/hoodie_black_1.jpg" alt="هودي إلى متى يا لوز">
        <button class="arrow left" onclick="showImage('hoodie5', -1)">&#x276F;</button>
      </div>
      <h3>هودي " إلى متى يا لوز " </h3>
      <div class="price">
        <span class="new-price">₪139.99</span>
      </div>
      <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
      <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
      <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'15')"></i>
    </div>

  </div>

</div>


<div id="universalModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="document.getElementById('universalModal').style.display='none'">&times;</span>
    <h2 id="modalTitle"></h2>
    <img id="modalImg" style="width: 100%; max-width: 200px;" />
    <p id="modalDesc"></p>
    <div id="modalExtra"></div> <!-- نغير محتواه حسب نوع المودال -->

    <!-- مثال على الألوان -->
    <div class="product-options">
      <label>الألوان المتوفرة:</label>
      <div class="color-options">
        <span class="color-swatch" style="background-color: black;"></span>
        <span class="color-swatch" style="background-color: #183B4E;"></span>
        <span class="color-swatch" style="background-color: pink;"></span>
        <span class="color-swatch" style="background-color: white; border: 1px solid #ccc;"></span>
      </div>

      <label>الأحجام:</label>
      <div class="size-options">
        <button class="size-btn">S</button>
        <button class="size-btn">M</button>
        <button class="size-btn">L</button>
        <button class="size-btn">XL</button>
        <button class="size-btn">2XL</button>
        <button class="size-btn">3XL</button>
        <!-- بعد أزرار الأحجام -->
        <input type="hidden" id="selectedSize" />
        <input type="hidden" id="selectedColor" />

      </div>
    </div>
  </div>
</div>

<script>
function openModal(button, type) {
  const product = button.closest('.product');
  const title = product.getAttribute('data-title');
  const desc = product.getAttribute('data-description');
  const img = product.getAttribute('data-img');
  const priceOld = product.getAttribute('data-price-old');
  const priceNew = product.getAttribute('data-price-new');
  const pid = product.getAttribute('data-pid');
  const colors = product.getAttribute('data-colors');

  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalDesc').textContent = desc;
  document.getElementById('modalImg').src = img;
  document.getElementById('cartPid').value = pid;

  // توليد ألوان حسب المنتج
  if (colors) {
    const colorArray = colors.split(',');
    const colorContainer = document.querySelector('.color-options');
    colorContainer.innerHTML = ''; // حذف الألوان القديمة

    colorArray.forEach(color => {
      const span = document.createElement('span');
      span.classList.add('color-swatch');
      span.style.backgroundColor = color.trim();

      if (color.trim().toLowerCase() === 'white') {
        span.style.border = '1px solid #ccc'; // لتوضيح الأبيض
      }

      span.addEventListener('click', () => {
        document.getElementById('selectedColor').value = color;
        document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
        span.classList.add('selected');
        document.getElementById('cartColor').value = color; // أضف هذا السطر 👈

      });

      colorContainer.appendChild(span);
    });
  }

  // ربط أزرار الحجم
document.querySelectorAll('.size-btn').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    button.classList.add('active');
    document.getElementById('selectedSize').value = button.textContent.trim();
    document.getElementById('cartSize').value = button.textContent.trim(); // 👈 مهم جداً
  });
});

  // محتوى السعر والزر
  const modalExtra = document.getElementById('modalExtra');
  if (type === 'buy') {
    modalExtra.innerHTML = `
      <p><strong>السعر القديم:</strong> ${priceOld}</p>
      <p><strong>السعر الجديد:</strong> ${priceNew}</p>
      <button type="button" onclick="addToCart('${pid}')" style="background: green; color: white;">أضف إلى السلة</button>
    `;
  } else {
    modalExtra.innerHTML = '';
  }

  document.getElementById('universalModal').style.display = 'block';
}

</script>
<style>
.size-btn.active,
.color-swatch.selected {
  outline: 2px solid #4b002f;
}
</style>

<script>
function addToCart(pid) {
  const size = document.getElementById('cartSize').value;
  const color = document.getElementById('cartColor').value;

  if (!size || !color) {
    alert("يرجى اختيار اللون والحجم أولاً.");
    return;
  }

  document.getElementById("addToCartForm").submit();
}
</script>

<script>
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');

  // نتحقق إذا المستخدم أتى من المفضلة
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(`.product[data-pid="${pid}"]`);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    // نحذف العلامة بعد الفتح، حتى لا تفتح عند التحديث
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>
<script>
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');

  // نتحقق إذا المستخدم أتى من المفضلة
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(.product[data-pid="${pid}"]);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    // نحذف العلامة بعد الفتح، حتى لا تفتح عند التحديث
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>

<form id="addToCartForm" method="POST" action="/add-to-cart" style="display: none;">
  <input type="hidden" id="cartPid" name="pid" />
  <input type="hidden" id="cartColor" name="color" />
  <input type="hidden" id="cartSize" name="size" />
</form>
<script>
window.onload = function () {
  // ✅ صور المنتجات
  window.images_hoodie1 = [
    "https://images.cdn-files-a.com/uploads/6243106/400_65fc7b5b607f9.png",
    "https://images.cdn-files-a.com/uploads/6243106/400_65fc7b4d29542.png"
  ];
  window.index_hoodie1 = 0;

  window.images_hoodie2 = [
    "https://files.cdn-files-a.com/uploads/6243106/400_66844047797b4.jpg"
  ];
  window.index_hoodie2 = 0;

  window.images_hoodie3 = [
    "https://files.cdn-files-a.com/uploads/6243106/400_66843f625e9e4.jpg"
  ];
  window.index_hoodie3 = 0;

  window.images_hoodie4 = [
    "https://images.cdn-files-a.com/uploads/6243106/400_65fc46647bcc2.png"
  ];
  window.index_hoodie4 = 0;

  window.images_hoodie5 = [
    "https://files.cdn-files-a.com/uploads/6243106/400_66843fcd06af6.jpg",
    "https://files.cdn-files-a.com/uploads/6243106/400_66843fcd06580.jpg"
  ];
  window.index_hoodie5 = 0;

  document.getElementById("img_hoodie1").src = window.images_hoodie1[0];
  document.getElementById("img_hoodie2").src = window.images_hoodie2[0];
  document.getElementById("img_hoodie3").src = window.images_hoodie3[0];
  document.getElementById("img_hoodie4").src = window.images_hoodie4[0];
  document.getElementById("img_hoodie5").src = window.images_hoodie5[0];

  // ✅ فتح النافذة عند العودة من المفضلة
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(`.product[data-pid="${pid}"]`);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>                  
</body>
    <footer id="footer" style="
  position: relative; /* عادي */
  width: 100%;
  background-color: #51122F;
  padding: 15px 20px;
  color: white;
  font-family: 'Cairo', sans-serif;
  box-shadow: 0 -4px 15px rgba(81, 18, 47, 0.5);
  opacity: 0;  /* مخفي في البداية */
  transition: opacity 0.5s ease;
">
  <div style="
    max-width: 1200px;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: right;
  ">
    <h3 style="margin-bottom: 8px; font-size: 18px;"> تواصل معنا</h3>

    <a href="https://wa.me/972599663279" target="_blank"
       style="
         background-color: white;
         color: #51122F;
         padding: 8px 20px;
         border-radius: 30px;
         font-size: 14px;
         text-decoration: none;
         margin-bottom: 12px;
         transition: transform 0.3s, box-shadow 0.3s;
         box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
       ">
      إرسال رسالة واتساب
    </a>

    <p style="margin: 8px 0 15px; font-size: 14px; color: #f4f4f4;">
      نحن متجر متخصص في بيع الهوديز والملابس بتصاميم مميزة وجودة عالية.
    </p>

    <div style="font-size: 22px; display: flex; gap: 15px;">
      <a href="https://www.instagram.com/anbstore9?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" target="_blank" title="Instagram"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-instagram"></i>
      </a>
      <a href="https://www.facebook.com/profile.php?id=100083607621116&mibextid=ZbWKwL" target="_blank" title="Facebook"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-facebook"></i>
      </a>
      <a href="https://www.tiktok.com/@anbstore9?fbclid=IwY2xjawK-tkVleHRuA2FlbQIxMABicmlkETEzR1l6YVdSM2dydUx4Zm1lAR7g6BJCqbnkGvy9JFTU6T9l0u2Kqg4EYYPPq92KMGMZ_YchKAXPuEaZ9iwtrQ_aem_DKcG3GyDqUnxEM_AIkiTNQ" target="_blank" title="TikTok"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-tiktok"></i>
      </a>
    </div>
    <p style="font-size: 12px; color: #ccc; margin-top: 20px;">
  © جميع الحقوق محفوظة - <strong>Bailasan Riyad</strong> 2025
</p>
  </div>
</footer>

<style>
  footer a:hover {
    transform: translateY(-4px) scale(1.05);
  }
</style>

<script>
  window.addEventListener('scroll', function() {
    const footer = document.getElementById('footer');
    const scrollPosition = window.scrollY + window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;

    if (scrollPosition >= pageHeight - 100) { 
      // عندما تكون قريب من نهاية الصفحة بـ 100 بكسل
      footer.style.opacity = '1';
    } else {
      footer.style.opacity = '0';
    }
  });
</script>
</html>''',
                                      pid=pid,
                                      query=query,
                                      products=filtered_products,
                                      section=section)
# صيفي

    elif section == "T-SHIRT":
        section = request.args.get("section", "")
        pid = request.args.get("pid")  # أضف هذا السطر
        query = request.args.get("q", "").strip()

        return render_template_string('''
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
          <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700&display=swap" rel="stylesheet">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <meta charset="UTF-8">
        <title>الرئيسية - متجري</title>
        <style>
        @media (max-width: 768px) {
          .header-container {
            flex-direction: column;
            align-items: stretch;
            gap: 15px;
          }

          .logo {
            text-align: center;
            width: 100%;
            font-size: 22px;
          }

          nav {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            width: 100%;
            gap: 10px;
          }

          nav a {
            font-size: 20px;
          }
        }

        body, button, input, select, textarea {
          font-family: 'Cairo', sans-serif;
          margin: 0;
          padding: 0;
          background-color: #E0E0E0; 
          overflow-x: hidden; 
        }

        header {
          background-color: #f1f1f2;
          box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
          color: #51122F;
          padding: 15px 30px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }

        .logo {
          font-size: 28px;
          font-weight: bold;
          color: #51122F;
        }

        .search-form {
          display: flex;
          align-items: center;
          background-color: #fff;
          padding: 5px 10px;
          border-radius: 20px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          margin: 0 20px;
        }

        .search-form i {
          color: #888;
          margin-left: 8px;
          font-size: 16px;
        }

        .search-form input[type="text"] {
          padding: 8px 15px;
          border: none;
          border-radius: 20px;
          font-size: 16px;
          outline: none;
          width: 200px;
          background: transparent;
          color: #333;
        }

        nav a {
          color: #51122F;
          margin: 0 15px;
          text-decoration: none;
          font-size: 18px;
        }

        nav a:hover {
          text-decoration: underline;
        }
        .sections {
          text-align: center;
          margin: 50px 20px;
          color:#51122F;
        }

        .sections button {
          padding: 15px 30px;
          margin: 20px;
          font-size: 18px;
          background-color: #51122F;
          color: white;
          border: none;
          border-radius: 25px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .sections button:hover {
          transform: scale(1.05);
        }
        .price {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 10px;
          margin-top: 10px;
        }

        .old-price {
          text-decoration: line-through;
          color: #888;
          font-size: 16px;
        }

        .new-price {
          color: #b3003b;
          font-size: 20px;
          font-weight: bold;
        }

        .welcome {
          text-align: center;
          margin: 40px 20px;
          font-size: 24px;
          color: #444;
        }
        .content { text-align: center; margin-top: 50px; }
        .store-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 30px; }
        .product {   margin: 25px;border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center;  width: 250px; /* أو أي عرض تريده */
  height:520px; /* نفس الارتفاع لكل البطاقات */ background:  #fff; }
        .product img { width: 100%; border-radius: 10px;  height: 200px; /* اضبط حسب طول الصور */
  object-fit: cover; /* يمنع الصورة من التشوه */ }
        .buy-btn { display: block; margin-top: 10px; background-color: #51122F; color: white; padding: 10px; border: none; border-radius: 5px; text-decoration: none; }
        .buy-btn:hover { background-color:  #51122F; }   
        .sub-bar {
          background-color: #51122F;
          color: white;
          text-align: center;
          padding: 10px;
          font-size: 14px;
          margin: 0;           /* إزالة أي هامش علوي */
          border-top: 1px solid #ffffff22; /* إن أردت حدود خفيفة */
        }                                         

        .modal {
          display: none; /* تكون مخفية بالبداية */
          position: fixed; /* تبقى فوق الصفحة */
          z-index: 1000; /* فوق كل العناصر */
          left: 0; top: 0;
          width: 100%; height: 100%;
          background: rgba(0, 0, 0, 0.5); /* خلفية شفافة سوداء */

        }
    .modal-content {
      font-family: 'Cairo', sans-serif; /* خط عربي جميل */
      font-size: 20px;
      color: #333;
      font-weight: 500;
      line-height: 1.6;
      text-align: center;
      margin: 10% auto;
      margin-top: 20px;
      padding: 20px;
      width: 80%;
      max-width: 500px;
      top: 5vh; /* يجعل البطاقة ترتفع لأعلى (تقدري تعدلي النسبة حسب ما تحبي) */
      border-radius: 10px;
      position: relative;
      background: white;
      max-height: 90vh; /* لا يتعدى 90% من ارتفاع الشاشة */
      overflow-y: auto; /* إضافة تمرير عمودي عند الحاجة */
    }
        .close {
          float: right;
          font-size: 28px;
          cursor: pointer;
        }
          button,
          .details-btn {
            background-color: #4b002f; /* البنفسجي الغامق */
            color: white;
            border: none;
            border-radius: 8px; /* الزوايا ناعمة */
            padding: 10px 15px;
            margin-top: 10px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: 0.3s ease;
          }

          button:hover,
          .details-btn:hover {
            background-color: #6a0044; /* لون أفتح عند المرور */
          }


          .product-options {
            margin-top: 15px;
            text-align: right;
            font-family: 'Cairo', sans-serif;
          }

          .color-options {
            display: flex;
            gap: 10px;
            margin: 10px 0;
            justify-content: right;
          }

    .color-swatch {
      width: 25px;
      height: 25px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid #fff;
      box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
      transition: 0.2s;
    }

    .color-swatch:hover {
      transform: scale(1.1);
      border-color: #4b002f;
    }

    .size-options {
      display: flex;
      gap: 10px;
      justify-content: right;
    }

    .size-btn {
      background-color: #4b002f;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 5px 10px;
      cursor: pointer;
      font-size: 14px;
      transition: 0.3s;
    }

    .size-btn:hover {
      background-color: #4b002f;
      color: white;
      border-color: #4b002f;
    }
     .buy-btn {
        padding: 10px 20px;
        background-color: #4b002f;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      }

      button:hover, .buy-btn:hover {
        background-color: #7a1f4d;
      }

    .favorite-icon {
      background:none;
      border: none;
      cursor: pointer;
      font-size: 22px;
      color: #333; /* اللون الأساسي للقلب */
      transition: color 0.3s ease;
    }

    .favorite-icon.active {
      color: #4b002f; /* بنفسجي عند التفعيل */
    }

    .favorite-icon {
      background: transparent;   /* بدون خلفية */
      border: none;              /* بدون إطار */
      cursor: pointer;
      padding: 0;                /* بدون حواف */
      font-size: 22px;
      transition: color 0.3s;
       margin-top: 16px;  /* عدّلي الرقم حسب المسافة اللي بدك إياها */
    }
    .favorite-icon:hover,
    .favorite-icon:focus,
    .favorite-icon:active {
      box-shadow: none;                    /* يمنع أي ظل */
      outline: none;                       /* لا يظهر إطار عند التحديد */
    }
    .favorite-icon.favorited {
    color: #4b002f;
    }


    .products-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  align-items: flex-start
}

.product {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 250px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  font-size: 14px; /* 👈 هذا هو السطر الجديد */

}

* {
  box-sizing: border-box;
}

  </style>
</head>

<script>
function toggleFavorite(icon) {
  // ✅ يبدّل شكل القلب بين مملوء وفارغ
  icon.classList.toggle('fa-regular'); // القلب الفارغ
  icon.classList.toggle('fa-solid');   // القلب المملوء

  // ✅ يضيف أو يزيل كلاس favorited
  icon.classList.toggle('favorited');

  // ✅ تحديد المنتج من HTML
  const product = icon.closest('.product');
  const pid = product.getAttribute('data-pid');

  // ✅ إذا كان مفضل أو لا (بعد التبديل)
  const isFavorited = icon.classList.contains('favorited');

  // ✅ إرسال طلب إلى السيرفر حسب الحالة
  fetch(isFavorited ? '/add-to-favorites' : '/remove-from-favorites', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ pid: pid })
  }).then(response => {
    if (!response.ok) {
      alert('حدث خطأ أثناء تعديل حالة المفضلة.');
    } else {
      // ✅ إذا المستخدم في صفحة المفضلات ونزع المنتج من المفضلة، احذفه من الواجهة
      if (!isFavorited && window.location.pathname === '/favorites') {
        product.remove();
      }
    }
  });
}
</script>

<body>

      <header>
      <div class="header-container">
      <div class="logo">ANB store</div>

      <nav>
        <a href="/" title="الرئيسية"><i class="fas fa-home"></i></a>
        <a href="/cart" title="السلة"><i class="fas fa-shopping-cart"></i></a>
        <a href="/favorites" title=" المفضلة"><i class="fas fa-heart"></i></a>

      </nav>
      </div>
      </header>

      <div class="side-box">
      <div class="sub-bar"> التوصيل مجاني للطلبات فوق 300 شيكل !</div>
      </div>
      </div>
      <div class="content">

        <h2>T-sheert</h2>
        <p>تصفح أحدث منتجاتنا المميزة!</p>
        <div class="store-container">

<form id="addToCartForm" action="/add-to-cart" method="post" style="display: none;">
  <input type="hidden" name="pid" id="cartPid">
  <input type="hidden" name="color" id="cartColor">
  <input type="hidden" name="size" id="cartSize">
  <input type="hidden" name="quantity" value="1">

</form>
<div class="product"
     data-pid="16"
     data-title="تحقق ما كان بالأمس حُلماً" 
     data-description="تيشرت صيفي بتصميم خاص بطلبة الثانوية العامة (تيشيرت التواقيع)"
     data-price-old="₪70" 
     data-price-new="₪49.99" 
     data-colors="white"
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_6684418364991.jpg">

  <img src="https://files.cdn-files-a.com/uploads/6243106/400_6684418364991.jpg" alt="منتج 1">
  <h3>تحقق ما كان بالأمس حُلماً</h3>
    <div class="price">
    <span class="old-price">₪70</span>
    <span class="new-price">₪49.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'16')"></i>
</div>



<div class="product"
     data-pid="17"
     data-title="Cristiano" 
     data-description="تيشرت صيفي بتصميم خاص بمحبين المباريات و Cristiano!"
     data-price-old="₪70" 
     data-price-new="₪44.99"
     data-colors="black,#183B4E,pink,white" 
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_668441cae61ae.jpg">
  <img src="https://files.cdn-files-a.com/uploads/6243106/400_668441cae61ae.jpg" alt="منتج 4">
  <h3>Cristiano !</h3>
    <div class="price">
    <span class="old-price">₪70</span>
    <span class="new-price">₪44.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'17')"></i>
</div>

<div class="product"
     data-pid="18"
     data-title="درسنا لنعمرها" 
     data-description="تيشرت صيفي مميز بتصميم محفز"
     data-price-old="₪60" 
     data-price-new="₪39.99" 
     data-colors="white"
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_66a90c56065cd.jpg">
  <img src="https://files.cdn-files-a.com/uploads/6243106/400_66a90c56065cd.jpg" alt="منتج 5">
  <h3>درسنا لنعمرها</h3>
  <div class="price">
    <span class="old-price">₪60</span>
    <span class="new-price">₪39.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'18')"></i>
</div>

<div class="product"
     data-pid="19"
     data-title="فكر خارج الصندوق" 
     data-description="تيشرت تحفيزي بتصميم شبابي"
     data-price-old="₪60" 
     data-price-new="₪39.99"
     data-colors="black,white" 
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_6684411d02014.jpg">
  <img src="https://files.cdn-files-a.com/uploads/6243106/400_6684411d02014.jpg" alt="منتج 6">
  <h3>فكر خارج الصندوق</h3>
  <div class="price">
    <span class="old-price">₪60</span>
    <span class="new-price">₪39.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'19')"></i>
</div>

<div id="universalModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="document.getElementById('universalModal').style.display='none'">&times;</span>
    <h2 id="modalTitle"></h2>
    <img id="modalImg" style="width: 100%; max-width: 200px;" />
    <p id="modalDesc"></p>
    <div id="modalExtra"></div> <!-- نغير محتواه حسب نوع المودال -->

    <!-- مثال على الألوان -->
    <div class="product-options">
      <label>الألوان المتوفرة:</label>
      <div class="color-options">
        <span class="color-swatch" style="background-color: black;"></span>
        <span class="color-swatch" style="background-color: #183B4E;"></span>
        <span class="color-swatch" style="background-color: pink;"></span>
        <span class="color-swatch" style="background-color: white; border: 1px solid #ccc;"></span>
      </div>

      <label>الأحجام:</label>
      <div class="size-options">
        <button class="size-btn">S</button>
        <button class="size-btn">M</button>
        <button class="size-btn">L</button>
        <button class="size-btn">XL</button>
        <button class="size-btn">2XL</button>
        <button class="size-btn">3XL</button>
        <!-- بعد أزرار الأحجام -->
        <input type="hidden" id="selectedSize" />
        <input type="hidden" id="selectedColor" />

      </div>
    </div>
  </div>
</div>

<script>
function openModal(button, type) {
  const product = button.closest('.product');
  const title = product.getAttribute('data-title');
  const desc = product.getAttribute('data-description');
  const img = product.getAttribute('data-img');
  const priceOld = product.getAttribute('data-price-old');
  const priceNew = product.getAttribute('data-price-new');
  const pid = product.getAttribute('data-pid');
  const colors = product.getAttribute('data-colors');

  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalDesc').textContent = desc;
  document.getElementById('modalImg').src = img;
  document.getElementById('cartPid').value = pid;

  // توليد ألوان حسب المنتج
  if (colors) {
    const colorArray = colors.split(',');
    const colorContainer = document.querySelector('.color-options');
    colorContainer.innerHTML = ''; // حذف الألوان القديمة

    colorArray.forEach(color => {
      const span = document.createElement('span');
      span.classList.add('color-swatch');
      span.style.backgroundColor = color.trim();

      if (color.trim().toLowerCase() === 'white') {
        span.style.border = '1px solid #ccc'; // لتوضيح الأبيض
      }

      span.addEventListener('click', () => {
        document.getElementById('selectedColor').value = color;
        document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
        span.classList.add('selected');
        document.getElementById('cartColor').value = color; // أضف هذا السطر 👈

      });

      colorContainer.appendChild(span);
    });
  }
  // ربط أزرار الحجم
document.querySelectorAll('.size-btn').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    button.classList.add('active');
    document.getElementById('selectedSize').value = button.textContent.trim();
    document.getElementById('cartSize').value = button.textContent.trim(); // 👈 مهم جداً
  });
});

  // محتوى السعر والزر
  const modalExtra = document.getElementById('modalExtra');
  if (type === 'buy') {
    modalExtra.innerHTML = `
      <p><strong>السعر القديم:</strong> ${priceOld}</p>
      <p><strong>السعر الجديد:</strong> ${priceNew}</p>
      <button type="button" onclick="addToCart('${pid}')" style="background: green; color: white;">أضف إلى السلة</button>
    `;
  } else {
    modalExtra.innerHTML = '';
  }

  document.getElementById('universalModal').style.display = 'block';
}

</script>
<style>
.size-btn.active,
.color-swatch.selected {
  outline: 2px solid #4b002f;
}
</style>
<script>
function addToCart(pid) {
  const size = document.getElementById('cartSize').value;
  const color = document.getElementById('cartColor').value;

  if (!size || !color) {
    alert("يرجى اختيار اللون والحجم أولاً.");
    return;
  }

  document.getElementById("addToCartForm").submit();
}
</script>


<script>
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');

  // نتحقق إذا المستخدم أتى من المفضلة
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(`.product[data-pid="${pid}"]`);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    // نحذف العلامة بعد الفتح، حتى لا تفتح عند التحديث
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>

</body>

  <footer id="footer" style="
  position: relative; /* عادي */
  width: 100%;
  background-color: #51122F;
  padding: 15px 20px;
  color: white;
  font-family: 'Cairo', sans-serif;
  box-shadow: 0 -4px 15px rgba(81, 18, 47, 0.5);
  opacity: 0;  /* مخفي في البداية */
  transition: opacity 0.5s ease;
">
  <div style="
    max-width: 1200px;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: right;
  ">
    <h3 style="margin-bottom: 8px; font-size: 18px;"> تواصل معنا</h3>

    <a href="https://wa.me/972599663279" target="_blank"
       style="
         background-color: white;
         color: #51122F;
         padding: 8px 20px;
         border-radius: 30px;
         font-size: 14px;
         text-decoration: none;
         margin-bottom: 12px;
         transition: transform 0.3s, box-shadow 0.3s;
         box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
       ">
      إرسال رسالة واتساب
    </a>

    <p style="margin: 8px 0 15px; font-size: 14px; color: #f4f4f4;">
      نحن متجر متخصص في بيع الهوديز والملابس بتصاميم مميزة وجودة عالية.
    </p>

    <div style="font-size: 22px; display: flex; gap: 15px;">
      <a href="https://www.instagram.com/anbstore9?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" target="_blank" title="Instagram"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-instagram"></i>
      </a>
      <a href="https://www.facebook.com/profile.php?id=100083607621116&mibextid=ZbWKwL" target="_blank" title="Facebook"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-facebook"></i>
      </a>
      <a href="https://www.tiktok.com/@anbstore9?fbclid=IwY2xjawK-tkVleHRuA2FlbQIxMABicmlkETEzR1l6YVdSM2dydUx4Zm1lAR7g6BJCqbnkGvy9JFTU6T9l0u2Kqg4EYYPPq92KMGMZ_YchKAXPuEaZ9iwtrQ_aem_DKcG3GyDqUnxEM_AIkiTNQ" target="_blank" title="TikTok"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-tiktok"></i>
      </a>
    </div>
      <p style="font-size: 12px; color: #ccc; margin-top: 20px;">
  © جميع الحقوق محفوظة - <strong>Bailasan Riyad</strong> 2025
      </p>

  </div>
</footer>

<style>
  footer a:hover {
    transform: translateY(-4px) scale(1.05);
  }
</style>

<script>
  window.addEventListener('scroll', function() {
    const footer = document.getElementById('footer');
    const scrollPosition = window.scrollY + window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;

    if (scrollPosition >= pageHeight - 100) { 
      // عندما تكون قريب من نهاية الصفحة بـ 100 بكسل
      footer.style.opacity = '1';
    } else {
      footer.style.opacity = '0';
    }
  });
</script>
        </html>
    ''',
                                      pid=pid,
                                      query=query,
                                      section=section,
                                      products=filtered_products)

    elif section == "orood":

        return render_template_string('''

        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
          <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700&display=swap" rel="stylesheet">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <meta charset="UTF-8">
        <title>الرئيسية - متجري</title>
        <style>
        @media (max-width: 768px) {
          .header-container {
            flex-direction: column;
            align-items: stretch;
            gap: 15px;
          }

          .logo {
            text-align: center;
            width: 100%;
            font-size: 22px;
          }

          nav {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            width: 100%;
            gap: 10px;
          }

          nav a {
            font-size: 20px;
          }
        }

        body, button, input, select, textarea {
          font-family: 'Cairo', sans-serif;
          margin: 0;
          padding: 0;
          background-color: #E0E0E0; 
          overflow-x: hidden; 
        }

        header {
          background-color: #f1f1f2;
          box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
          color: #51122F;
          padding: 15px 30px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }

        .logo {
          font-size: 28px;
          font-weight: bold;
          color: #51122F;
        }

        .search-form {
          display: flex;
          align-items: center;
          background-color: #fff;
          padding: 5px 10px;
          border-radius: 20px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          margin: 0 20px;
        }

        .search-form i {
          color: #888;
          margin-left: 8px;
          font-size: 16px;
        }

        .search-form input[type="text"] {
          padding: 8px 15px;
          border: none;
          border-radius: 20px;
          font-size: 16px;
          outline: none;
          width: 200px;
          background: transparent;
          color: #333;
        }

        nav a {
          color: #51122F;
          margin: 0 15px;
          text-decoration: none;
          font-size: 18px;
        }

        nav a:hover {
          text-decoration: underline;
        }
        .sections {
          text-align: center;
          margin: 50px 20px;
          color:#51122F;
        }

        .sections button {
          padding: 15px 30px;
          margin: 20px;
          font-size: 18px;
          background-color: #51122F;
          color: white;
          border: none;
          border-radius: 25px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .sections button:hover {
          transform: scale(1.05);
        }
        .price {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 10px;
          margin-top: 10px;
        }

        .old-price {
          text-decoration: line-through;
          color: #888;
          font-size: 16px;
        }

        .new-price {
          color: #b3003b;
          font-size: 20px;
          font-weight: bold;
        }

        .welcome {
          text-align: center;
          margin: 40px 20px;
          font-size: 24px;
          color: #444;
        }
        .content { text-align: center; margin-top: 50px; }
        .store-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 30px; }
        .product {   margin: 25px;border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center;  width: 250px; /* أو أي عرض تريده */
  height: 520px; /* نفس الارتفاع لكل البطاقات */background:  #fff; }
        .product img { width: 100%; border-radius: 10px;  height: 200px; /* اضبط حسب طول الصور */
  object-fit: cover; /* يمنع الصورة من التشوه */ }
        .buy-btn { display: block; margin-top: 10px; background-color: #51122F; color: white; padding: 10px; border: none; border-radius: 5px; text-decoration: none; }
        .buy-btn:hover { background-color:  #51122F; }   
        .sub-bar {
          background-color: #51122F;
          color: white;
          text-align: center;
          padding: 10px;
          font-size: 14px;
          margin: 0;           /* إزالة أي هامش علوي */
          border-top: 1px solid #ffffff22; /* إن أردت حدود خفيفة */
        }                                         

        .modal {
          display: none; /* تكون مخفية بالبداية */
          position: fixed; /* تبقى فوق الصفحة */
          z-index: 1000; /* فوق كل العناصر */
          left: 0; top: 0;
          width: 100%; height: 100%;
          background: rgba(0, 0, 0, 0.5); /* خلفية شفافة سوداء */

        }
    .modal-content {
      font-family: 'Cairo', sans-serif; /* خط عربي جميل */
      font-size: 20px;
      color: #333;
      font-weight: 500;
      line-height: 1.6;
      text-align: center;
      margin: 10% auto;
      margin-top: 20px;
      padding: 20px;
      width: 80%;
      max-width: 500px;
      top: 5vh; /* يجعل البطاقة ترتفع لأعلى (تقدري تعدلي النسبة حسب ما تحبي) */
      border-radius: 10px;
      position: relative;
      background: white;
      max-height: 90vh; /* لا يتعدى 90% من ارتفاع الشاشة */
      overflow-y: auto; /* إضافة تمرير عمودي عند الحاجة */
    }
        .close {
          float: right;
          font-size: 28px;
          cursor: pointer;
        }
          button,
          .details-btn {
            background-color: #4b002f; /* البنفسجي الغامق */
            color: white;
            border: none;
            border-radius: 8px; /* الزوايا ناعمة */
            padding: 10px 15px;
            margin-top: 10px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: 0.3s ease;
          }

          button:hover,
          .details-btn:hover {
            background-color: #6a0044; /* لون أفتح عند المرور */
          }


          .product-options {
            margin-top: 15px;
            text-align: right;
            font-family: 'Cairo', sans-serif;
          }

          .color-options {
            display: flex;
            gap: 10px;
            margin: 10px 0;
            justify-content: right;
          }

    .color-swatch {
      width: 25px;
      height: 25px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid #fff;
      box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
      transition: 0.2s;
    }

    .color-swatch:hover {
      transform: scale(1.1);
      border-color: #4b002f;
    }

    .size-options {
      display: flex;
      gap: 10px;
      justify-content: right;
    }

    .size-btn {
      background-color: #4b002f;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 5px 10px;
      cursor: pointer;
      font-size: 14px;
      transition: 0.3s;
    }

    .size-btn:hover {
      background-color: #4b002f;
      color: white;
      border-color: #4b002f;
    }
     .buy-btn {
        padding: 10px 20px;
        background-color: #4b002f;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      }

      button:hover, .buy-btn:hover {
        background-color: #7a1f4d;
      }

    .favorite-icon {
      background:none;
      border: none;
      cursor: pointer;
      font-size: 22px;
      color: #333; /* اللون الأساسي للقلب */
      transition: color 0.3s ease;
    }

    .favorite-icon.active {
      color: #4b002f; /* بنفسجي عند التفعيل */
    }

    .favorite-icon {
      background: transparent;   /* بدون خلفية */
      border: none;              /* بدون إطار */
      cursor: pointer;
      padding: 0;                /* بدون حواف */
      font-size: 22px;
      transition: color 0.3s;
       margin-top: 16px;  /* عدّلي الرقم حسب المسافة اللي بدك إياها */
    }
    .favorite-icon:hover,
    .favorite-icon:focus,
    .favorite-icon:active {
      box-shadow: none;                    /* يمنع أي ظل */
      outline: none;                       /* لا يظهر إطار عند التحديد */
    }
    .favorite-icon.favorited {
    color: #4b002f;
    }


    .products-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  align-items: flex-start
}

.product {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 250px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  font-size: 13.5px; /* 👈 هذا هو السطر الجديد */

}

* {
  box-sizing: border-box;
}

  </style>
</head>

<script>
function toggleFavorite(icon) {
  // ✅ يبدّل شكل القلب بين مملوء وفارغ
  icon.classList.toggle('fa-regular'); // القلب الفارغ
  icon.classList.toggle('fa-solid');   // القلب المملوء

  // ✅ يضيف أو يزيل كلاس favorited
  icon.classList.toggle('favorited');

  // ✅ تحديد المنتج من HTML
  const product = icon.closest('.product');
  const pid = product.getAttribute('data-pid');

  // ✅ إذا كان مفضل أو لا (بعد التبديل)
  const isFavorited = icon.classList.contains('favorited');

  // ✅ إرسال طلب إلى السيرفر حسب الحالة
  fetch(isFavorited ? '/add-to-favorites' : '/remove-from-favorites', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ pid: pid })
  }).then(response => {
    if (!response.ok) {
      alert('حدث خطأ أثناء تعديل حالة المفضلة.');
    } else {
      // ✅ إذا المستخدم في صفحة المفضلات ونزع المنتج من المفضلة، احذفه من الواجهة
      if (!isFavorited && window.location.pathname === '/favorites') {
        product.remove();
      }
    }
  });
}
</script>

<body>

      <header>
      <div class="header-container">
      <div class="logo">ANB store</div>

      <nav>
        <a href="/" title="الرئيسية"><i class="fas fa-home"></i></a>
        <a href="/cart" title="السلة"><i class="fas fa-shopping-cart"></i></a>
        <a href="/favorites" title=" المفضلة"><i class="fas fa-heart"></i></a>

      </nav>
      </div>
      </header>

      <div class="side-box">
      <div class="sub-bar"> التوصيل مجاني للطلبات فوق 300 شيكل !</div>
      </div>
      </div>
      <div class="content">

<form id="addToCartForm" action="/add-to-cart" method="post" style="display: none;">
  <input type="hidden" name="pid" id="cartPid">
  <input type="hidden" name="color" id="cartColor">
  <input type="hidden" name="size" id="cartSize">
  <input type="hidden" name="quantity" value="1">

</form>
    <h2>SALE !</h2>
    <p>تصفح أحدث منتجاتنا المميزة!</p>
    <div class="store-container">

<div class="product"
     data-pid="16"
     data-title="تحقق ما كان بالأمس حُلماً" 
     data-description="تيشرت صيفي بتصميم خاص بطلبة الثانوية العامة (تيشيرت التواقيع)"
     data-price-old="₪70" 
     data-price-new="₪49.99" 
     data-colors="white"
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_6684418364991.jpg">

  <img src="https://files.cdn-files-a.com/uploads/6243106/400_6684418364991.jpg" alt="منتج 1">
  <h3>تحقق ما كان بالأمس حُلماً</h3>
    <div class="price">
    <span class="old-price">₪70</span>
    <span class="new-price">₪49.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'16')"></i>
</div>



<div class="product"
     data-pid="17"
     data-title="Cristiano" 
     data-description="تيشرت صيفي بتصميم خاص بمحبين المباريات و Cristiano!"
     data-price-old="₪70" 
     data-price-new="₪44.99"
     data-colors="black,#183B4E,pink,white" 
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_668441cae61ae.jpg">
  <img src="https://files.cdn-files-a.com/uploads/6243106/400_668441cae61ae.jpg" alt="منتج 4">
  <h3>Cristiano !</h3>
    <div class="price">
    <span class="old-price">₪70</span>
    <span class="new-price">₪44.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'17')"></i>
</div>

<div class="product"
     data-pid="18"
     data-title="درسنا لنعمرها" 
     data-description="تيشرت صيفي مميز بتصميم محفز"
     data-price-old="₪60" 
     data-price-new="₪39.99" 
     data-colors="white"
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_66a90c56065cd.jpg">
  <img src="https://files.cdn-files-a.com/uploads/6243106/400_66a90c56065cd.jpg" alt="منتج 5">
  <h3>درسنا لنعمرها</h3>
  <div class="price">
    <span class="old-price">₪60</span>
    <span class="new-price">₪39.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'18')"></i>
</div>

<div class="product"
     data-pid="19"
     data-title="فكر خارج الصندوق" 
     data-description="تيشرت تحفيزي بتصميم شبابي"
     data-price-old="₪60" 
     data-price-new="₪39.99"
     data-colors="black,white" 
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_6684411d02014.jpg">
  <img src="https://files.cdn-files-a.com/uploads/6243106/400_6684411d02014.jpg" alt="منتج 6">
  <h3>فكر خارج الصندوق</h3>
  <div class="price">
    <span class="old-price">₪60</span>
    <span class="new-price">₪39.99</span>
  </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'19')"></i>
</div>

<div class="product" 
     data-pid="3"
     data-title="هودي 'بتضلي أنتِ العنوان'" 
     data-description="هودي شتوي دافئ بتصميم مميز 'بتضلي أنتِ العنوان'" 
     data-price-old="₪80" 
     data-price-new="₪49.99" 
     data-colors="black,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc4a8eba036.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc4a8eba036.png" alt="منتج">
  <h3>هودي " بتضلي أنتِ العنوان "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪49.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'3')"></i>

</div>

<div class="product" 
     data-pid="4"
     data-title="هودي '  معادلة التوجيهي'" 
     data-description="هودي شتوي دافئ بتصميم مميز خاص بطلبة الثانوية العامة' معادلة التوجيهي'"
     data-price-old="₪80" 
     data-price-new="₪49.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc493bd98f0.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc493bd98f0.png" alt="منتج">
  <h3>هودي "معادلة التوجيهي "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪49.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'4')"></i>

</div>                                             

<div class="product"
     data-pid="5" 
     data-title="هودي ' الحياة مشوار '" 
     data-description=" هودي شتوي دافئ بتصميم مميز 'الحياة مشوار '"
     data-price-old="₪80" 
     data-price-new="₪59.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://files.cdn-files-a.com/uploads/6243106/400_66843c98479db.jpg">

  <img src="https://files.cdn-files-a.com/uploads/6243106/400_66843c98479db.jpg" alt="منتج">
  <h3>هودي "الحياة مشوار  "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪59.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'5')"></i>

</div>  

<div class="product" 
     data-pid="8"
     data-title="هودي '  أنا عزيز الروح  '" 
     data-description= "هودي شتوي دافئ بتصميم مميز من كلمات أغنية الفنان الفلسطيني أنس أبو سنينة' أنا عزيز الروح'"
     data-price-old="₪80" 
     data-price-new="₪49.99" 
     data-colors="black,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c8e1646b.png">

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c8e1646b.png" alt="منتج">
  <h3>هودي " أنا عزيز الروح "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪49.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'8')"></i>

</div>         

<div class="product"
     data-pid="10" 
     data-title="هودي 'الأمور تحت السيطرة '" 
     data-description= "هودي شتوي دافئ بتصميم 'الأمور تحت السيطرة'"
     data-price-old="₪80" 
     data-price-new="₪59.99" 
     data-colors="black,#183B4E,pink,white" 
     data-img="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c4862ef1.png" >

  <img src="https://images.cdn-files-a.com/uploads/6243106/400_65fc7c4862ef1.png" alt="منتج">
  <h3>هودي "الأمور تحت السيطرة "</h3>
  <div class="price">
    <span class="old-price">₪80</span>
    <span class="new-price">₪59.99</span>
  </div>

  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'10')"></i>

</div>     

<div id="universalModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="document.getElementById('universalModal').style.display='none'">&times;</span>
    <h2 id="modalTitle"></h2>
    <img id="modalImg" style="width: 100%; max-width: 200px;" />
    <p id="modalDesc"></p>
    <div id="modalExtra"></div> <!-- نغير محتواه حسب نوع المودال -->

    <!-- مثال على الألوان -->
    <div class="product-options">
      <label>الألوان المتوفرة:</label>
      <div class="color-options">
        <span class="color-swatch" style="background-color: black;"></span>
        <span class="color-swatch" style="background-color: #183B4E;"></span>
        <span class="color-swatch" style="background-color: pink;"></span>
        <span class="color-swatch" style="background-color: white; border: 1px solid #ccc;"></span>
      </div>

      <label>الأحجام:</label>
      <div class="size-options">
        <button class="size-btn">S</button>
        <button class="size-btn">M</button>
        <button class="size-btn">L</button>
        <button class="size-btn">XL</button>
        <button class="size-btn">2XL</button>
        <button class="size-btn">3XL</button>
        <!-- بعد أزرار الأحجام -->
        <input type="hidden" id="selectedSize" />
        <input type="hidden" id="selectedColor" />

      </div>
    </div>
  </div>
</div>

<script>
function openModal(button, type) {
  const product = button.closest('.product');
  const title = product.getAttribute('data-title');
  const desc = product.getAttribute('data-description');
  const img = product.getAttribute('data-img');
  const priceOld = product.getAttribute('data-price-old');
  const priceNew = product.getAttribute('data-price-new');
  const pid = product.getAttribute('data-pid');
  const colors = product.getAttribute('data-colors');

  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalDesc').textContent = desc;
  document.getElementById('modalImg').src = img;
  document.getElementById('cartPid').value = pid;

  // توليد ألوان حسب المنتج
  if (colors) {
    const colorArray = colors.split(',');
    const colorContainer = document.querySelector('.color-options');
    colorContainer.innerHTML = ''; // حذف الألوان القديمة

    colorArray.forEach(color => {
      const span = document.createElement('span');
      span.classList.add('color-swatch');
      span.style.backgroundColor = color.trim();

      if (color.trim().toLowerCase() === 'white') {
        span.style.border = '1px solid #ccc'; // لتوضيح الأبيض
      }

      span.addEventListener('click', () => {
        document.getElementById('selectedColor').value = color;
        document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
        span.classList.add('selected');
        document.getElementById('cartColor').value = color; // أضف هذا السطر 👈

      });

      colorContainer.appendChild(span);
    });
  }
// ربط أزرار الحجم
document.querySelectorAll('.size-btn').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    button.classList.add('active');
    document.getElementById('selectedSize').value = button.textContent.trim();
    document.getElementById('cartSize').value = button.textContent.trim(); // 👈 مهم جداً
  });
});

  // محتوى السعر والزر
  const modalExtra = document.getElementById('modalExtra');
  if (type === 'buy') {
    modalExtra.innerHTML = `
      <p><strong>السعر القديم:</strong> ${priceOld}</p>
      <p><strong>السعر الجديد:</strong> ${priceNew}</p>
      <button type="button" onclick="addToCart('${pid}')" style="background: green; color: white;">أضف إلى السلة</button>
    `;
  } else {
    modalExtra.innerHTML = '';
  }

  document.getElementById('universalModal').style.display = 'block';
}

</script>
<style>
.size-btn.active,
.color-swatch.selected {
  outline: 2px solid #4b002f;
}
</style>

<script>
function addToCart(pid) {
  const size = document.getElementById('cartSize').value;
  const color = document.getElementById('cartColor').value;

  if (!size || !color) {
    alert("يرجى اختيار اللون والحجم أولاً.");
    return;
  }

  document.getElementById("addToCartForm").submit();
}
</script>


<script>
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');

  // نتحقق إذا المستخدم أتى من المفضلة
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(`.product[data-pid="${pid}"]`);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    // نحذف العلامة بعد الفتح، حتى لا تفتح عند التحديث
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>
<script>
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');

  // نتحقق إذا المستخدم أتى من المفضلة
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(`.product[data-pid="${pid}"]`);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    // نحذف العلامة بعد الفتح، حتى لا تفتح عند التحديث
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>

</body>
  <footer id="footer" style="
  position: relative; /* عادي */
  width: 100%;
  background-color: #51122F;
  padding: 15px 20px;
  color: white;
  font-family: 'Cairo', sans-serif;
  box-shadow: 0 -4px 15px rgba(81, 18, 47, 0.5);
  opacity: 0;  /* مخفي في البداية */
  transition: opacity 0.5s ease;
">
  <div style="
    max-width: 1200px;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: right;
  ">
    <h3 style="margin-bottom: 8px; font-size: 18px;"> تواصل معنا</h3>

    <a href="https://wa.me/972599663279" target="_blank"
       style="
         background-color: white;
         color: #51122F;
         padding: 8px 20px;
         border-radius: 30px;
         font-size: 14px;
         text-decoration: none;
         margin-bottom: 12px;
         transition: transform 0.3s, box-shadow 0.3s;
         box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
       ">
      إرسال رسالة واتساب
    </a>

    <p style="margin: 8px 0 15px; font-size: 14px; color: #f4f4f4;">
      نحن متجر متخصص في بيع الهوديز والملابس بتصاميم مميزة وجودة عالية.
    </p>

    <div style="font-size: 22px; display: flex; gap: 15px;">
      <a href="https://www.instagram.com/anbstore9?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" target="_blank" title="Instagram"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-instagram"></i>
      </a>
      <a href="https://www.facebook.com/profile.php?id=100083607621116&mibextid=ZbWKwL" target="_blank" title="Facebook"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-facebook"></i>
      </a>
      <a href="https://www.tiktok.com/@anbstore9?fbclid=IwY2xjawK-tkVleHRuA2FlbQIxMABicmlkETEzR1l6YVdSM2dydUx4Zm1lAR7g6BJCqbnkGvy9JFTU6T9l0u2Kqg4EYYPPq92KMGMZ_YchKAXPuEaZ9iwtrQ_aem_DKcG3GyDqUnxEM_AIkiTNQ" target="_blank" title="TikTok"
         style="color: white; transition: transform 0.3s;">
        <i class="fab fa-tiktok"></i>
      </a>
    </div>
        <p style="font-size: 12px; color: #ccc; margin-top: 20px;">
  © جميع الحقوق محفوظة - <strong>Bailasan Riyad</strong> 2025
        </p>
  </div>
</footer>

<style>
  footer a:hover {
    transform: translateY(-4px) scale(1.05);
  }
</style>

<script>
  window.addEventListener('scroll', function() {
    const footer = document.getElementById('footer');
    const scrollPosition = window.scrollY + window.innerHeight;
    const pageHeight = document.documentElement.scrollHeight;

    if (scrollPosition >= pageHeight - 100) { 
      // عندما تكون قريب من نهاية الصفحة بـ 100 بكسل
      footer.style.opacity = '1';
    } else {
      footer.style.opacity = '0';
    }
  });
</script>
        </html>
    ''',
                                      pid=pid,
                                      query=query,
                                      section=section,
                                      products=filtered_products)
    else:
        return render_template_string("<p>القسم غير موجود</p>")


# بيانات المنتجات
products_data = [
    {
        "pid": "1",
        "name": "هودي 'دكتور'",
        "price": 69.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc81a667676.png",
        "description": "هودي دكتور"
    },
    {
        "pid": "2",
        "name": "هودي 'المهندس'",
        "price": 69.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843b0e55998.jpg",
        "description": "هودي المهندس"
    },
    {
        "pid": "3",
        "name": "هودي 'بتضلي أنتِ العنوان'",
        "price": 49.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc4a8eba036.png",
        "description": "هودي العنوان"
    },
    {
        "pid": "4",
        "name": "هودي 'معادلة التوجيهي'",
        "price": 49.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc493bd98f0.png",
        "description": "هودي توجيهي"
    },
    {
        "pid": "5",
        "name": "هودي 'الحياة مشوار'",
        "price": 59.99,
        "old_price": 80,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843c98479db.jpg",
        "description": "هودي الحياة"
    },
    {
        "pid": "6",
        "name": "هودي 'Why always me'",
        "price": 69.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7dd71fcb5.png",
        "description": "هودي why"
    },
    {
        "pid": "7",
        "name": "هودي 'أنا ما زلت على قيد الحياة'",
        "price": 59.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7e7a28d72.png",
        "description": "هودي الحياة"
    },
    {
        "pid": "8",
        "name": "هودي 'أنا عزيز الروح'",
        "price": 49.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7c8e1646b.png",
        "description": "هودي عزيز الروح"
    },
    {
        "pid": "9",
        "name": "هودي 'فلسطين مزروعة بالقلب'",
        "price": 59.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc42a07fbf4.png",
        "description": "هودي فلسطين"
    },
    {
        "pid": "10",
        "name": "هودي 'الأمور تحت السيطرة'",
        "price": 59.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7c4862ef1.png",
        "description": "هودي السيطرة"
    },
    {
        "pid": "11",
        "name": "توم & جيري",
        "price": 139.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7b5b607f9.png",
        "description": "هودي زوجي بتصميم توم وجيري"
    },
    {
        "pid": "12",
        "name": "تاريخ مميز باللاتيني",
        "price": 119.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66844047797b4.jpg",
        "description": "هودي تاريخ مميز"
    },
    {
        "pid": "13",
        "name": "لك جناح و لي جناح",
        "price": 129.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843f625e9e4.jpg",
        "description": "هودي جناح"
    },
    {
        "pid": "14",
        "name": "إلى متى يا لوز",
        "price": 139.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843fcd06af6.jpg",
        "description": "هودي لوز"
    },
    {
        "pid": "15",
        "name": "القلب و التاريخ",
        "price": 129.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc46647bcc2.png",
        "description": "هودي قلب"
    },
    {
        "pid": "16",
        "name": "تحقق ما كان بالأمس حلماً",
        "price": 49.99,
        "old_price": 70,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_6684418364991.jpg",
        "description": "هودي حلم"
    },
    {
        "pid": "17",
        "name": "cristiano",
        "price": 44.99,
        "old_price": 70,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_668441cae61ae.jpg",
        "description": "هودي كريستيانو"
    },
    {
        "pid": "18",
        "name": "درسنا لنعمرها",
        "price": 39.99,
        "old_price": 60,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66a90c56065cd.jpg",
        "description": "هودي لنعمرها"
    },
    {
        "pid": "19",
        "name": "فكر خارج الصندوق",
        "price": 39.99,
        "old_price": 60,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_6684411d02014.jpg",
        "description": "هودي الصندوق"
    },
]
# ✅ قائمة موحدة لجميع المنتجات
products = [
    {
        "pid": "1",
        "name": "هودي 'دكتور'",
        "price": 69.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc81a667676.png",
        "description": "هودي دكتور"
    },
    {
        "pid": "2",
        "name": "هودي 'المهندس'",
        "price": 69.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843b0e55998.jpg",
        "description": "هودي المهندس"
    },
    {
        "pid": "3",
        "name": "هودي 'بتضلي أنتِ العنوان'",
        "price": 49.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc4a8eba036.png",
        "description": "هودي العنوان"
    },
    {
        "pid": "4",
        "name": "هودي 'معادلة التوجيهي'",
        "price": 49.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc493bd98f0.png",
        "description": "هودي توجيهي"
    },
    {
        "pid": "5",
        "name": "هودي 'الحياة مشوار'",
        "price": 59.99,
        "old_price": 80,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843c98479db.jpg",
        "description": "هودي الحياة"
    },
    {
        "pid": "6",
        "name": "هودي 'Why always me'",
        "price": 69.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7dd71fcb5.png",
        "description": "هودي why"
    },
    {
        "pid": "7",
        "name": "هودي 'أنا ما زلت على قيد الحياة'",
        "price": 59.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7e7a28d72.png",
        "description": "هودي الحياة"
    },
    {
        "pid": "8",
        "name": "هودي 'أنا عزيز الروح'",
        "price": 49.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7c8e1646b.png",
        "description": "هودي عزيز الروح"
    },
    {
        "pid": "9",
        "name": "هودي 'فلسطين مزروعة بالقلب'",
        "price": 59.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc42a07fbf4.png",
        "description": "هودي فلسطين"
    },
    {
        "pid": "10",
        "name": "هودي 'الأمور تحت السيطرة'",
        "price": 59.99,
        "old_price": 80,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7c4862ef1.png",
        "description": "هودي السيطرة"
    },
    {
        "pid": "11",
        "name": "توم & جيري",
        "price": 139.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc7b5b607f9.png",
        "description": "هودي زوجي بتصميم توم وجيري"
    },
    {
        "pid": "12",
        "name": "تاريخ مميز باللاتيني",
        "price": 119.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66844047797b4.jpg",
        "description": "هودي تاريخ مميز"
    },
    {
        "pid": "13",
        "name": "لك جناح و لي جناح",
        "price": 129.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843f625e9e4.jpg",
        "description": "هودي جناح"
    },
    {
        "pid": "14",
        "name": "إلى متى يا لوز",
        "price": 139.99,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66843fcd06af6.jpg",
        "description": "هودي لوز"
    },
    {
        "pid": "15",
        "name": "القلب و التاريخ",
        "price": 129.99,
        "image":
        "https://images.cdn-files-a.com/uploads/6243106/400_65fc46647bcc2.png",
        "description": "هودي قلب"
    },
    {
        "pid": "16",
        "name": "تحقق ما كان بالأمس حلماً",
        "price": 49.99,
        "old_price": 70,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_6684418364991.jpg",
        "description": "هودي حلم"
    },
    {
        "pid": "17",
        "name": "cristiano",
        "price": 44.99,
        "old_price": 70,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_668441cae61ae.jpg",
        "description": "هودي كريستيانو"
    },
    {
        "pid": "18",
        "name": "درسنا لنعمرها",
        "price": 39.99,
        "old_price": 60,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_66a90c56065cd.jpg",
        "description": "هودي لنعمرها"
    },
    {
        "pid": "19",
        "name": "فكر خارج الصندوق",
        "price": 39.99,
        "old_price": 60,
        "image":
        "https://files.cdn-files-a.com/uploads/6243106/400_6684411d02014.jpg",
        "description": "هودي الصندوق"
    },
]

# ✅ دالة واحدة موحدة فقط


def get_product_by_id(pid):
    pid = str(pid).strip()
    return next((p for p in products if p["pid"] == pid), None)


# ✅ إضافة للمفضلة


@app.route('/add-to-favorites', methods=['POST'])
def add_to_favorites():
    data = request.get_json()
    pid = data.get('pid')
    favorites = session.get('favorites', [])

    product = get_product_by_id(pid)
    if not product:
        return jsonify({'error': 'المنتج غير موجود'}), 404

    if not any(p['pid'] == pid for p in favorites):
        favorites.append(product)

    session['favorites'] = favorites
    session.modified = True
    return jsonify({'message': 'تمت الإضافة إلى المفضلة'})


@app.route('/search')
def search():
    query = request.args.get("q", "").strip().lower()
    filtered = [p for p in products_data
                if query in p["name"].lower()] if query else []

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <meta charset="UTF-8">
        <title>الرئيسية - متجري</title>
        <style>
        body, button, input, select, textarea {
          font-family: 'Cairo', sans-serif;
          margin: 0;
          padding: 0;
          background-color: #E0E0E0;  
        }

        header {
          background-color: #f1f1f2;
          box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
          color: #51122F;
          padding: 15px 30px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .header-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
        }

        .logo {
          font-size: 28px;
          font-weight: bold;
          color: #51122F;
        }

        .search-form {
          display: flex;
          align-items: center;
          background-color: #fff;
          padding: 5px 10px;
          border-radius: 20px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          margin: 0 20px;
        }

        .search-form i {
          color: #888;
          margin-left: 8px;
          font-size: 16px;
        }

        .search-form input[type="text"] {
          padding: 8px 15px;
          border: none;
          border-radius: 20px;
          font-size: 16px;
          outline: none;
          width: 200px;
          background: transparent;
          color: #333;
        }

        nav a {
          color: #51122F;
          margin: 0 15px;
          text-decoration: none;
          font-size: 18px;
        }

        nav a:hover {
          text-decoration: underline;
        }
        .sections {
          text-align: center;
          margin: 50px 20px;
          color:#51122F;
        }

        .sections button {
          padding: 15px 30px;
          margin: 20px;
          font-size: 18px;
          background-color: #51122F;
          color: white;
          border: none;
          border-radius: 25px;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .sections button:hover {
          transform: scale(1.05);
        }
        .price {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 10px;
          margin-top: 10px;
        }

        .old-price {
          text-decoration: line-through;
          color: #888;
          font-size: 16px;
        }

        .new-price {
          color: #b3003b;
          font-size: 20px;
          font-weight: bold;
        }

        .welcome {
          text-align: center;
          margin: 40px 20px;
          font-size: 24px;
          color: #444;
        }
        .content { text-align: center; margin-top: 50px; }
        .store-container { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-top: 30px; }
        .product {   margin: 25px;border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; width: 200px; background:  #fff; }
        .product img { width: 100%; border-radius: 10px; }
        .buy-btn { display: block; margin-top: 10px; background-color: #51122F; color: white; padding: 10px; border: none; border-radius: 5px; text-decoration: none; }
        .buy-btn:hover { background-color:  #51122F; }   
        .sub-bar {
          background-color: #51122F;
          color: white;
          text-align: center;
          padding: 10px;
          font-size: 14px;
          margin: 0;           /* إزالة أي هامش علوي */
          border-top: 1px solid #ffffff22; /* إن أردت حدود خفيفة */
        }                                         

        .modal {
          display: none; /* تكون مخفية بالبداية */
          position: fixed; /* تبقى فوق الصفحة */
          z-index: 1000; /* فوق كل العناصر */
          left: 0; top: 0;
          width: 100%; height: 100%;
          background: rgba(0, 0, 0, 0.5); /* خلفية شفافة سوداء */

        }
    .modal-content {
      font-family: 'Cairo', sans-serif; /* خط عربي جميل */
      font-size: 20px;
      color: #333;
      font-weight: 500;
      line-height: 1.6;
      text-align: center;
      margin: 10% auto;
      margin-top: 20px;
      padding: 20px;
      width: 80%;
      max-width: 500px;
      top: 5vh; /* يجعل البطاقة ترتفع لأعلى (تقدري تعدلي النسبة حسب ما تحبي) */
      border-radius: 10px;
      position: relative;
      background: white;
      max-height: 90vh; /* لا يتعدى 90% من ارتفاع الشاشة */
      overflow-y: auto; /* إضافة تمرير عمودي عند الحاجة */
    }
        .close {
          float: right;
          font-size: 28px;
          cursor: pointer;
        }
          button,
          .details-btn {
            background-color: #4b002f; /* البنفسجي الغامق */
            color: white;
            border: none;
            border-radius: 8px; /* الزوايا ناعمة */
            padding: 10px 15px;
            margin-top: 10px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: 0.3s ease;
          }

          button:hover,
          .details-btn:hover {
            background-color: #6a0044; /* لون أفتح عند المرور */
          }


          .product-options {
            margin-top: 15px;
            text-align: right;
            font-family: 'Cairo', sans-serif;
          }

          .color-options {
            display: flex;
            gap: 10px;
            margin: 10px 0;
            justify-content: right;
          }

    .color-swatch {
      width: 25px;
      height: 25px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid #fff;
      box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
      transition: 0.2s;
    }

    .color-swatch:hover {
      transform: scale(1.1);
      border-color: #4b002f;
    }

    .size-options {
      display: flex;
      gap: 10px;
      justify-content: right;
    }

    .size-btn {
      background-color: #4b002f;
      border: 1px solid #ccc;
      border-radius: 6px;
      padding: 5px 10px;
      cursor: pointer;
      font-size: 14px;
      transition: 0.3s;
    }

    .size-btn:hover {
      background-color: #4b002f;
      color: white;
      border-color: #4b002f;
    }
     .buy-btn {
        padding: 10px 20px;
        background-color: #4b002f;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      }

      button:hover, .buy-btn:hover {
        background-color: #7a1f4d;
      }


    .favorite-icon {
      background:none;
      border: none;
      cursor: pointer;
      font-size: 22px;
      color: #333; /* اللون الأساسي للقلب */
      transition: color 0.3s ease;
    }

    .favorite-icon.active {
      color: #4b002f; /* بنفسجي عند التفعيل */
    }

    .favorite-icon {
      background: transparent;   /* بدون خلفية */
      border: none;              /* بدون إطار */
      cursor: pointer;
      padding: 0;                /* بدون حواف */
      font-size: 22px;
      transition: color 0.3s;
       margin-top: 16px;  /* عدّلي الرقم حسب المسافة اللي بدك إياها */
    }
    .favorite-icon:hover,
    .favorite-icon:focus,
    .favorite-icon:active {
      box-shadow: none;                    /* يمنع أي ظل */
      outline: none;                       /* لا يظهر إطار عند التحديد */
    }
    .favorite-icon.favorited {
    color: #4b002f;
    }


    .products-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  align-items: flex-start
}

.product {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 250px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

* {
  box-sizing: border-box;
}
  </style>

<script>
function toggleFavorite(icon) {
  // ✅ يبدّل شكل القلب بين مملوء وفارغ
  icon.classList.toggle('fa-regular'); // القلب الفارغ
  icon.classList.toggle('fa-solid');   // القلب المملوء

  // ✅ يضيف أو يزيل كلاس favorited
  icon.classList.toggle('favorited');

  // ✅ تحديد المنتج من HTML
  const product = icon.closest('.product');
  const pid = product.getAttribute('data-pid');

  // ✅ إذا كان مفضل أو لا (بعد التبديل)
  const isFavorited = icon.classList.contains('favorited');

  // ✅ إرسال طلب إلى السيرفر حسب الحالة
  fetch(isFavorited ? '/add-to-favorites' : '/remove-from-favorites', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ pid: pid })
  }).then(response => {
    if (!response.ok) {
      alert('حدث خطأ أثناء تعديل حالة المفضلة.');
    } else {
      // ✅ إذا المستخدم في صفحة المفضلات ونزع المنتج من المفضلة، احذفه من الواجهة
      if (!isFavorited && window.location.pathname === '/favorites') {
        product.remove();
      }
    }
  });
}
</script>

<body>

      <header>
      <div class="header-container">
      <div class="logo">ANB store</div>

      <nav>
        <a href="/" title="الرئيسية"><i class="fas fa-home"></i></a>
        <a href="/cart" title="السلة"><i class="fas fa-shopping-cart"></i></a>
        <a href="/favorites" title=" المفضلة"><i class="fas fa-heart"></i></a>

      </nav>
      </div>
      </header>

      <div class="side-box">
      <div class="sub-bar"> التوصيل مجاني للطلبات فوق 300 شيكل !</div>
      </div>
      </div>
      <div class="content">

        <h2>نتائج البحث</h2>
        <div class="store-container">

<form id="addToCartForm" action="/add-to-cart" method="post" style="display: none;">
  <input type="hidden" name="pid" id="cartPid">
  <input type="hidden" name="color" id="cartColor">
  <input type="hidden" name="size" id="cartSize">
  <input type="hidden" name="quantity" value="1">

</form>                                   

        <meta charset="UTF-8">
{% if products %}
  <div class="products-container" style="display: flex; flex-wrap: wrap; gap: 20px;">
    {% for product in products %}
      <div class="product" 
           data-pid="{{ product.pid }}"
           data-title="{{ product.name }}"
           data-description="{{ product.description }}"
           data-price-old="₪{{ product.old_price }}"
           data-price-new="₪{{ product.price }}"
           data-img="{{ product.image }}"
           style="background: #fff; border-radius: 10px; padding: 15px; width: 250px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">

        <img src="{{ product.image }}" alt="منتج" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
        <h3 style="font-size: 18px; margin: 10px 0;">{{ product.name }}</h3>
        <div class="price" style="margin-bottom: 10px;">
          <span class="old-price" style="text-decoration: line-through; color: gray;">₪{{ product.old_price }}</span>
          <span class="new-price" style="color: green; margin-right: 10px;">₪{{ product.price }}</span>
        </div>

        <button onclick="openModal(this, 'details')" style="margin-bottom: 5px;">عرض التفاصيل</button>
        <button class="buy-btn" onclick="openModal(this, 'buy')" style=margin-bottom: 5px;">شراء الآن</button>
        <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this, '{{ product.pid }}')" style="cursor: pointer; margin-top: 10px; display: inline-block;"></i>
      </div>
    {% endfor %}
  </div>
{% else %}
  <p>لا يوجد منتجات مطابقة.</p>
{% endif %}
<div id="universalModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="document.getElementById('universalModal').style.display='none'">&times;</span>
    <h2 id="modalTitle"></h2>
    <img id="modalImg" style="width: 100%; max-width: 200px;" />
    <p id="modalDesc"></p>
    <div id="modalExtra"></div> <!-- نغير محتواه حسب نوع المودال -->

    <!-- مثال على الألوان -->
    <div class="product-options">
      <label>الألوان المتوفرة:</label>
      <div class="color-options">
        <span class="color-swatch" style="background-color: black;"></span>
        <span class="color-swatch" style="background-color: #183B4E;"></span>
        <span class="color-swatch" style="background-color: pink;"></span>
        <span class="color-swatch" style="background-color: white; border: 1px solid #ccc;"></span>
      </div>

      <label>الأحجام:</label>
      <div class="size-options">
        <button class="size-btn">S</button>
        <button class="size-btn">M</button>
        <button class="size-btn">L</button>
        <button class="size-btn">XL</button>
        <button class="size-btn">2XL</button>
        <button class="size-btn">3XL</button>
        <!-- بعد أزرار الأحجام -->
        <input type="hidden" id="selectedSize" />
        <input type="hidden" id="selectedColor" />

      </div>
    </div>
  </div>
</div>

<script>
function openModal(button, type) {
  const product = button.closest('.product');
  const title = product.getAttribute('data-title');
  const desc = product.getAttribute('data-description');
  const img = product.getAttribute('data-img');
  const priceOld = product.getAttribute('data-price-old');
  const priceNew = product.getAttribute('data-price-new');
  const pid = product.getAttribute('data-pid');
  const colors = product.getAttribute('data-colors');

  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalDesc').textContent = desc;
  document.getElementById('modalImg').src = img;
  document.getElementById('cartPid').value = pid;

  // توليد ألوان حسب المنتج
  if (colors) {
    const colorArray = colors.split(',');
    const colorContainer = document.querySelector('.color-options');
    colorContainer.innerHTML = ''; // حذف الألوان القديمة

    colorArray.forEach(color => {
      const span = document.createElement('span');
      span.classList.add('color-swatch');
      span.style.backgroundColor = color.trim();

      if (color.trim().toLowerCase() === 'white') {
        span.style.border = '1px solid #ccc'; // لتوضيح الأبيض
      }

      span.addEventListener('click', () => {
        document.getElementById('selectedColor').value = color;
        document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
        span.classList.add('selected');
        document.getElementById('cartColor').value = color; // أضف هذا السطر 👈

      });

      colorContainer.appendChild(span);
    });
  }

  // محتوى السعر والزر
  const modalExtra = document.getElementById('modalExtra');
  if (type === 'buy') {
    modalExtra.innerHTML = `
      <p><strong>السعر القديم:</strong> ${priceOld}</p>
      <p><strong>السعر الجديد:</strong> ${priceNew}</p>
      <button type="button" onclick="addToCart('${pid}')" style="background: green; color: white;">أضف إلى السلة</button>
    `;
  } else {
    modalExtra.innerHTML = '';
  }

  document.getElementById('universalModal').style.display = 'block';
}

</script>
<style>
.size-btn.active,
.color-swatch.selected {
  outline: 2px solid #4b002f;
}
</style>

<script>
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const pid = urlParams.get('pid');

  // نتحقق إذا المستخدم أتى من المفضلة
  const fromFavorites = sessionStorage.getItem('fromFavorites');

  if (pid && fromFavorites === '1') {
    const product = document.querySelector(`.product[data-pid="${pid}"]`);
    if (product) {
      const button = product.querySelector('.buy-btn');
      if (button) {
        openModal(button, 'buy');
      }
    }
    // نحذف العلامة بعد الفتح، حتى لا تفتح عند التحديث
    sessionStorage.removeItem('fromFavorites');
  }
};
</script>

    </body>
    </html>
    ''',products=filtered,query=query)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = session.get('cart', [])
    total = 0.0

    # نحسب المجموع الكلي تلقائيًا
    for item in cart_items:
        try:
            price = float(item.get('price', 0))
            quantity = int(item.get('quantity', 1))
            total += price * quantity
        except:
            pass

    template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="UTF-8">
        <title>🛒 سلة المشتريات</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
        <style>
            /* التنسيقات كما هي */
            body { font-family: 'Cairo', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
            header { background-color: #f1f1f2; box-shadow: 0 4px 10px rgba(0,0,0,0.1); padding: 15px 30px; color: #51122F; display: flex; justify-content: space-between; align-items: center; }
            .logo { font-size: 24px; font-weight: bold; }
            nav a { color: #51122F; margin: 0 10px; text-decoration: none; font-size: 18px; }
            nav a:hover { text-decoration: underline; }
            .container { padding: 30px; }
            h1 { text-align: center; color: #333; margin-bottom: 30px; }
            table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
            th { background-color: #eee; color: #444; }
            td form { margin: 0; }
            .total { font-size: 20px; font-weight: bold; color: #4b002f; text-align: center; margin-top: 20px; }
            .actions { text-align: center; margin-top: 20px; }
            .actions a, .actions button {
                text-decoration: none; color: white; background-color: #4b002f; padding: 10px 20px; border-radius: 8px;
                margin: 5px; display: inline-block; border: none; cursor: pointer; transition: background 0.3s ease;
                font-family: 'Cairo', sans-serif;
            }
            .actions a:hover, .actions button:hover { background-color: #7a1f4d; }
            @media (max-width: 768px) {
                table, th, td { font-size: 14px; }
                .logo { font-size: 20px; }
                nav a { font-size: 16px; }
            }
        </style>
    </head>
    <body>
    <header>
        <div class="logo">ANB store</div>
        <nav>
            <a href="/"><i class="fas fa-home"></i></a>
            <a href="/cart"><i class="fas fa-shopping-cart"></i></a>
            <a href="/favorites"><i class="fas fa-heart"></i></a>
        </nav>
    </header>

    <div class="container">
        <h1>🛒 سلة المشتريات</h1>

        {% if cart_items %}
            <table>
                <tr>
                    <th>المنتج</th>
                    <th>اللون</th>
                    <th>الحجم</th>
                    <th>الكمية</th>
                    <th>السعر</th>
                    <th>المجموع الفرعي</th>
                    <th>إجراء</th>
                </tr>
                {% for item in cart_items %}
                    {% set price = item['price']|float %}
                    {% set quantity = item['quantity']|int %}
                    {% set name = item['name'] if 'name' in item else 'منتج غير معروف' %}
                    {% set subtotal = price * quantity %}
                    <tr>
                        <td>{{ name }}</td>
                        <td>{{ item['color'] or 'غير محدد' }}</td>
                        <td>{{ item['size'] or 'غير محدد' }}</td>
                        <td>
                            <form action="/update-cart/{{ loop.index0 }}" method="post">
                                <input type="number" name="quantity" value="{{ quantity }}" min="1" style="width:50px;" required>
                                <button type="submit">🔄</button>
                            </form>
                        </td>
                        <td>{{ "%.2f"|format(price) }} شيكل</td>
                        <td>{{ "%.2f"|format(subtotal) }} شيكل</td>
                        <td>
                            <form action="/remove-from-cart/{{ loop.index0 }}" method="post" style="display:inline;">
                                <button type="submit">❌</button>
                            </form>
                        </td>
                    </tr>
                {% endfor %}
            </table>

            <p class="total">💰 المجموع الكلي: {{ "%.2f"|format(total) }} شيكل</p>

        {% else %}
            <p style="text-align:center;">السلة فارغة 🕸️</p>
        {% endif %}

        <div class="actions">
            <a href="/clear">🗑️ إفراغ السلة</a>
            <a href="/">🏬 الرجوع للمتجر</a>
            <a href="/checkout" class="actions">📦 استكمال الطلب</a>
        </div>
    </div>
    </body>
    </html>
    """

    return render_template_string(template, cart_items=cart_items, total=total)


# ✅ دالة تعديل الكمية
@app.route('/update-cart/<int:index>', methods=['POST'])
def update_cart(index):
    quantity = request.form.get('quantity')
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except:
        quantity = 1

    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart[index]['quantity'] = quantity
        session['cart'] = cart
        session.modified = True

    return redirect('/cart')


@app.route('/remove-from-cart/<int:index>', methods=['POST'])
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session['cart'] = cart
        session.modified = True

    return redirect(url_for('cart'))


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    pid = request.form.get('pid')
    print(f"Received pid: {pid}")  # DEBUG

    if not pid:
        return "معرف المنتج غير موجود", 400

    color = request.form.get('color')
    size = request.form.get('size')
    
    try:
        quantity = int(request.form.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    product = get_product_by_id(pid)

    if not product:
        return "المنتج غير موجود", 404

    item = {
        'pid': pid,
        'name': product['name'],
        'price': product['price'],
        'color': color,
        'size': size,
        'quantity': quantity
    }

    cart = session.get('cart', [])
    cart.append(item)
    session['cart'] = cart
    session.modified = True

    print("🛒 Current Cart:", session['cart'])
    return redirect(url_for('cart'))


@app.route('/clear')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', [])
    if not cart:
        return redirect('/cart')

    delivery_price = 0
    total = sum(float(item['price']) * int(item['quantity']) for item in cart)

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        region = request.form.get('region')
        payment_method = request.form.get('payment')
        notes = request.form.get('notes')

        if region == 'الضفة الغربية':
            delivery_price = 20
        elif region == 'القدس':
            delivery_price = 30
        elif region == 'الداخل المحتل':
            delivery_price = 50

        total += delivery_price

        with open('orders_new.txt', 'a', encoding='utf-8') as f:
            f.write("=== طلب جديد ===\n")
            f.write(f"الاسم: {name}\n")
            f.write(f"رقم الواتساب: {phone}\n")
            f.write(f"العنوان: {address}\n")
            f.write(f"طريقة الدفع: {payment_method}\n")
            f.write(f"منطقة التوصيل: {region}\n")
            f.write(f"ملاحظات: {notes or 'لا يوجد'}\n")
            f.write("المنتجات:\n")
            for item in cart:
                f.write(
                    f"- {item['name']}، الحجم: {item.get('size', 'غير محدد')}، اللون: {item.get('color', 'غير محدد')}، الكمية: {item['quantity']}، السعر: {item['price']} شيكل\n"
                )
            f.write(f"رسوم التوصيل: {delivery_price} شيكل\n")
            f.write(f"المجموع الكلي: {total} شيكل\n")
            f.write("==================\n\n")

        return render_template_string("""
              <!DOCTYPE html>
              <html lang="ar" dir="rtl">
              <head>
                 <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
                  <meta charset="UTF-8">
                  <title>تم استلام الطلب</title>
                  <style>
                      body {
                          font-family: 'Cairo', sans-serif;
                          background-color: #f9f9f9;
                          padding: 40px;
                          text-align: center;
                          color: #333;
                      }
                      .box {
                          background-color: #fff;
                          border-radius: 15px;
                          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                          padding: 30px;
                          max-width: 500px;
                          margin: auto;

                      }
                      h2 {
                          color: #4CAF50;
                          margin-bottom: 20px;
                      }
                      p {
                          font-size: 18px;
                          margin-bottom: 10px;
                      }
                      a {
                          display: inline-block;
                          margin-top: 20px;
                          padding: 10px 20px;
                          background-color: #4CAF50;
                          color: white;
                          text-decoration: none;
                          border-radius: 8px;
                          transition: background-color 0.3s;
                      }
                      a:hover {
                          background-color: #45a049;
                      }
                  </style>
              </head>
              <body>
                  <div class="box">
                      <h2>✅ تم استلام الطلب بنجاح</h2>
                      <p>شكرًا لك {{ name }}! طلبك قيد المعالجة وسنتواصل معك قريبًا عبر واتساب.</p>
                      <p>📦 سيتم التوصيل إلى: {{ address }}</p>
                      <p>💵 طريقة الدفع: {{ payment_method }}</p>
                      <p>🚚 منطقة التوصيل: {{ delivery_method }}</p>
                      <p>📝 ملاحظات: {{ notes or 'لا يوجد' }}</p>
                      <p>💰 المبلغ الإجمالي: {{ total }} شيكل</p>
                      <a href="/">العودة للمتجر</a>
                  </div>
          webhook_url = "https://hooks.zapier.com/hooks/catch/23486054/uo015mm/"

requests.post(webhook_url, json={
    "name": name,
    "phone": phone,
    "address": address,
    "region": region,
    "payment": payment_method,
    "notes": notes,
    "total": total,
    "products": cart
})
              </body>
              </html>
              """,
                                      name=name,
                                      address=address,
                                      payment_method=payment_method,
                                      delivery_method=region,
                                      total=total,
                                      notes=notes)

    return render_template_string("""
        <!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    <title>📦 استكمال الطلب</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Cairo', sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        .checkout-container {
            background-color: white;
            max-width: 600px;
            margin: auto;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        h2 {
            text-align: center;
            color: #51122F;
            margin-bottom: 25px;
        }
        label {
            font-weight: bold;
            display: block;
            margin-bottom: 5px;
            color: #333;
        }
        input, select, textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-family: 'Cairo', sans-serif;
        }
        button {
            background-color: #51122F;
            color: white;
            padding: 12px;
            width: 100%;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #7a1f4d;
        }
        .summary {
            text-align: center;
            margin-top: 30px;
            font-size: 18px;
            color: #444;
        }
    </style>
</head>
<body>

<div class="checkout-container">
    <h2>📦 استكمال الطلب</h2>
    <form method="post">
        <label for="name">الاسم الكامل:</label>
        <input type="text" name="name" id="name" required>

        <label for="address">العنوان الكامل:</label>
        <input type="text" name="address" id="address" required>

        <label for="phone">رقم الواتساب:</label>
        <input type="text" name="phone" id="phone" required>

        <label for="region">منطقة التوصيل:</label>
        <select name="region" id="region" required>
            <option value="الضفة الغربية">الضفة الغربية (+20 شيكل)</option>
            <option value="القدس">القدس (+30 شيكل)</option>
            <option value="الداخل المحتل">الداخل المحتل (+50 شيكل)</option>
        </select>

        <label for="payment">طريقة الدفع:</label>
        <select name="payment" id="payment" required>
            <option value="الدفع عند الاستلام">الدفع عند الاستلام</option>
            <option value="الدفع عن طريق بطاقة ريفليكت">الدفع عن طريق بطاقة ريفليكت</option>
        </select>

        <label for="notes">ملاحظات إضافية:</label>
        <textarea name="notes" id="notes" rows="4" placeholder="اكتب أي تفاصيل إضافية هنا..."></textarea>

        <button type="submit">✅ تأكيد الطلب</button>
    </form>
</div>

</body>
</html>
    """)


# دالة بسيطة لإرجاع منتج حسب pid


def add_to_favorites():

    data = request.get_json()
    pid = data.get('pid')
    favorites = session.get('favorites', [])

    product = get_product_by_id(pid)
    if not product:
        return jsonify({'error': 'المنتج غير موجود'}), 404
    if not any(p['pid'] == pid for p in favorites):
        favorites.append(product)

    session['favorites'] = favorites
    session.modified = True
    return jsonify({'message': 'تمت الإضافة إلى المفضلة'})


@app.route('/favorites')
def show_favorites():
    favorites = session.get('favorites', [])
    return render_template_string(template, favorites=favorites)


@app.route('/remove-from-favorites', methods=['POST'])
def remove_from_favorites():

    data = request.get_json()
    pid = data.get('pid')
    favorites = session.get('favorites', [])

    favorites = [p for p in favorites if p['pid'] != pid]
    session['favorites'] = favorites
    return jsonify({'success': True})


template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta charset="UTF-8">
  <title>المفضلة</title>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <style>

            /* التنسيقات كما هي */
            body { font-family: 'Cairo', sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }
            header { background-color: #f1f1f2; box-shadow: 0 4px 10px rgba(0,0,0,0.1); padding: 15px 30px; color: #51122F; display: flex; justify-content: space-between; align-items: center; }
            .logo { font-size: 24px; font-weight: bold; }
            nav a { color: #51122F; margin: 0 10px; text-decoration: none; font-size: 18px; }
            nav a:hover { text-decoration: underline; }
.container {
  max-width: 1100px;
  margin: auto;
  padding: 30px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
}
            h2 { text-align: center; color: #333; margin-bottom: 30px; }
            table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
            th { background-color: #eee; color: #444; }
            td form { margin: 0; }
            .total { font-size: 20px; font-weight: bold; color: #4b002f; text-align: center; margin-top: 20px; }
            .actions { text-align: center; margin-top: 20px; }
            .actions a, .actions button {
                text-decoration: none; color: white; background-color: #4b002f; padding: 10px 20px; border-radius: 8px;
                margin: 5px; display: inline-block; border: none; cursor: pointer; transition: background 0.3s ease;
                font-family: 'Cairo', sans-serif;
            }
            .actions a:hover, .actions button:hover { background-color: #7a1f4d; }
            @media (max-width: 768px) {
                table, th, td { font-size: 14px; }
                .logo { font-size: 20px; }
                nav a { font-size: 16px; }
            }

    .product-container {
      background: white;
      border: 1px solid #ddd;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.08);
      overflow: hidden;
      width: 220px;
      transition: transform 0.3s;
      position: relative;
    }

    .product-container:hover {
      transform: translateY(-5px);
    }

    .product-container a {
      text-decoration: none;
      color: inherit;
    }

    .product {
      text-align: center;
      padding: 15px;
    }

    .product img {
      width: 100%;
      border-radius: 8px;
      max-height: 200px;
      object-fit: cover;
    }

    .product h3 {
      font-size: 16px;
      margin: 10px 0 5px;
    }

    .product p {
      font-size: 14px;
      color: #555;
      margin: 5px 0;
    }

    .delete-favorite {
      position: absolute;
      top: 5px;
      right: 5px;
      background: #c0392b;
      color: white;
      border: none;
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 13px;
      z-index: 10;
      transition: background-color 0.3s;
    }

    .delete-favorite:hover {
      background-color: #a93226;
    }

    .no-favorites {
      text-align: center;
      font-size: 18px;
      color: #777;
      padding: 60px;
    }
  </style>
</head>
<body>

    <header>
        <div class="logo">ANB store</div>
        <nav>
            <a href="/"><i class="fas fa-home"></i></a>
            <a href="/cart"><i class="fas fa-shopping-cart"></i></a>
            <a href="/favorites"><i class="fas fa-heart"></i></a>
        </nav>
    </header>
  <h2>منتجاتك المفضلة </h2>
  <div class="container">
    {% for product in favorites %}
    {% set section = (
      'clothes' if product.pid in ['1','2','3','4','5','6','7','8','9','10']
      else 'couples' if product.pid in ['11','12','13','14','15']
      else 'T-SHIRT' if product.pid in ['16','17','18','19']
      else 'clothes'
    ) %}
    <div class="product-container">
      <button class="delete-favorite">حذف</button>
      <a href="/products?section={{ section }}&pid={{ product.pid }}" onclick="sessionStorage.setItem('fromFavorites', '1')">
        <div class="product" data-pid="{{ product.pid }}">
          <img src="{{ product.image }}" alt="صورة المنتج">
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <p>السعر: ₪{{ product.price }}</p>
        </div>
      </a>
    </div>
    {% else %}
    <p class="no-favorites">لا توجد منتجات مفضلة حتى الآن.</p>
    {% endfor %}
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', function() {
      document.querySelectorAll('.delete-favorite').forEach(button => {
        button.addEventListener('click', function(event) {
          event.stopPropagation();
          const container = this.parentElement;
          const productDiv = container.querySelector('.product');
          const pid = productDiv.getAttribute('data-pid');

          fetch('/remove-from-favorites', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pid: pid })
          }).then(response => {
            if (response.ok) {
              container.remove();
            } else {
              alert('حدث خطأ أثناء حذف المنتج من المفضلات.');
            }
          }).catch(err => {
            alert('فشل الاتصال بالسيرفر.');
            console.error(err);
          });
        });
      });
    });
  </script>
</body>

</html>
"""


@app.route('/submit-order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    whatsapp = request.form.get('whatsapp')
    address = request.form.get('address')
    payment_method = request.form.get('payment_method')
    delivery_method = request.form.get('delivery_method')
    cart_items = session.get('cart', [])
    delivery_fee = 0

    if delivery_method == 'الضفة الغربية':
        delivery_fee = 20
    elif delivery_method == 'القدس':
        delivery_fee = 35
    elif delivery_method == 'الداخل المحتل':
        delivery_fee = 65

    total = delivery_fee
    order_details = []

    for item in cart_items:
        price = float(item.get('price', 0))
        quantity = int(item.get('quantity', 1))
        subtotal = price * quantity
        total += subtotal
        order_details.append(
            f"- {item.get('name', 'منتج')}، الحجم {item.get('size', 'غير محدد')}، اللون {item.get('color', 'غير محدد')}، الكمية: {quantity}، السعر: {price} شيكل، المجموع الفرعي: {subtotal} شيكل"
        )

    with open('orders.txt', 'a', encoding='utf-8') as f:
        f.write("=== طلب جديد ===\n")
        f.write(f"الاسم: {name}\n")
        f.write(f"رقم الواتساب: {whatsapp}\n")
        f.write(f"العنوان: {address}\n")
        f.write(f"طريقة الدفع: {payment_method}\n")
        f.write(f"طريقة التوصيل: {delivery_method}\n")
        f.write("المنتجات:\n")
        for line in order_details:
            f.write(line + "\n")
        f.write(f"رسوم التوصيل: {delivery_fee} شيكل\n")
        f.write(f"المجموع الكلي: {total} شيكل\n")
        f.write("==================\n\n")

    # ممكن تمسح السلة بعد الطلب
    session.pop('cart', None)

    return "تم استلام الطلب بنجاح! شكرًا لك."

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)