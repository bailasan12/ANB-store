   elif section == "cables":


      return render_template_string('''

        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;700&display=swap" rel="stylesheet">  <meta charset="UTF-8">
        <meta charset="UTF-8">
        <title>الرئيسية - متجري</title>
        <style>
                                    
        body, button, input, select, textarea {
          font-family: 'Cairo', sans-serif;
          margin: 0;
          padding: 0;
          background-color: #E0E0E0;
        }
                                    
        .image-wrapper {
          position: relative;
          width: 100%;
        }

        .image-wrapper img {
          width: 100%;
          border-radius: 10px;
        }
                                    
        .arrow {
          position: absolute;
          top:25%;
          transform: translateY(-50%);
          font-size: 20px;
          color: white;
          background-color: transparent;
          border: none;
          cursor: pointer;
          padding: 5px 10px;
          z-index:2;
          border-radius: 5px;
        }
                                    
        .arrow.left {
          left: 5px;
        }
                                    
        .arrow.right {
          right:5px;
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
          height: 450px; /* تجعل كل الكروت بنفس الارتفاع */
          justify-content: space-between; /* يوزع المحتوى بالتساوي */
          display: flex;
          flex-direction: column;
        }

        .container {
          position: relative;
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
        .product {   margin: 25px;border: 1px solid #ddd; padding: 15px; border-radius: 10px; text-align: center; width: 200px; background:  #fff; }
        .product img { width: 100%; border-radius: 10px; }
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

        <script>
          function showImage(productId, direction) {
          let images = window["images_" + productId];
          let index = window["index_" + productId];

          index = (index + direction + images.length) % images.length;
          document.getElementById("img_" + productId).src = images[index];

          window["index_" + productId] = index;
          }

          // تحضير الصور للمنتجات
          window.onload = function() {
          window.images_hoodie1 = [
          "https://images.cdn-files-a.com/uploads/6243106/400_65fc7b5b607f9.png",
          "https://images.cdn-files-a.com/uploads/6243106/400_65fc7b4d29542.png"
          ];
          window.index_hoodie1 = 0;

          window.images_hoodie2 = [
          "https://files.cdn-files-a.com/uploads/6243106/400_66844047797b4.jpg",
          "https://files.cdn-files-a.com/uploads/6243106/400_66844047797b4.jpg"
          ];
          window.index_hoodie2 = 0; 
                                    
          window.images_hoodie3 = [
          "https://files.cdn-files-a.com/uploads/6243106/400_66843f625e9e4.jpg",
          "https://files.cdn-files-a.com/uploads/6243106/400_66843f625e9e4.jpg"
          ];
          window.index_hoodie3 = 0; 

          window.images_hoodie4 = [
          "https://images.cdn-files-a.com/uploads/6243106/400_65fc46647bcc2.png",
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
    
          };
                                    
          function toggleFavorite(icon) {
          icon.classList.toggle('favorited');
          icon.classList.toggle('fa-regular'); // القلب الفارغ
          icon.classList.toggle('fa-solid');   // القلب المملوء
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
    <a href="#" title="اتصل بنا"><i class="fas fa-phone-alt"></i></a>
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
      <div class="store-container">
              
      <div class="products-container">
      <div class="product-card">
      <div class="container">
      <div class="image-wrapper"> 
      <button class="arrow right" onclick="showImage('hoodie1', 1)">&#x276E;</button>
      <img id="img_hoodie1" src="/static/hoodie_black_1.jpg">
      <button class="arrow left" onclick="showImage('hoodie1', -1)">&#x276F;</button>
      <h3>هودي " توم & جيري  " </h3>
      <p>₪140</p>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'11')"></i>
                                    
      </div>
      </div>
      </div>  
      </div>
                                    
              
      <div class="product-card">
      <div class="container">
      <div class="image-wrapper">
      <button class="arrow right" onclick="showImage('hoodie2', 1)">&#x276E;</button>
      <img id="img_hoodie2" src="/static/hoodie_black_1.jpg">
      <button class="arrow left" onclick="showImage('hoodie2', -1)">&#x276F;</button>
      <h3>هودي " تاريخك المميز باللاتيني  " </h3>
      <div class="price">
      <span class="old-price">₪164.99</span>
      <span class="new-price">₪119.99</span>
      </div>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'12')"></i>
                                    
      </div>
      </div>
      </div>
                                    
      <div class="product-card">
      <div class="container">
      <div class="image-wrapper">
      <button class="arrow right" onclick="showImage('hoodie3', 1)">&#x276E;</button>
      <img id="img_hoodie3" src="/static/hoodie_black_1.jpg">
      <button class="arrow left" onclick="showImage('hoodie3', -1)">&#x276F;</button>
      <h3>هودي " لك جناح ولي جناح  " </h3>
      <p>₪140</p>
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'13')"></i>
                                    
      </div>
      </div>
      </div>
                                    
      <div class="product-card">
      <div class="container">
      <div class="image-wrapper">
      <button class="arrow right" onclick="showImage('hoodie4', 1)">&#x276E;</button>
      <img id="img_hoodie4" src="/static/hoodie_black_1.jpg">
      <button class="arrow left" onclick="showImage('hoodie4', -1)">&#x276F;</button>
      <h3>هودي " القلب و التاريخ  " </h3>
      <div class="price">
      <span class="old-price">₪149.99</span>
      <span class="new-price">₪119.99</span>
      </div>
                    
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'14')"></i>
                                    
       </div>
       </div>
       </div>

       <div class="product-card">
       <div class="container">
       <div class="image-wrapper">
        data-pid="15" 
                 data-title="هودي إلى متى يا لوز" 
                 data-description="هودي زوجي بتصميم مميز - قماش قطني عالي الجودة" 
                 data-price-old="₪170" 
                 data-price-new="₪129.99">
       <button class="arrow right" onclick="showImage('hoodie5', 1)">&#x276E;</button>
       <img id="img_hoodie5" src="/static/hoodie_black_1.jpg">
       <button class="arrow left" onclick="showImage('hoodie5', -1)">&#x276F;</button>
       <h3>هودي " إلى متى يا لوز " </h3>
       <div class="price">
       <span class="old-price">₪170</span>
       <span class="new-price">₪129.99</span>
       </div>
                  
  <button onclick="openModal(this, 'details')">عرض التفاصيل</button>
  <button class="buy-btn" onclick="openModal(this, 'buy')">شراء الآن</button>
  <i class="fa-regular fa-heart favorite-icon" onclick="toggleFavorite(this,'15')"></i>
                                    
       </div>
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

  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalDesc').textContent = desc;
  document.getElementById('modalImg').src = img;
  document.getElementById('cartPid').value = pid;


  const modalExtra = document.getElementById('modalExtra');
  if (type === 'buy') {
    modalExtra.innerHTML = 
      <p><strong>السعر القديم:</strong> ${priceOld}</p>
      <p><strong>السعر الجديد:</strong> ${priceNew}</p>
  <button type="button" onclick="addToCart('${pid}')" style="background: green; color: white;">أضف إلى السلة</button>
;
  } else {
    modalExtra.innerHTML = '';
  }

  document.getElementById('universalModal').style.display = 'block';
}

function addToCart(pid) {
    console.log("Adding product with pid:", pid);
  const size = document.getElementById('selectedSize').value;
  const color = document.getElementById('selectedColor').value;

  if (!size || !color) {
    alert("يرجى اختيار الحجم واللون قبل الشراء.");
    return;
  }

  document.getElementById('cartPid').value = pid;
  document.getElementById('cartColor').value = color;
  document.getElementById('cartSize').value = size;

  document.getElementById('addToCartForm').submit();
}
function closeModal() {
  document.getElementById('universalModal').style.display = 'none';
}
</script>

<script>
document.querySelectorAll('.size-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.getElementById('selectedSize').value = btn.textContent;
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

document.querySelectorAll('.color-swatch').forEach(swatch => {
  swatch.addEventListener('click', () => {
    const color = swatch.style.backgroundColor;
    document.getElementById('selectedColor').value = color;
    document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
    swatch.classList.add('selected');
  });
});
</script>

<script>
document.querySelectorAll('.size-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.getElementById('selectedSize').value = btn.textContent;
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

document.querySelectorAll('.color-swatch').forEach(swatch => {
  swatch.addEventListener('click', () => {
    const color = swatch.style.backgroundColor;
    document.getElementById('selectedColor').value = color;
    document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('selected'));
    swatch.classList.add('selected');
  });
});
                                    
  
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
    </body>
    </html>''', pid=pid, query=query, products=products, section=section)