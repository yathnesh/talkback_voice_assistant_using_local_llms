from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate_response():
    data = request.get_json()
    prompt = data.get("prompt")
    # Simulate a response from a model
    response = {"response": f"Response to: {prompt}"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=11434)
