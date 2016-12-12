from flask import Flask, jsonify, request
from afinn import Afinn
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
afinn = Afinn()
db="https://919hj0d72g.execute-api.us-west-2.amazonaws.com/prod/reviews"

reviews = [
    {
        'tripId': "1",
        'comments': u'Good experience in booking',
        'score': 3.0
    },
    {
        'tripId': "2",
        'comments': u'Worst booking',
        'score': -3.0
    }
]

@app.route('/analysis', methods=['GET'])
def get_sentiments():
    neg,pos,neu = 0,0,0
    for review in reviews:
        if(review['score'] < 0):
            neg += 1
        elif(review['score']> 0):
            pos += 1
        else:
            neu += 1

    data = {
        "neg": neg,
        "pos": pos,
        "neu": neu
    }

    return jsonify(data), 200 


@app.route('/review', methods=['POST'])
def set_sentiments():
    print "Reached asdlhasodhajshdoash odhasodhoasi dias;";
    print request.json

    print "APPLE BANACNAa";
    if not request.json:
        abort(400)

    msg = request.json
    
    if msg['comments']:
        msg['score'] = find_score(msg['comments'])    
    
    reviews.append(msg)

    return jsonify({'review': msg}), 201




def find_score(text):
    return afinn.score(text)


if __name__ == '__main__':
    app.run(debug=True)