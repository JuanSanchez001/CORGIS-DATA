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
    
    return render_template('page1.html', state_options=states, name_options=names)
    
    
@app.route("/p2")
def render_page2():
    states = get_state_options()
    names = get_name_options(states)
    
    return render_template('page2.html', state_options=states, name_options=names)
    
    
@app.route("/p3")
def render_page3():
    total_summer = summer_peak_demand()
    total_winter = winter_peak_demand()
    #https://www.perplexity.ai/search/why-use-total-winter-state-wde-wqLX7z5MS4aN.PwXQyq9qA( used to find sort )
    sorted_summer = dict(sorted(total_summer.items()))
    sorted_winter = dict(sorted(total_winter.items()))
    
    return render_template('page3.html', data_points1=sorted_summer, data_points2=sorted_winter)
    
    
@app.route('/utilities')
def render_utilities():
    states = get_state_options()
    state = request.args.get('state')
    names = get_name_options(state)
    name = request.args.get('name')
    
    return render_template('page1.html', state_options=states, name_options=names)
    
    
#https://www.perplexity.ai/search/why-is-this-giving-me-this-err-s_sLBpCpTs6xQP9Fqu_vtQ  (using f-strings)       
@app.route('/customers')
def render_customers():
    state = request.args.get('state')
    name = request.args.get('name')
    total_customers = total_customers_per_utility(name)
    total_sales = total_sales_per_utility(name)
    total_revenue = total_revenue_per_utility(name)
    customer = f"{name} had an overall total of the folowing in 2017: "
    customer1 = f"({total_customers}) customers"
    customer2 = f"({total_sales}) in total sales"
    customer3 = f"Total revenue received was ({total_revenue})"
    
    return render_template('page1.html', customers=customer, customers1=customer1, customers2=customer2, customers3=customer3)

    
@app.route('/sources')   
def render_sources():
    states = get_state_options()
    state = request.args.get('state') 
    name = request.args.get('name') 
    big_producer = highest_electricity_producing_utility(state)
    source = f"The Utility with the highest electricty obtained from itself and outside producer in this state was {big_producer[0]} with ({big_producer[1]}) megawatt hours."
    
    return render_template('page2.html', sources=source) 
    
    
def get_state_options():
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    states = sorted({u["Utility"]["State"] for u in utilities})
    options = ""
    for s in states:
        options += Markup(f'<option value="{s}">{s}</option>')
    return options

def get_name_options(state):
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    # it sorts it and then looks to see if the state they selected = state
    names = sorted({u["Utility"]["Name"] for u in utilities if u["Utility"]["State"] == state})
    options = ""
    for n in names:
        options += Markup("<option value=\"" + n + "\">" + n + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
    #connect to def summeR and winter peak(TBD)
    
    '''dataPoints: [[{ winter }] 
			{ y: 333, label: "Italy" },
			{ y: 333, label: "China" },
			{ y: s["Demand"][], label: "France" },
			{ y: 299, label: "Great Britain" },
			{ y: 270, label: "Germany" },
			{ y: 165, label: "Russia" },
			{ y: 896, label: "CA" } 
		]
    
        
        #dataPoints: [
			#{ y: 236, label: "Italy" },
			#{ y: 172, label: "China" },
			#{ y: 309, label: "France" },
			#{ y: 302, label: "Great Britain" },
			#{ y: 285, label: "Ge" },
			#{ y: 188, label: "Russia" },
			#{ y: 788, label: "CA" }
		#]'''
        
    
def total_customers_per_utility(name):
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    for u in utilities:
        if u["Utility"]["Name"] == name:
            return u["Retail"]["Total"]["Customers"]
           
def total_sales_per_utility(name):
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    for u in utilities:
        if u["Utility"]["Name"] == name:
            return u["Retail"]["Total"]["Sales"]     
           
def total_revenue_per_utility(name):
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    for u in utilities:
        if u["Utility"]["Name"] == name:
            return u["Retail"]["Total"]["Revenue"]    
            
def highest_electricity_producing_utility(state):
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    highest=0
    name = ""
    for u in utilities:
    	if u["Utility"]["State"] == state:
    		if u["Sources"]["Total"] > highest:
    			highest = u["Sources"]["Total"]
    			name = u["Utility"]["Name"]
    return (name, highest)
    	
def summer_peak_demand():                 
    with open('electricity.json') as file:
        data = json.load(file)             
    total_summer = {}
    counts = {}
    for d in data:
        state = d["Utility"]["State"]
        sdemand = d["Demand"]["Summer Peak"]
        if state not in total_summer:
            total_summer[state] = 0
            counts[state] = 0
        total_summer[state] += sdemand
        total_summer[state] = total_summer[state] 
    return total_summer
    
def winter_peak_demand():                 
    with open('electricity.json') as file:
        data = json.load(file)             
    total_winter = {}
    counts = {}
    for d in data:
        state = d["Utility"]["State"]
        wdemand = d["Demand"]["Winter Peak"]
        if state not in total_winter:
            total_winter[state] = 0
            counts[state] = 0
        total_winter[state] += wdemand
        total_winter[state] = total_winter[state] 
    return total_winter    
 
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url

if __name__=="__main__":
    app.run(debug=False)