import json
from flask import Flask,request
import pandas as pd
import numpy as np
import random
from datetime import datetime

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self,obj)

app = Flask(__name__)

@app.route('/')
def index():
    return "Give startDate and endDate as URL Parameters"


def query_data(csv_file_path, query_start_date, query_end_date):
    # Load the DataFrame
    df = pd.read_csv(csv_file_path)
    print('+++++++++++++++++before++++++++++++++',df.head)
    # Convert date strings to datetime objects for comparison
    df['date'] = pd.to_datetime(df['date'])
    print('+++++++++++++++++After++++++++++++++',df.head)

    query_start_date = pd.to_datetime(query_start_date)
    query_end_date = pd.to_datetime(query_end_date)
    print('query_start_date++++++++++++++++',query_start_date)
    print('query_end_date++++++++++++++++',query_end_date)
    
    # Filter rows between start and end dates
    mask = (df['date'] >= query_start_date) & (df['date'] <= query_end_date)
    result_df = df.loc[mask]
    
    return result_df



def create_json_response(df):
    # Ensure the date column is in the correct format
    df['date'] = df['date'].dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    # Calculate the total of the 'value' column
    total_value = df['value'].sum()
    
    # Convert the DataFrame to a list of dictionaries
    data_list = df.to_dict('records')
    
    # Construct the response
    response = {
        "data": {
            "data": data_list,
            "trend": random.randint(10,1000),
            "total": total_value
        }
    }
    print(len(data_list))
    return json.dumps(response,cls=NpEncoder)


#queried_data = query_data(csv_file_path, '2023-01-01T00:00:00.000Z', '2023-01-10T00:00:00.000Z')




@app.route('/query')
def query():
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    startDate = request.args.get('startDate')
    startDate = datetime.strptime(startDate, date_format)
    endDate = request.args.get('endDate')
    endDate = datetime.strptime(endDate, date_format)
    print('start++++++++++++',startDate)
    print('end++++++++++++',endDate)
    queried_data = query_data('fake_data.csv', startDate, endDate)
    json_response = create_json_response(queried_data)
    return json_response



# if __name__ == '__main__':
#     # Change the port number if needed
#     app.run(debug=True, port=5002)
