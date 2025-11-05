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

    names = get_name_options(states)
    return render_template('page2.html', state_options=states, name_options=names)
    
@app.route("/p3")
def render_page3():
    data_points = average_summer_peak_per_state()
    return render_template('page3.html', data_points=data_points)
    
@app.route('/utilities')
def render_utilities():
    states = get_state_options()
    state = request.args.get('state')
    names = get_name_options(state)
    name = request.args.get('name')
    #county = name_retail_sale(state, name)
    #demand = demand_per_utility(state)
    #sale= "In " + state + ", the electrical utility " + county[0] + " sold (" + str(county[1]) + ") megawatts of electricity" + "."
   
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
    # it sorts it and then looks to see if the state they selected
    names = sorted({u["Utility"]["Name"] for u in utilities if u["Utility"]["State"] == state})
    options = ""
    for n in names:
        options += Markup("<option value=\"" + n + "\">" + n + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
    #connect to def demand_average_summer_and_winter() idk?
    
    '''dataPoints: [[{ winter }]
			{ y: 333, label: "Italy" },
			{ y: 333, label: "China" },
			{ y: s["Demand"][], label: "France" },
			{ y: 299, label: "Great Britain" },
			{ y: 270, label: "Germany" },
			{ y: 165, label: "Russia" },
			{ y: 896, label: "CA" } 
		]'''
    
        
        #dataPoints: [
			#{ y: 236, label: "Italy" },
			#{ y: 172, label: "China" },
			#{ y: 309, label: "France" },
			#{ y: 302, label: "Great Britain" },
			#{ y: 285, label: "Ge" },
			#{ y: 188, label: "Russia" },
			#{ y: 788, label: "CA" }
		#]
        
    
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
    	
'''def demand_average_summer_and_winter():
    with open('electricity.json') as electricity_data:
        s_demand = json.load(electricity_data)
    average_demand=[]
    for s in s_demand:
        s_demand = s['Demand']['Summer Peak']
        
    return average_demand'''
      
'''with open('electricity.json', encoding='utf-8') as file:
    data = json.load(file)

names = [entry['Utility']['Name'] for entry in data]

# Normalize names by stripping spaces and converting to lowercase
normalized_names = [name.strip().lower() for name in names]

unique_names = set(normalized_names)

print("Total unique utilities (normalized):", len(unique_names))


with open('electricity.json', encoding='utf-8') as file:
    data = json.load(file)

state_utilities = {}

for entry in data:
    state = entry['Utility']['State']
    name = entry['Utility']['Name']
    if state not in state_utilities:
        state_utilities[state] = set()
    state_utilities[state].add(name)

for state, utilities in state_utilities.items():
    print(f"{state}: {len(utilities)}")'''
    
'''def summer_peak_demand():
    with open('electricity.json', encoding='utf-8') as file:
        data = json.load(file)
    s_peak = []
    for s in data:
        summer = s['Demand'].get('Summer Peak')
        state = s['Utility'].get('State')
        if summer is not None and state is not None:
            s_peak.append({'state': state, 'summer_peak': summer})
    # Optionally create a string or HTML output
    options = ""
    for entry in s_peak:
        options += Markup(f"<option value='{entry['state']}'>{entry['state']}: {entry['summer_peak']}</option>")
    return options'''
    
'''def summer_peak_demand():
    with open('electricity.json', encoding='utf-8') as file:
        data = json.load(file)
    s_peak=[]
    for s in s_peak:
        s_peak.append("x":s["Demand"]["Summer Peak"], "y":s["Utility"]["State"])
    
    return Markup(s_peak)'''
    
# the main idea is to get the info from each name in 1 state and find the average while still keeping it under the state
                  
#def winter_peak_demand():
                  
                  
                  
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
'''def get_data_points():
    with open('electricity.json', encoding='utf-8') as file:
        data = json.load(file)
    data_points = []
    for entry in data:
        state = entry['Utility'].get('State', 'Unknown')
        summer_peak = entry['Demand'].get('Summer Peak')
        if summer_peak is not None:
            data_points.append({"label": state, "y": summer_peak})
    return data_points'''
def average_summer_peak_per_state():
    with open('electricity.json', encoding='utf-8') as file:
        data = json.load(file)
    
    state_totals = {}
    state_counts = {}

    # Aggregate total summer peak demand and counts by state
    for entry in data:
        state = entry['Utility'].get('State')
        summer_peak = entry.get('Demand', {}).get('Summer Peak')
        if state and summer_peak is not None:
            state_totals[state] = state_totals.get(state, 0) + summer_peak
            state_counts[state] = state_counts.get(state, 0) + 1

    # Compute averages
    averages = []
    for state, total in state_totals.items():
        count = state_counts[state]
        avg = total / count if count > 0 else 0
        averages.append({"label": state, "y": avg})
    
    # Optionally sort by state name
    averages.sort(key=lambda x: x["label"])
    return averages    
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url

if __name__=="__main__":
    app.run(debug=True)