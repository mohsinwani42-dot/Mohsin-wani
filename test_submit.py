from app import app

client = app.test_client()
resp = client.post('/submit', json={'name': 'Test', 'email': 'test@example.com', 'message': 'Hello'})
print(resp.status_code)
print(resp.get_json())
