from flask import Flask,render_template,request,redirect,url_for,flash
import requests

app=Flask(__name__)
app.secret_key='meteo.app'.encode('utf-8')
@app.route('/',methods=['GET','POST'])
def home():
    oras = request.args.get("oras")
    if not oras:
        return render_template('main.html')
    else:
        try:
            url = f"https://geocoding-api.open-meteo.com/v1/search?name={oras}&count=1&language=ro"
            response=requests.get(url)
            data_loc=response.json()
            lat = data_loc["results"][0]["latitude"]
            long = data_loc["results"][0]["longitude"]
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
            response = requests.get(url)
            data_meteo = response.json()
            viteza_vant = data_meteo["current_weather"]["windspeed"]
            temperatura = data_meteo["current_weather"]["temperature"]
            directie_vant = data_meteo["current_weather"]["winddirection"]
            return render_template('main.html',v=viteza_vant,t=temperatura,d=directie_vant)
        except requests.exceptions.RequestException as e:
            flash("Eroare:",e)
            return render_template('main.html',eroare=e)

if __name__=='__main__':
    app.run(debug=True)
