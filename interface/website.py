import os
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Directory containing subfolders, each containing two CSV files
DATA_DIRECTORY = '<Here should be the local directory name with data, where the folders with csv files are stored>'

# Function to randomly select one CSV file from each subfolder
def select_random_csv_files():
    tractor_data = {}
    for folder_name in os.listdir(DATA_DIRECTORY):
        folder_path = os.path.join(DATA_DIRECTORY, folder_name)
        if os.path.isdir(folder_path):
            csv_files = [file_name for file_name in 
os.listdir(folder_path) if file_name.endswith('.csv')]
            if len(csv_files) >= 2:
                selected_csv_file = random.choice(csv_files)
                csv_file_path = os.path.join(folder_path, 
selected_csv_file)
                tractor_data[folder_name] = csv_file_path
    return tractor_data

# Load tractor data from selected CSV files
tractor_data = select_random_csv_files()

# Route to fetch tractor information by folder name
@app.route('/get_tractor_info/<tractor_id>')
def get_tractor_info(tractor_id):
    if tractor_id in tractor_data:
        csv_folder_path = os.path.join(DATA_DIRECTORY, tractor_id)
        if os.path.exists(csv_folder_path):
            csv_files = [file_name for file_name in 
os.listdir(csv_folder_path) if file_name.endswith('.csv')]
            if csv_files:
                selected_csv_file = random.choice(csv_files)
                csv_file_path = os.path.join(csv_folder_path, 
selected_csv_file)
                return jsonify({'csv_file_path': csv_file_path})
        return jsonify({'ошибка: файл с информацией о тракторе с этим ID не найден'})
    else:
        return jsonify({'ошибка: трактор с таким ID не найден'})

def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def make_predictions(data):
    predictions = model.predict(data)
    return predictions

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the data sent from the frontend
    predictions = make_predictions(data)  # Make predictions
    return jsonify(predictions)  # Return the predictions as JSON

if __name__ == '__main__':
    model = load_model()    
    app.run(debug=True)

