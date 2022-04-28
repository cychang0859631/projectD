#import model # Import the python file containing the ML model
from flask import Flask, request, render_template,jsonify # Import flask libraries
import joblib
import numpy as np
# Initialize the flask class and specify the templates directory
app = Flask(__name__,template_folder="templates")


clf2 = joblib.load('clf.pkl')
variety_mappings = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}
# Default route set as 'home'
@app.route('/')
def home():
    return render_template('home.html') # Render home.html

# Route 'classify' accepts GET request
@app.route('/classify',methods=['POST','GET'])
def classify_type():
    try:
        sepal_len = request.args.get('slen') # Get parameters for sepal length
        sepal_wid = request.args.get('swid') # Get parameters for sepal width
        petal_len = request.args.get('plen') # Get parameters for petal length
        petal_wid = request.args.get('pwid') # Get parameters for petal width
        X = np.array([sepal_len,sepal_wid,petal_len,petal_wid])
        X = X.reshape(1,-1)
        #print(X)
        # Get the output from the classification model
        #variety = model.classify(sepal_len, sepal_wid, petal_len, petal_wid)
        variety = variety_mappings[clf2.predict(X)[0]]
        # Render the output in new HTML page
        return render_template('output.html', variety=variety)
    except:
        return 'Error'

# Run the Flask server
if(__name__=='__main__'):
    app.run(debug=True)