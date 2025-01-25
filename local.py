from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from mira_sdk import MiraClient, CompoundFlow
from mira_sdk.exceptions import FlowError

app = Flask(__name__)

CORS(app)

client = MiraClient(config={"API_KEY": "sb-415e643939543e5d2e57067df4149efb"})

flow = CompoundFlow(source="flow.yaml")

@app.route('/submit', methods=['POST'])
def generate_website():
    data = request.json
    test_input = {
        "purpose": data.get("purpose", ""),
        "color_combination": data.get("color_combination", ""),
        "design": data.get("design", ""),
        "additional_features": data.get("additional_features", ""),
    }

    try:
        
        response = client.flow.test(flow, test_input)
        print("Mira API Response:", response)  

        if response is None:
            raise FlowError("Mira API returned no response.")

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
        print("FlowError:", str(e)) 
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        print("Unexpected Error:", str(e))  
        return jsonify({"success": False, "error": "An unexpected error occurred."}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
