from flask import Flask, url_for, render_template
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p1")
def render_page1():
    return render_template('page1.html')

@app.route("/p2")
def render_page2():
    return render_template('page2.html')
    
with open('electricity.json', encoding='utf-8') as electricity:
    electricity_data = json.load(electricity) 

#print(electricity_data) #word_data is a list of dictionaries
    
if __name__=="__main__":
    app.run(debug=True)
    
    
    
    
    
    # do some research about the  source of the data, the significance of the data, and how it is calculated and regulated
    
   