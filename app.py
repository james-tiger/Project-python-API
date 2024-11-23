import time
import requests
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Ahmed Ali", "email": "ahmed.ali@example.com"},
    {"id": 2, "name": "Fatma Mohamed", "email": "fatma.mohamed@example.com"},
    {"id": 3, "name": "Omar Khaled", "email": "omar.khaled@example.com"},
    {"id": 4, "name": "Nadia Hassan", "email": "nadia.hassan@example.com"},
    {"id": 5, "name": "Mona Ibrahim", "email": "mona.ibrahim@example.com"},
    {"id": 6, "name": "Tarek Magdy", "email": "tarek.magdy@example.com"},
    {"id": 7, "name": "Sara Youssef", "email": "sara.youssef@example.com"},
    {"id": 8, "name": "Yassin Ahmed", "email": "yassin.ahmed@example.com"},
    {"id": 9, "name": "Layla Abdelaziz", "email": "layla.abdelaziz@example.com"},
    {"id": 10, "name": "Hassan Elshamy", "email": "hassan.elshamy@example.com"}
]

cars = [
    {"id": 1, "model": "BMW 320i", "year": 2020, "color": "Red", "price": 35000},
    {"id": 2, "model": "BMW X5", "year": 2023, "color": "Blue", "price": 75000},
    {"id": 3, "model": "BMW M3", "year": 2024, "color": "Black", "price": 95000},
    {"id": 4, "model": "Mercedes-Benz C-Class", "year": 2021, "color": "White", "price": 40000},
    {"id": 5, "model": "Mercedes-Benz GLC", "year": 2022, "color": "Silver", "price": 60000},
    {"id": 6, "model": "Mercedes-Benz S-Class", "year": 2023, "color": "Gray", "price": 120000},
    {"id": 7, "model": "BMW 740i", "year": 2021, "color": "Green", "price": 85000},
    {"id": 8, "model": "Mercedes-Benz E-Class", "year": 2022, "color": "Yellow", "price": 55000},
    {"id": 9, "model": "BMW 118i", "year": 2020, "color": "Purple", "price": 32000},
    {"id": 10, "model": "Mercedes-Benz A-Class", "year": 2024, "color": "Orange", "price": 43000}
]

tasks = [
    {"id": 1, "name": "Complete Project", "startTime": "2024-11-23T10:00:00Z", "endTime": "2024-11-24T10:00:00Z", "status": "in-progress"},
    {"id": 2, "name": "Submit Report", "startTime": "2024-11-24T12:00:00Z", "endTime": "2024-11-25T12:00:00Z", "status": "pending"},
    {"id": 3, "name": "Finish Documentation", "startTime": "2024-11-25T14:00:00Z", "endTime": "2024-11-26T14:00:00Z", "status": "pending"},
    {"id": 4, "name": "Client Meeting", "startTime": "2024-11-23T08:00:00Z", "endTime": "2024-11-23T10:00:00Z", "status": "completed"},
    {"id": 5, "name": "Design UI", "startTime": "2024-11-23T09:00:00Z", "endTime": "2024-11-23T17:00:00Z", "status": "completed"},
    {"id": 6, "name": "Code Backend", "startTime": "2024-11-24T10:00:00Z", "endTime": "2024-11-24T18:00:00Z", "status": "in-progress"},
    {"id": 7, "name": "Deploy Application", "startTime": "2024-11-25T11:00:00Z", "endTime": "2024-11-25T15:00:00Z", "status": "pending"},
    {"id": 8, "name": "Test Features", "startTime": "2024-11-26T13:00:00Z", "endTime": "2024-11-26T17:00:00Z", "status": "pending"},
    {"id": 9, "name": "Prepare Presentation", "startTime": "2024-11-22T10:00:00Z", "endTime": "2024-11-22T12:00:00Z", "status": "completed"},
    {"id": 10, "name": "Team Meeting", "startTime": "2024-11-21T09:00:00Z", "endTime": "2024-11-21T11:00:00Z", "status": "completed"}
]


def fetch_users():
    while True:
        try:
            response = requests.get('http://127.0.0.1:5000/api/v1/users')  # Update the URL for version 1
            if response.status_code == 200:
                users.extend(response.json())
                print(f"Fetched {len(response.json())} users")
                break
            else:
                print(f"Connection failed with status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Server not available, retrying...")
        time.sleep(2)


def apply_filter(data, filters):
    for key, value in filters.items():
        data = [item for item in data if str(item.get(key, '')).lower() == str(value).lower()]
    return data

def apply_sorting(data, sort_by):
    for sort in sort_by:
        reverse = False
        if sort.startswith('-'):
            reverse = True
            sort = sort[1:]  
        data = sorted(data, key=lambda x: x.get(sort, ''), reverse=reverse)
    return data

def apply_field_selection(data, fields):
    if not fields:
        return data
    fields = set(fields.split(','))
    for item in data:
        for key in list(item.keys()):
            if key not in fields:
                del item[key]
    return data

# API 1 
@app.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    filters = {key: request.args.get(key) for key in ['name', 'email'] if request.args.get(key)}
    users_data = apply_filter(users, filters)
    
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    users_data = users_data[offset:offset + limit]
    
    sort_by = request.args.get('sort', '').split(',')
    users_data = apply_sorting(users_data, sort_by)
    
    fields = request.args.get('fields', '')
    users_data = apply_field_selection(users_data, fields)
    
    return jsonify(users_data), 200

@app.route('/api/v1/users', methods=['POST'])
def create_user_v1():
    data = request.get_json()
    
    if not all(key in data for key in ('name', 'email')):
        return jsonify({"error": "Both name and email are required!"}), 400

    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user_v1(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User  not found"}), 404
    return jsonify(user), 200

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user_v1(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user.update({key: data.get(key, user[key]) for key in ('name', 'email')})
    return jsonify(user), 200

@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user_v1(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    users.remove(user)
    return jsonify({}), 204

@app.route('/api/v1/users/<int:user_id>', methods=['PATCH'])
def patch_user_v1(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({" error": "No data provided"}), 400

    user.update({key: data.get(key, user[key]) for key in ('name', 'email')})
    return jsonify(user), 200

# API 2 
@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    filters = {key: request.args.get(key) for key in ['name', 'email'] if request.args.get(key)}
    users_data = apply_filter(users, filters)
    
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    users_data = users_data[offset:offset + limit]
    
    sort_by = request.args.get('sort', '').split(',')
    users_data = apply_sorting(users_data, sort_by)
    
    fields = request.args.get('fields', '')
    users_data = apply_field_selection(users_data, fields)
    
    return jsonify(users_data), 200

@app.route('/api/v2/users', methods=['POST'])
def create_user_v2():
    data = request.get_json()
    
    if not all(key in data for key in ('name', 'email')):
        return jsonify({"error": "Both name and email are required!"}), 400

    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/v2/users/<int:user_id>', methods=['GET'])
def get_user_v2(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User    not found"}), 404
    return jsonify(user), 200

@app.route('/api/v2/users/<int:user_id>', methods=['PUT'])
def update_user_v2(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User    not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user.update({key: data.get(key, user[key]) for key in ('name', 'email')})
    return jsonify(user), 200

@app.route('/api/v2/users/<int:user_id>', methods=['DELETE'])
def delete_user_v2(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User    not found"}), 404

    users.remove(user)
    return jsonify({}), 204

@app.route('/api/v2/users/<int:user_id>', methods=['PATCH'])
def patch_user_v2(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User    not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user.update({key: data.get(key, user[key]) for key in ('name', 'email')})
    return jsonify(user), 200

# Common /users
@app.route('/users', methods=['GET'])
def get_users():
    filters = {key: request.args.get(key) for key in ['name', 'email'] if request.args.get(key)}
    users_data = apply_filter(users, filters)

    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    users_data = users_data[offset:offset + limit]

    sort_by = request.args.get('sort', '').split(',')
    users_data = apply_sorting(users_data, sort_by)

    fields = request.args.get('fields', '')
    users_data = apply_field_selection(users_data, fields)
    
    return jsonify(users_data), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not all(key in data for key in ('name', 'email')):
        return jsonify({"error": "Both name and email are required!"}), 400

    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201
@app.route('/api/v2/cars', methods=['POST'])
def create_car():
    data = request.get_json()

    if not all(key in data for key in ('model', 'year', 'color', 'price')):
        return jsonify({"error": "Model, year, color, and price are required!"}), 400

    new_car = {
        'id': len(cars) + 1,
        'model': data['model'],
        'year': data['year'],
        'color': data['color'],
        'price': data['price']
    }
    cars.append(new_car)
    return jsonify(new_car), 201


@app.route('/api/v2/cars', methods=['POST'])
def add_car_v2():
    data = request.get_json()

    new_car = {
        'id': len(cars) + 1,
        'model': data['model'],
        'year': data['year'],
        'color': data.get('color', 'Unknown'),
        'price': data.get('price', 0)
    }
    
    cars.append(new_car)
    
    return jsonify(new_car), 201

@app.route('/api/v2/cars', methods=['GET'])
def get_cars_v2():
    car_list = []
    
    # Get query parameters
    color = request.args.get('color')  
    sort = request.args.get('sort')  
    fields = request.args.get('fields')  
    
    offset = int(request.args.get('offset', 0))  
    limit = int(request.args.get('limit', 10))  
    
    filtered_cars = [car for car in cars if not color or car['color'].lower() == color.lower()]
    
    if sort:
        sort_fields = sort.split(',')
        for field in sort_fields:
            reverse = field.startswith('-')  
            field = field.lstrip('-')  
            filtered_cars.sort(key=lambda x: x.get(field, ''), reverse=reverse)

    cars_data = filtered_cars[offset:offset + limit]
    
    if fields:
        fields_to_include = fields.split(',')
        cars_data = [{field: car[field] for field in fields_to_include if field in car} for car in cars_data]
    
    for car in cars_data:
        car['links'] = [
            {
                "rel": "self",
                "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
            },
            {
                "rel": "update",
                "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
            },
            {
                "rel": "delete",
                "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
            },
            {
                "rel": "list",
                "href": "http://127.0.0.1:5000/api/v2/cars"
            }
        ]
    
    return jsonify(cars_data), 200


@app.route('/api/v2/cars/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    car = next((car for car in cars if car['id'] == car_id), None)
    if car:
        car_data = car.copy()
        car_data['links'] = [
            {
                "rel": "self",
                "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
            },
            {
                "rel": "update",
                "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
            },
            {
                "rel": "delete",
                "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
            },
            {
                "rel": "list",
                "href": "http://127.0.0.1:5000/api/v2/cars"
            }
        ]
        return jsonify(car_data), 200
    else:
        return jsonify({"message": "Car not found"}), 404

@app.route('/api/v2/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = next((car for car in cars if car['id'] == car_id), None)
    
    if not car:
        return jsonify({'message': 'Car not found'}), 404
    
    data = request.get_json()
    
    car['model'] = data.get('model', car['model'])
    car['year'] = data.get('year', car['year'])
    car['color'] = data.get('color', car['color'])
    car['price'] = data.get('price', car['price'])

    car_data = car.copy()
    car_data['links'] = [
        {
            "rel": "self",
            "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
        },
        {
            "rel": "update",
            "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
        },
        {
            "rel": "delete",
            "href": f"http://127.0.0.1:5000/api/v2/cars/{car['id']}"
        },
        {
            "rel": "list",
            "href": "http://127.0.0.1:5000/api/v2/cars"
        }
    ]
    return jsonify(car_data), 200

@app.route('/api/v2/tasks', methods=['POST'])
def create_task():
    task = {
        'id': len(tasks) + 1,
        'status': 'in_progress',
        'result': None
    }
    tasks.append(task)
    
    threading.Thread(target=long_running_task, args=(task['id'],)).start()
    
    return jsonify({'taskId': task['id']}), 202

def long_running_task(task_id):
    time.sleep(5)

    task = next(t for t in tasks if t['id'] == task_id)
    task['status'] = 'completed'
    task['result'] = 'Task completed successfully'
    
@app.route('/api/v2/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

if __name__ == "__main__":
    threading.Thread(target=fetch_users, daemon=True).start()
    app.run(debug=True)