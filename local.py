from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from mira_sdk import MiraClient, CompoundFlow
from mira_sdk.exceptions import FlowError

# Initialize Flask app
app = Flask(__name__)  # Use double underscores: __name__

# Enable CORS for all routes
CORS(app)  # Allow all origins

# Initialize Mira Client
client = MiraClient(config={"API_KEY": "YOUR_API_KEY"})

# Load the compound flow configuration
flow = CompoundFlow(source="flow.yaml")  

@app.route('/submit', methods=['POST'])
def generate_website():
    # Parse the JSON payload from the frontend
    data = request.json
    test_input = {
        "purpose": data.get("purpose", ""),
        "color_combination": data.get("color_combination", ""),
        "design": data.get("design", ""),
        "additional_features": data.get("additional_features", ""),
    }

    try:
        # Test the pipeline
        response = client.flow.test(flow, test_input)

        validated_inputs = response.get("validate_inputs", "")
        generated_html = response.get("generate_html", "")
        formatted_html = response.get("format_output", "")

        # Save the formatted HTML to a file
        if formatted_html:
            with open("output.html", "w") as file:
                file.write(formatted_html)

        # Return the formatted HTML and other data to the frontend
        return jsonify({
            "success": True,
            "validated_inputs": validated_inputs,
            "generated_html": generated_html,
            "formatted_html": formatted_html
        })

    except FlowError as e:
        # Handle test failure
        return jsonify({"success": False, "error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':  # Use double underscores: __name__
    app.run(host='127.0.0.1', port=5000, debug=True)