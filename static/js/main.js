// فتح/إغلاق الكارت مع دفع الصفحة
$('#cartButton').on('click', function() {
    $('#cartSidebar').toggleClass('active'); // فتح/إغلاق الكارت
    if ($('#cartSidebar').hasClass('active')) {
        $('body').addClass('cart-open'); // دفع الصفحة
    } else {
        $('body').removeClass('cart-open'); // إرجاع الصفحة لوضعها الطبيعي
    }
});

// إغلاق الكارت فقط
$('#closeCart').on('click', function() {
    $('#cartSidebar').removeClass('active'); // إغلاق الكارت
    $('body').removeClass('cart-open'); // إرجاع الصفحة لوضعها الطبيعي
});

// إضافة منتج إلى السلة
function addToCart(productId) {
    $.ajax({
        url: '/add_to_cart',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId }),
        success: function(cartData) {
            updateCart(cartData);
            $('#cartSidebar').addClass('active'); // فتح الكارت تلقائيًا
            $('body').addClass('cart-open'); // دفع الصفحة تلقائيًا
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.error);
        }
    });
}

// زيادة الكمية لمنتج معين
function increaseQuantity(productId) {
    $.ajax({
        url: '/increase_quantity',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId }),
        success: function(cartData) {
            updateCart(cartData);
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.error);
        }
    });
}

// تقليل الكمية لمنتج معين
function decreaseQuantity(productId) {
    $.ajax({
        url: '/decrease_quantity',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ product_id: productId }),
        success: function(cartData) {
            updateCart(cartData);
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.error);
        }
    });
}

// تحديث محتويات الكارت
function updateCart(cartData) {
    let cartItems = $('#cartItems');
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
        url: '/clear_cart',
        type: 'POST',
        success: function() {
            updateCart([]); // تحديث الكارت ليصبح فارغًا
        },
        error: function(xhr) {
            alert('Error: ' + xhr.responseJSON.error);
        }
    });
}