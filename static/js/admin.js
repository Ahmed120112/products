// تحميل المنتجات وعرضها في الجدول
function loadProducts() {
    fetch('/api/products')
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch products');
            return response.json();
        })
        .then(data => {
            const tableBody = document.getElementById('productTable').querySelector('tbody');
            tableBody.innerHTML = ''; // تفريغ الجدول قبل إعادة تعبئته

            data.forEach(product => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${product.name}</td>
                    <td>$${product.price.toFixed(2)}</td>
                    <td>${product.description || 'No description available'}</td>
                    <td>
                        <img src="${product.image_url || 'https://via.placeholder.com/50'}" alt="${product.name}" width="50">
                    </td>
                    <td>
                        <button class="btn btn-sm btn-secondary" onclick="showEditForm(${product.id}, '${product.name}', ${product.price}, '${product.description || ''}', ${product.category_id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteProduct(${product.id})">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(err => {
            console.error('Error loading products:', err);
            alert('Failed to load products. Please try again.');
        });
}

// إضافة منتج جديد
document.getElementById('addProductForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const data = {
        name: document.getElementById('name').value.trim(),
        price: parseFloat(document.getElementById('price').value),
        description: document.getElementById('description').value.trim(),
        image_url: document.getElementById('image_url').value.trim(),
        category_id: parseInt(document.getElementById('category_id').value)
    };

    fetch('/api/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to add product');
            return response.json();
        })
        .then(() => {
            alert('Product added successfully');
            loadProducts();
        })
        .catch(err => {
            console.error('Error adding product:', err);
            alert('Error adding product. Please try again.');
        });
});

// عرض نموذج تعديل المنتج
function showEditForm(id, name, price, description, category_id) {
    // تعبئة النموذج بقيم المنتج
    document.getElementById('editProductId').value = id;
    document.getElementById('editName').value = name;
    document.getElementById('editPrice').value = price;
    document.getElementById('editDescription').value = description;
    document.getElementById('editImageUrl').value = '';
    document.getElementById('editCategoryId').value = category_id;

    // عرض نموذج التعديل
    document.getElementById('editProductForm').style.display = 'block';
}

// تعديل المنتج
document.getElementById('editProductForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const id = document.getElementById('editProductId').value;
    const data = {
        name: document.getElementById('editName').value.trim(),
        price: parseFloat(document.getElementById('editPrice').value),
        description: document.getElementById('editDescription').value.trim(),
        image_url: document.getElementById('editImageUrl').value.trim(),
        category_id: parseInt(document.getElementById('editCategoryId').value)
    };

    fetch(`/api/products/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to update product');
            return response.json();
        })
        .then(() => {
            alert('Product updated successfully');
            document.getElementById('editProductForm').style.display = 'none'; // إخفاء النموذج
            loadProducts();
        })
        .catch(err => {
            console.error('Error updating product:', err);
            alert('Error updating product. Please try again.');
        });
});

// حفظ التعديلات على المنتج
function submitEditProduct() {
    const id = document.getElementById('editProductId').value;
    const data = {
        name: document.getElementById('editName').value.trim(),
        price: parseFloat(document.getElementById('editPrice').value),
        description: document.getElementById('editDescription').value.trim(),
        image_url: document.getElementById('editImageUrl').value.trim(),
        category_id: parseInt(document.getElementById('editCategoryId').value)
    };

    fetch(`/api/products/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update product');
            }
            return response.json();
        })
        .then(() => {
            alert('Product updated successfully');
            document.getElementById('editProductForm').style.display = 'none'; // إخفاء نموذج التعديل
            loadProducts(); // إعادة تحميل المنتجات في الجدول
        })
        .catch(err => {
            console.error('Error updating product:', err);
            alert('Error updating product. Please try again.');
        });
}

// إخفاء نموذج التعديل عند الإلغاء
function cancelEdit() {
    document.getElementById('editProductForm').style.display = 'none';
}

// حذف المنتج
function deleteProduct(productId) {
    fetch(`/api/products/${productId}`, { method: 'DELETE' })
        .then(response => {
            if (!response.ok) throw new Error('Failed to delete product');
            return response.json();
        })
        .then(() => {
            alert('Product deleted successfully');
            loadProducts();
        })
        .catch(err => {
            console.error('Error deleting product:', err);
            alert('Error deleting product. Please try again.');
        });
}

// تحميل المنتجات عند فتح الصفحة
document.addEventListener('DOMContentLoaded', loadProducts);