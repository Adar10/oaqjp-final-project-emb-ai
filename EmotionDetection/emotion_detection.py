import requests
import json

def emotion_detector(text_to_analyze):

    if not text_to_analyze:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }, 400

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    data = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response_text = response.text  
        response_dict = json.loads(response_text)  
        
        emotion_scores = response_dict['emotionPredictions'][0]['emotion']
        required_emotions = {
            'anger': emotion_scores.get('anger', 0),
            'disgust': emotion_scores.get('disgust', 0),
            'fear': emotion_scores.get('fear', 0),
            'joy': emotion_scores.get('joy', 0),
            'sadness': emotion_scores.get('sadness', 0)
        }

        dominant_emotion = max(required_emotions, key=required_emotions.get)

        output = {
            'anger': required_emotions['anger'],
            'disgust': required_emotions['disgust'],
            'fear': required_emotions['fear'],
            'joy': required_emotions['joy'],
            'sadness': required_emotions['sadness'],
            'dominant_emotion': dominant_emotion
        }
        
        return output
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Failed to parse response as JSON: {e}")
        return None