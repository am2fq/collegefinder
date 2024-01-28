from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

JSON_FILE_PATH = 'surveys.json'

def initialize_json_file():
    if not os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump([], file)

def read_json_file():
    with open(JSON_FILE_PATH, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
    return data

def write_json_file(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    try:
        data = request.json
        full_name = data.get('fullName')
        contact_info = data.get('contactInfo')
        feedback = data.get('feedback')
        rating = data.get('rating')

        initialize_json_file()

        # Read existing data from the file
        existing_data = read_json_file()

        # Append the new survey data
        new_entry = {
            'fullName': full_name,
            'contactInfo': contact_info,
            'feedback': feedback,
            'rating': rating
        }
        existing_data.append(new_entry)

        # Write the updated data back to the file
        write_json_file(existing_data)

        return jsonify({'success': True, 'message': 'Survey submitted successfully'})

    except Exception as e:
        # Log the exception and return an error response
        print(f'Error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5500)

