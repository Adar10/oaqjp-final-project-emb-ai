"""
Server code

"""

from flask import Flask, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def detect_emotion():

    """
    Handles POST requests to the /emotionDetector endpoint.
    
    """

    data = request.get_json()

    text_to_analyze = data["text"]
    if not text_to_analyze:
        return jsonify({"response": "Invalid text! Please try again!"}), 400

    result = emotion_detector(text_to_analyze)
    if result['dominant_emotion'] is None:
        return jsonify({"response": "Invalid text! Please try again!"}), 400

    response_text = (f"For the given statement, the system response is "
                     f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
                     f"'fear': {result['fear']}, 'joy': {result['joy']} and "
                     f"'sadness': {result['sadness']}. "
                     f"The dominant emotion is {result['dominant_emotion']}.")

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
