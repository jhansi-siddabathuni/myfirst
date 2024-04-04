from flask import Flask, render_template, request
import pickle
  
# Create an app object using the Flask class. 
app = Flask(__name__, template_folder="templates")

# Load the trained model (Pickle file).
model = pickle.load(open('rf.pkl', 'rb'))

# Define the route to be home. 
@app.route('/')
def home():
    return render_template('index.html')

# Add Post method to the decorator to allow for form submission. 
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    print("Request method:", request.method)
    print("Form data:", request.form)  # Print the form data for debugging
    
    if request.method == 'POST':
        # List of required form fields
        required_fields = ['age', 'sex', 'chestpain', 'restbloodpressure', 'cholestrol', 
                           'fastingbloodsugar', 'restingelectrocardiographicresults', 
                           'thalach', 'exerciseinducedangina', 'oldpeak', 'slope', 'ca', 'thal']
        
        # Check if all required fields are present in the form data
        missing_fields = [field for field in required_fields if field not in request.form]
        
        if missing_fields:
            return f"Error: Missing form field(s) - {', '.join(missing_fields)}"
        if not request.form['fastingbloodsugar'].strip():
            return "Error: Empty form field(s) found: fastingbloodsugar"


    
    
    if request.method == 'POST':
        try:
            age = float(request.form['age'])
            sex = request.form['sex']
            chestpain = request.form['chestpain']
            restbloodpressure = float(request.form['restbloodpressure'])
            cholestrol = float(request.form['cholestrol'])
            fastingbloodsugar = float(request.form['fastingbloodsugar'])
            restingelectrocardiographicresults = request.form['restingelectrocardiographicresults']
            thalach = float(request.form['thalach'])
            exerciseinducedangina = request.form['exerciseinducedangina']
            oldpeak = float(request.form['oldpeak'])
            slope = request.form['slope']
            ca = request.form['ca']
            thal = request.form['thal']
            
            empty_fields = [field for field, value in request.form.items() if not value.strip()]
            if empty_fields:
                return f"Error: Empty form field(s) found: {', '.join(empty_fields)}"

        
            input_list = [age, sex, chestpain, restbloodpressure, cholestrol, fastingbloodsugar,
                        restingelectrocardiographicresults, thalach, exerciseinducedangina,
                        oldpeak, slope, ca, thal]
            pred = model.predict([input_list])
            output = pred[0]
            if output == 0:
                return render_template("NODISEASE.html")
            else:
                return render_template("DISEASE.html")
        
        
        except KeyError as e:
            return f"Error: Missing form field - {e}"
        except Exception as e:
            return f"An error occurred: {e}"
    
    # Handle the case when the request method is GET.
    elif request.method == 'GET':
        return "GET request received. Please submit the form."

if __name__ == "__main__":
    app.run()
