from flask import Flask, jsonify, request
from afinn import Afinn
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
CORS(app)
afinn = Afinn()
db="https://919hj0d72g.execute-api.us-west-2.amazonaws.com/prod/reviews"

@app.route('/analysis', methods=['GET'])
def get_sentiments():
    neg,pos,neu = 0,0,0
    max_neg, max_pos = 0,0
    url = db + "?TableName=UserReviews"
    
    reviews = requests.get(url)

    res = reviews.json()

    
    for review in res['Items']:   
        score = review['score']    
        if(score < 0):
            neg += 1
        elif(score > 0):
            pos += 1
        else:
            neu += 1

    sorted_review = sorted(res['Items'],key=lambda x:x['score'])
    


    data = {
        "neg": neg,
        "pos": pos,
        "neu": neu,
        "top_pos": [],
        "top_neg": []
    }

    
    if(sorted_review[0]['Comments']):
        data["top_neg"].append(sorted_review[0]['Comments'])

    if(sorted_review[1]['Comments']):
        data["top_neg"].append(sorted_review[1]['Comments'])
    
    data["top_pos"].append(sorted_review[-1]['Comments'])
    data["top_pos"].append(sorted_review[-2]['Comments'])

    return jsonify(data), 200 


@app.route('/review', methods=['POST'])
def set_sentiments():

    print request.json

    if not request.json:
        abort(400)

    msg = {
        'TableName': u'UserReviews',
        'Item':{
            'TripId': u'',
            'Comments':u'',
            'score': 0
        }
    }


    if(request.json['comments']):
        msg['Item']['TripId'] = request.json['tripId']
        msg['Item']['Comments'] = request.json['comments']
        msg['Item']['score'] = find_score(request.json['comments'])


    r = requests.post(db, data=json.dumps(msg))

    print msg, "\n";
    print(r.status_code, r.reason)
    

    return jsonify({'review': msg}), 201




def find_score(text):
    return afinn.score(text)


if __name__ == '__main__':
    app.run(debug=True)