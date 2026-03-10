import requests

url = 'http://127.0.0.1:5000/items/batch_add'
cookies = {
    'user_id': '10',
    'session_token': 'abcdef123456'
}
data = {
    "data":[
        {
            "dollar": "39.90",
            "plat": "Alipay", 
            "detail": "661.45detail1111",
            "source": "web",
            "is_income": "1"
        },
        {
            "dollar": "49.90",
            "plat": "Alipay",
            "detail": "661.45detail1111",
            "source": "web",
            "is_income": "1"
        }   
    ]
    
}

response = requests.post(url, json=data, cookies=cookies)
print(response.json())