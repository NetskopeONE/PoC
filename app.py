from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

API_ENDPOINT = 'https://bortolato.de.goskope.com/api/v1/alerts?token=2ba863fa1073474f4e2535e96ab355ab&timeperiod=3600&type=dlp&query=alert_name%2520eq%2520%27%5BDLP%5D%20Approval%20Required%27'
ACTION_ENDPOINT = 'https://bortolato.de.goskope.com/api/v1/updatefilehashlist?token=2ba863fa1073474f4e2535e96ab355ab&name=Approved'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    try:
        response = requests.get(API_ENDPOINT)
        data = response.json().get('data', [])
        
        # Prepare the data for the template
        alerts = [{
            'alert_name': item['alert_name'],
            'app': item['app'],
            'activity': item['activity'],
            'user': item['user'],
            'object': item['object'],
            'src_time': item['src_time'],
            'id': item['sha256']
        } for item in data]
        
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/perform_action', methods=['POST'])
def perform_action():
    try:
        file_id = request.json.get('id')
        response = requests.post(f'{ACTION_ENDPOINT}&list={file_id}')
        
        if response.ok:
            return jsonify({'message': 'File Approved!'})
        else:
            return jsonify({'message': 'Failed to approve the file.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)