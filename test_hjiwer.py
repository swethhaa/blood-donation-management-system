from app import app
print("Testing donation for hjiwer (donorid=15)...")

with app.test_client() as client:
    with app.test_request_context():
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        print(f"Login: {response.status_code}")
        response = client.post('/donate', data={
            'donorid': '15',
            'bloodgroup': 'A+',
            'units': '1'
        }, follow_redirects=True)
        
        print(f"Donate: {response.status_code}")
        print(f"Response text:\n{response.data.decode()[:2000]}")
