from flask import Flask, render_template, request
import pickle
import numpy as np
import requests

app = Flask(__name__)

def get_exchange_rate():
    api_key = "752e006f245aa9f888acc381" 
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/EUR"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and 'conversion_rates' in data:
        return data['conversion_rates']['LKR']
    else:
        return 219  

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value    

@app.route('/', methods=['POST', 'GET'])
def index():
    pred = 0

    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')

        feature_list = [int(ram), float(weight), len(touchscreen), len(ips)]
        
        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'toshiba', 'other']
        typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
        opsys_list = ['windows', 'mac', 'linux', 'other']
        cpu_list = ['intelcorei3', 'intelcorei5', 'intelcorei7', 'amd', 'other']
        gpu_list = ['intel', 'amd', 'nvidia']

        def traverse(lst, value):
            for item in lst:
                feature_list.append(1 if item == value else 0)

        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)

        exchange_rate = get_exchange_rate()
        pred = prediction(feature_list) * exchange_rate
        pred = np.round(pred[0], 2)

    return render_template("index.html", pred=pred)

if __name__ == '__main__':
    app.run(debug=True)
