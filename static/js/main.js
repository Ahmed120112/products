// فتح/إغلاق الكارت مع دفع الصفحة
$('#cartButton').on('click', function () {
    $('#cartSidebar').toggleClass('active'); // فتح/إغلاق الكارت
    if ($('#cartSidebar').hasClass('active')) {
        $('body').addClass('cart-open'); // دفع الصفحة
    } else {
        $('body').removeClass('cart-open'); // إرجاع الصفحة لوضعها الطبيعي
    }
});

// إغلاق الكارت فقط
$('#closeCart').on('click', function () {
    $('#cartSidebar').removeClass('active'); // إغلاق الكارت
    $('body').removeClass('cart-open'); // إرجاع الصفحة لوضعها الطبيعي
});

// إضافة منتج إلى السلة
function addToCart(productId) {
    $.ajax({
        url: '/api/cart', // تحديث الرابط ليتماشى مع API
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId }),
        success: function (cartData) {
            updateCart(cartData); // تحديث محتويات الكارت
            $('#cartSidebar').addClass('active'); // فتح الكارت تلقائيًا
            $('body').addClass('cart-open'); // دفع الصفحة تلقائيًا
        },
        error: function (xhr) {
            alert('Error: ' + xhr.responseJSON.error);
        }
    });
}

// زيادة الكمية لمنتج معين
function increaseQuantity(productId) {
    $.ajax({
        url: '/api/cart', // تحديث الرابط ليتماشى مع API
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId }),
        success: function (cartData) {
            updateCart(cartData); // تحديث محتويات الكارت
        },
        error: function (xhr) {
            alert('Error: ' + xhr.responseJSON.error);
        }
    });
}

// تقليل الكمية لمنتج معين
function decreaseQuantity(productId) {
    $.ajax({
        url: `/api/cart/${productId}`, // تحديث الرابط ليتماشى مع API
        type: 'DELETE',
        success: function (cartData) {
            updateCart(cartData); // تحديث محتويات الكارت
        },
        error: function (xhr) {
            alert('Error: ' + xhr.responseJSON.error);
        }
    });
}

// تحديث محتويات الكارت
function updateCart(cartData) {
    const cartItems = $('#cartItems');
    cartItems.empty();
    let totalPrice = 0;

    cartData.forEach(item => {
        cartItems.append(`
            <li>
                ${item.name} - ${item.quantity} pcs - $${(item.price * item.quantity).toFixed(2)}
                <button class="btn btn-sm btn-secondary mx-1" onclick="increaseQuantity(${item.id})">+</button>
                <button class="btn btn-sm btn-secondary mx-1" onclick="decreaseQuantity(${item.id})">-</button>
            </li>
        `);
        totalPrice += item.price * item.quantity;
    });

    $('#totalPrice').text(`Total: $${totalPrice.toFixed(2)}`);
}

// مسح جميع المنتجات من السلة
function clearCart() {
    $.ajax({
        url: '/api/cart', // مسار API لتفريغ السلة
        type: 'DELETE', // نوع الطلب
        success: function () {
            updateCart([]); // تحديث الكارت ليصبح فارغًا
            alert('Cart cleared successfully!');
        },
        error: function (xhr) {
            alert('Error: Failed to clear cart.');
            console.error('Clear Cart Error:', xhr.responseJSON);
        }
    });
}