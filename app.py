import json
from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

df = pd.read_excel('dataset.xlsx')
json_string = df.to_json(orient='records')

with open('dataset.json', 'w') as f:
    f.write(json_string)

app = Flask(__name__)
CORS(app)
# @app.route('/cardata', methods=['GET'])
# def get_cardata():

#     with open("dataset.json") as f:
#         data = json.load(f)
    
#     # Return the CarData response
#     cardata = []
#     for i in range(0, len(data)):
#         cardata.append({'id': i})
#         cardata.append({'vin': data[i]['vin']})
#         cardata.append({'dealer': data[i]['dealer']})

#         metadata_str = data[i]['metadata_json']
#         metadata_str = metadata_str.replace("'", "\"")
#         metadata_json = json.loads(metadata_str)
#         for key, value in metadata_json.items():
#             cardata.append({key: value})

#         cardata.append({'Miles':data[i]['odometer']})

#         result = {}
#         for item in cardata:
#             key, value = next(iter(item.items()))
#             result[key] = value
#         carsdata.append(result)

#     return json.dumps(carsdata)


@app.route('/car/<string:id>', methods=('GET', 'POST'))
def getCarByID(id):
    carsdata = []
    with open("dataset.json") as f:
        data = json.load(f)
    


    cardata = []
    for i in range(0, len(data)):
        if(data[i]['vin'] == id):
            cardata.append({'id': i})
            cardata.append({'vin': data[i]['vin']})
            cardata.append({'dealer': data[i]['dealer']})
            cardata.append({'avg_market_price': data[i]['avg_market_price']})
            cardata.append({'asking_price': data[i]['asking_price']})

            metadata_str = data[i]['metadata_json']
            metadata_str = metadata_str.replace("'", "\"")
            metadata_json = json.loads(metadata_str)
            for key, value in metadata_json.items():
                cardata.append({key: value})

            cardata.append({'Miles':data[i]['odometer']})

            
            recon_str = data[i]['recon_json']
            recon_str = recon_str.replace("'", "\"")
            recon_str = recon_str.replace("None", "\"None\"")
            recon_json = json.loads(recon_str)
            for key, value in recon_json.items():
                if (key == 'table'):
                    cardata.append({'category': value[0]['category']})


            result = {}
            for item in cardata:
                key, value = next(iter(item.items()))
                result[key] = value
            carsdata.append(result)
    return json.dumps(carsdata[0])

@app.route('/filter_make_model', methods=['GET'])
def get_filterdata():
    carsdata = []
    with open("dataset.json") as f:
        data = json.load(f)
    


    cardata = []
    for i in range(0, len(data)):
        cardata.append({'id': i})
        cardata.append({'vin': data[i]['vin']})
        cardata.append({'dealer': data[i]['dealer']})
        cardata.append({'avg_market_price': data[i]['avg_market_price']})
        cardata.append({'asking_price': data[i]['asking_price']})

        metadata_str = data[i]['metadata_json']
        metadata_str = metadata_str.replace("'", "\"")
        metadata_json = json.loads(metadata_str)
        for key, value in metadata_json.items():
            cardata.append({key: value})

        cardata.append({'Miles':data[i]['odometer']})

        
            


        result = {}
        for item in cardata:
            key, value = next(iter(item.items()))
            result[key] = value
        carsdata.append(result)


    # Return the FilterData response
    # Initialize dictionary to store make and model counts
    make_model_counts = {}

    # Extract make and model information
    for entry in carsdata:
        make = entry["make"]
        model = entry["model"]
        
        if make not in make_model_counts:
            make_model_counts[make] = {
                "count": 1,
                "model": [[
                    {"count": 1, "name": model}
                ]]
            }
        else:
            make_count = make_model_counts[make]["count"]
            make_model_counts[make]["count"] = make_count + 1
            
            models = make_model_counts[make]["model"]
            model_found = False
            
            for i, model_data in enumerate(models):
                if model_data[0]["name"] == model:
                    model_count = model_data[0]["count"]
                    model_data[0]["count"] = model_count + 1
                    model_found = True
                    break
            
            if not model_found:
                models.append([{"count": 1, "name": model}])

    # Generate the output JSON dictionary
    output = {}

    for make, make_data in make_model_counts.items():
        make_count = make_data["count"]
        make_models = make_data["model"]
        
        output[make] = {
            "count": make_count,
            "model": [{"count": model_data[0]["count"], "name": model_data[0]["name"]} for model_data in make_models]
        }

    # Output the result as a JSON string
    output_json = json.dumps([{"carsdata": carsdata}, {"filterdata":output}])

    carsdata = []
    return output_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    
    
