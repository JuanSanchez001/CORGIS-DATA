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
   
    names = get_name_options(state)
    return render_template('page1.html', state_options=states, name_options=names)#, county_options=counties')
    
@app.route("/p2")
def render_page2():
    states = get_state_options()

    names = get_name_options(states)
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
    
    return render_template('page1.html', 'page2.html', state_options=states, name_options=names)
       
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
    #sales=sale)# county_options=counties, 
    
@app.route('/sources')   
def render_sources():
    states = get_state_options()
    state = request.args.get('state') 
    name = request.args.get('name') 
    big_producer = highest_electricity_producing_utility(state)
    source = f"The Utility with the highest electricty obtained from itself and outside producer was {big_producer[0]} with ({big_producer[1]}) megawatt hours"
    
    return render_template('page2.html', sources=source) 
    
    

def get_state_options():
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    # Use set comprehension to get unique states, then sort
    states = sorted({u["Utility"]["State"] for u in utilities})
    options = ""
    for s in states:
        options += Markup(f'<option value="{s}">{s}</option>')
    return options

def get_name_options(state):
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)
    # Collect unique utility names for the given state
    names = sorted({u["Utility"]["Name"] for u in utilities if u["Utility"]["State"] == state})
    options = ""
    for n in names:
        options += Markup("<option value=\"" + n + "\">" + n + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
    
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
    
def is_localhost():
    """ Determines if app is running on localhost or not
    Adapted from: https://stackoverflow.com/questions/17077863/how-to-see-if-a-flask-app-is-being-run-on-localhost
    """
    root_url = request.url_root
    developer_url = 'http://127.0.0.1:5000/'
    return root_url == developer_url

if __name__=="__main__":
    app.run(debug=True)
    
    
    
    
    

   
  # def get_state_options():
   # with open('electricity.json') as file:
   #     utilities = json.load(file)
  #  states=[]
  #  for u in utilities:
   #     if u["State"] not in states:
  #          states.append.sorted(u["State"])
   # states = sorted({u['Utility']['State'] for u in utilities if 'Utility' in u and 'State' in u['Utility']})
   # options = ""
   # for s in states:
    #   options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    #return options

#def get_name_options(state):
  #  with open('electricity.json') as file:
   #     utilities = json.load(file)
   # utilities=[]
   # for u in utilities:
  #  if state:
       # names = sorted({u['Utility']['Name'] for u in utilities if u['Utility']['State'] == state})
      #  if u["Utilities"] not in states:        
      #3      utilities.append.sorted(u["Utility"])
   # options = ""
   # for n in utilities:
    #      options += Markup("<option value=\"" + n + "\">" + n + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
  #  return options


#def county_most_under_18(state):
   # """Return the name of a county in the given state with the highest percent of under 18 year olds."""
  #  with open('demographics.json') as demographics_data:
  #      counties = json.load(demographics_data)
  #  highest=0
  #  county = ""
  #  for c in counties:
    #    if c["State"] == state:
      #      if c["Age"]["Percent Under 18 Years"] > highest:
       #         highest = c["Age"]["Percent Under 18 Years"]
           #     county = c["County"]
  #  return county       
    