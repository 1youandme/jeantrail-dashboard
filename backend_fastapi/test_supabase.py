from services.supabase_service import insert_product

test_product = {
    "title": "Test Product",
    "description": "وصف تجريبي",
    "price": 99.99,
    "image": "https://via.placeholder.com/300"
}

result = insert_product(test_product)
print(result)
