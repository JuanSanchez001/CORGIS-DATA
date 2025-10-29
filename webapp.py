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
   
    names = get_name_options(states)

    return render_template('page1.html', state_options=states, name_options=names)#, county_options=counties')
    
@app.route("/p2")
def render_page2():
    states = get_state_options()

    names = get_name_options(state)
    return render_template('page2.html', state_options=states, name_options=names)
    
@app.route("/p3")
def render_page3():
    return render_template('page3.html')
    
@app.route('/utilities')
def render_utilities():
    states = get_state_options()
    state = request.args.get('state')
    names = get_name_options(state)
    name = request.args.get('name')
    #county = name_retail_sale(state, name)
    #demand = demand_per_utility(state)
    #sale= "In " + state + ", the electrical utility " + county[0] + " sold (" + str(county[1]) + ") megawatts of electricity" + "."
    #peaks = "In" + state + "," + name + " the electricity demand is" + demand[0] + " and the demand in the winter is" + str(demand[1]) + "."
    
    return render_template('page1.html', state_options=states, name_options=names)
    
    
@app.route('/customers')
def render_customers():
    state = request.args.get('state')
    name = request.args.get('name')
    number_of_c = customers_per_utility(state, name)
    customer = "This electrical utility " + number_of_c[0] + " had (" + str(number_of_c[1]) + ") total retail customers in 2017" + "."
    
    return render_template('page1.html', customers=customer)
    #sales=sale)# county_options=counties, 
    
    
def get_state_options():
    with open('electricity.json') as file:
        utilities = json.load(file)
    states = sorted({u['Utility']['State'] for u in utilities if 'Utility' in u and 'State' in u['Utility']})
    options = ""
    for s in states:
        options += Markup(f'<option value="{s}">{s}</option>')
    return options

def get_name_options(state):
    with open('electricity.json') as file:
        utilities = json.load(file)
    if state:
        names = sorted({u['Utility']['Name'] for u in utilities if u['Utility']['State'] == state})
    else:
        names = sorted({u['Utility']['Name'] for u in utilities})
    options = ""
    for n in names:
        options += Markup(f'<option value="{n}">{n}</option>')
    return options
 

  
#def name_retail_sale(state):
 #   """Return the name of a county in the given state with the highest percent of sales."""
  #  with open('electricity.json') as electricity_data:
   #     names = json.load(electricity_data)
    #highest=0
    #name = ""
    #for t in names:
     #   if t["Utility"]["State"] == state:
      #      if t["Retail"]["Total"]["Sales"] > highest:
       #         highest = t["Retail"]["Total"]["Sales"]
        #        name = t["Utility"]["Name"]
    #return (name, highest)
    
def customers_per_utility(state, name):
    with open('electricity.json') as file:
        customers = json.load(file) 
    highest=0
    for c in customers:
        if c["Utility"]["State"] == state and c["Utility"]["Name"] == name:
            if c["Retail"]["Total"]["Customers"] > highest:
                highest = c["Retail"]["Total"]["Customers"]
    return highest
    
        
    
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
    
       
#def name_retail_sale(state, name):
    #"""Return sold electricity by megawatts of a county in the given state."""
   # with open('electricity.json') as electricity_data:
   #     totals = json.load(electricity_data)
  #  highest =0
  #  total = ""
 #   for t in totals:
    #    if t["Utility"]["State"] == state:
   #         if t["Utility"]["Name"] == name:
       #         if t["Retail"]["Total"]["Sales"] == highest:
           #         highest = t["Retail"]["Total"]["Sales"]
      #              total = t["Utility"]["Name"]["State"]
   # return (total, highest)