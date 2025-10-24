from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p1")
def render_page1():
    states = get_state_options()
    names = get_name_options()
    return render_template('page1.html', state_options=states, name_options=names)#, county_options=counties')
    
@app.route("/p2")
def render_page2():
    return render_template('page2.html')
    
@app.route("/p3")
def render_page3():
    return render_template('page3.html')
    
@app.route('/sales')
def render_sales():
    states = get_state_options()
    state = request.args.get('state')
    names = get_name_options()
    name = request.args.get('name')
    county = name_retail_sale(state)
    sale= "In " + state + ", the electrical utility " + county[0] + " has sold (" + str(county[1]) + ") megawatts of electricity" + "."
    
    return render_template('page1.html', state_options=states, name_options=names, sales=sale)# county_options=counties, 
    
def get_state_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('electricity.json') as electricity_data:
        names = json.load(electricity_data)
    states=[]
    for n in names:
        if n["Utility"]["State"] not in states: 
            states.append(n["Utility"]["State"])
    states.sort()#added ai to sort
    options=""
    for s in states:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options    
    
def get_name_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('electricity.json') as electricity_data:
        states = json.load(electricity_data)
    names=[]
    for s in states:
        if s["Utility"]["Name"] not in names:
            names.append(s["Utility"]["Name"])
    names.sort()#added ai to sort
    options=""
    for n in names:
        options += Markup("<option value=\"" + n + "\">" + n + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options    
    
def name_retail_sale(state):
    """Return the name of a county in the given state with the highest percent of sales."""
    with open('electricity.json') as electricity_data:
        names = json.load(electricity_data)
    highest=0
    name = ""
    for t in names:
        if t["Utility"]["State"] == state:
            if t["Retail"]["Total"]["Sales"] > highest:
                highest = t["Retail"]["Total"]["Sales"]
                name = t["Utility"]["Name"]
    return (name, highest)
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url

if __name__=="__main__":
    app.run(debug=True)
    
    
    
    
    
    # do some research about the  source of the data, the significance of the data, and how it is calculated and regulated
    
   