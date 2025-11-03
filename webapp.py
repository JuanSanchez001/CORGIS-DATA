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
    
   # dataPoints: [{ winter }]
			#{ y: 212, label: "Italy" },
			#{ y: 186, label: "China" },
			#{ y: 272, label: "France" },
			#{ y: 299, label: "Great Britain" },
			#{ y: 270, label: "Germany" },
			#{ y: 165, label: "Russia" },
			#{ y: 896, label: "CA" } 
		#]
       '''  { y: 212, label: "Alabama" }, (states)
  { y: 186, label: "Alaska" },
  { y: 272, label: "Arizona" },
  { y: 299, label: "Arkansas" },
  { y: 270, label: "California" },
  { y: 165, label: "Colorado" },
  { y: 896, label: "Connecticut" },
  { y: 212, label: "Delaware" },
  { y: 186, label: "Florida" },
  { y: 272, label: "Georgia" },
  { y: 299, label: "Hawaii" },
  { y: 270, label: "Idaho" },
  { y: 165, label: "Illinois" },
  { y: 896, label: "Indiana" },
  { y: 212, label: "Iowa" },
  { y: 186, label: "Kansas" },
  { y: 272, label: "Kentucky" },
  { y: 299, label: "Louisiana" },
  { y: 270, label: "Maine" },
  { y: 165, label: "Maryland" },
  { y: 896, label: "Massachusetts" },
  { y: 212, label: "Michigan" },
  { y: 186, label: "Minnesota" },
  { y: 272, label: "Mississippi" },
  { y: 299, label: "Missouri" },
  { y: 270, label: "Montana" },
  { y: 165, label: "Nebraska" },
  { y: 896, label: "Nevada" },
  { y: 212, label: "New Hampshire" },
  { y: 186, label: "New Jersey" },
  { y: 272, label: "New Mexico" },
  { y: 299, label: "New York" },
  { y: 270, label: "North Carolina" },
  { y: 165, label: "North Dakota" },
  { y: 896, label: "Ohio" },
  { y: 212, label: "Oklahoma" },
  { y: 186, label: "Oregon" },
  { y: 272, label: "Pennsylvania" },
  { y: 299, label: "Rhode Island" },
  { y: 270, label: "South Carolina" },
  { y: 165, label: "South Dakota" },
  { y: 896, label: "Tennessee" },
  { y: 212, label: "Texas" },
  { y: 186, label: "Utah" },
  { y: 272, label: "Vermont" },
  { y: 299, label: "Virginia" },
  { y: 270, label: "Washington" },
  { y: 165, label: "West Virginia" },
  { y: 896, label: "Wisconsin" },
  { y: 212, label: "Wyoming" }'''
        
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
    	
def demand_average_summer_and_winter()
    with open('electricity.json') as electricity_data:
        utilities = json.load(electricity_data)                
                  
                  
                  
                  
                  
                  
                  
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