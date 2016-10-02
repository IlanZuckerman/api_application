from flask import Flask, jsonify, abort, make_response, request
from time import strftime
app = Flask(__name__)

nowTime = strftime("%Y-%m-%d %H:%M")

books = [
    {
        'id': 1,
        'title': u'first',
        'description': u'first element',
        'create_date': nowTime
    },
    {
        'id': 2,
        'title': u'second',
        'description': u'second element',
        'create_date': nowTime
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}),404)

@app.route('/api/index', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0: abort(404)
    return jsonify({'book': book[0]})

@app.route('/api/books/', methods=['POST'])
def create_book():
    nowTime = strftime("%Y-%m-%d %H:%M")
    if not request.json or not 'title' in request.json: abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'creation_date': nowTime
    }
    books.append(book)
    return jsonify({'book:': book}), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0: abort(404)  # requested book id not found
    if not request.json:
        abort(400)

    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['description'] = request.json.get('description', book[0]['description'])
    return jsonify({'book': book[0]})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0: abort(404)  # requested book id not found
    books.remove(book[0])
    return jsonify({'book': book[0]})

if __name__ == '__main__':
    app.run(debug=True)