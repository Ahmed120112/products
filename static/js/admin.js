 // إضافة منتج
 document.getElementById('addProductForm').addEventListener('submit', function (e) {
    e.preventDefault(); // منع إعادة تحميل الصفحة

    const formData = new FormData(e.target);

    fetch('/admin/products/add', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the product.');
    });
});
// حذف منتج
function deleteProduct(productId) {
    fetch(`/admin/products/delete/${productId}`, {
        method: 'POST'
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error);
        }
    });
}

// عرض نموذج تعديل المنتج
function showEditForm(id, name, price, description) {
    document.getElementById('editProductForm').style.display = 'block';
    document.getElementById('editProductId').value = id;
    document.getElementById('editName').value = name;
    document.getElementById('editPrice').value = price;
    document.getElementById('editDescription').value = description;
}

// تعديل منتج
function updateProduct() {
    const id = document.getElementById('editProductId').value;
    const formData = new FormData();
    formData.append('name', document.getElementById('editName').value);
    formData.append('price', document.getElementById('editPrice').value);
    formData.append('description', document.getElementById('editDescription').value);

    fetch(`/admin/products/update/${id}`, {
        method: 'POST',
        body: formData
    }).then(response => response.json()).then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error);
        }
    });
}