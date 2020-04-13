import requests, psycopg2

connection = psycopg2.connect(user="cs162_user",
                                  password="cs162_password",
                                  host="localhost",
                                  database="cs162")
cursor = connection.cursor()

try:
    # valid expression
    response = requests.post('http://127.0.0.1:5000/add',data={'expression':'3*2'})
    assert response.status_code == 200

    # check if valid expression is stored
    cursor.execute("SELECT * FROM Expression WHERE text='3*2' ORDER BY id DESC LIMIT 1")
    data = cursor.fetchall()
    print(data)
    assert data[0][2] == 6
    current_id = data[0][0]

    # invalid expression
    response = requests.post('http://127.0.0.1:5000/add', data={'expression':'3^2'})
    assert response.status_code == 500

    # check if invalid expression is not stored
    cursor.execute("SELECT * FROM Expression ORDER BY id DESC LIMIT 1")
    data = cursor.fetchall()
    print(data)
    assert data[0][2] == 6
    assert data[0][0] == current_id

# raise an exception if not all tests passed
except:
    raise 'At least one test failed'
