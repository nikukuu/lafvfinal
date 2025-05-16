from flask import Blueprint, render_template, request, jsonify
import mysql.connector

items_bp = Blueprint('items', __name__, template_folder='../templates')

def get_db_connection():
    connection = mysql.connector.connect(
            host='kwimn.h.filess.io',
            user='lostthenfound_gashorndog',
            password='1c2943e986bcf6276ea1c71099e14054ae2b9283',
            database='lostthenfound_gashorndog',
            port = "3307"
        )
    return connection

@items_bp.route('/items', methods=['GET'])
def items():
    query = request.args.get('query', '')  # Get the search query from the request
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if query:  # If there's a search query
            search_query = f"%{query}%"
            cursor.execute(
                "SELECT * FROM items WHERE status='published' AND (id LIKE %s OR item_name LIKE %s OR description LIKE %s OR location LIKE %s)",
                (search_query, search_query, search_query, search_query)
            )
        else:  # No query, fetch all items
            cursor.execute("SELECT * FROM items WHERE status='published'")

        # Fetch the items
        items = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        items = []
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the database connection

    return render_template('items.html', items=items)

@items_bp.route('/items/search', methods=['GET'])
def search_items():
    query = request.args.get('query', '')  # Get the search query
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if query:  # If there's a search query
            search_query = f"%{query}%"
            cursor.execute(
                "SELECT * FROM items WHERE status='published' AND (id LIKE %s OR item_name LIKE %s OR description LIKE %s OR location LIKE %s)",
                (search_query, search_query, search_query, search_query)
            )
        else:  # No query, fetch all items
            cursor.execute("SELECT * FROM items WHERE status='published'")

        items = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        items = []
    finally:
        cursor.close()
        connection.close()

    return jsonify({'items': items})  # Return items as JSON
