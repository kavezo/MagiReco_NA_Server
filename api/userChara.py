import json
import flask

def sale():
    body = flask.request.json
    charaId = body['charaId']
    amount = body['num']

    with open('data/user/userCharaList.json', encoding='utf-8') as f:
        userCharaList = json.load(f)

    rarity = 0
    saleItemId = None
    responseCharaList = []
    for i in range(len(userCharaList)):
        if userCharaList[i]['charaId'] == charaId:
            userCharaList[i]['lbItemNum'] -= amount
            rarity = int(userCharaList[i]['chara']['defaultCard']['rank'][-1])
            saleItemId = userCharaList[i]['chara']['maxSaleItemId'] if 'maxSaleItemId' in userCharaList[i]['chara'] \
                else userCharaList[i]['chara']['saleItemId']
            responseCharaList.append(userCharaList[i])
            break
        if userCharaList[i]['lbItemNum'] < 0:
            flask.abort(400, description='{"errorTxt": "You don\'t have that many gems to sell >:(","resultCode": "error","title": "Error"}')
            return

    gemsReceived = [1, 1, 3, 10]
    responseItemList = []
    with open('data/user/userItemList.json', encoding='utf-8') as f:
        itemList = json.load(f)
    for i in range(len(itemList)):
        if itemList[i]['itemId'] == 'PRISM':
            itemList[i]['quantity'] += amount * gemsReceived[rarity-1]
            responseItemList.append(itemList[i])
    if rarity == 4:
        for i in range(len(itemList)):
            if itemList[i]['itemId'] == 'DESTINY_CRYSTAL':
                itemList[i]['quantity'] += amount
                responseItemList.append(itemList[i])

    with open('data/user/userCharaList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCharaList, f, ensure_ascii=False)
    with open('data/user/userItemList.json', 'w+', encoding='utf-8') as f:
        json.dump(itemList, f, ensure_ascii=False)
    
    response = {
        "resultCode": "success",
        'userCharaList': responseCharaList,
        'userItemList': responseItemList
    }
    return flask.jsonify(response)

def visualize():
    body = flask.request.json
    response = {
        "resultCode": "success"
    }

    with open('data/user/userCardList.json', encoding='utf-8') as f:
        userCardList = json.load(f)
    
    for i in range(len(userCardList)):
        if userCardList[i]['card']['charaNo'] == body['charaId']:
            userCardList[i]['displayCardId'] = body['displayCardId']
            response['userCardList'] = userCardList

    with open('data/user/userCardList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCardList, f, ensure_ascii=False)

    with open('data/user/userCharaList.json', encoding='utf-8') as f:
        userCharaList = json.load(f)

    for i in range(len(userCharaList)):
        if userCharaList[i]['charaId'] == body['charaId']:
            userCharaList[i]['commandVisualId'] = body['commandVisualId']
            userCharaList[i]['commandVisualType'] = body['commandVisualType']
            response['userCharaList'] = [userCharaList[i]]

    with open('data/user/userCharaList.json', 'w+', encoding='utf-8') as f:
        json.dump(userCharaList, f, ensure_ascii=False)

    return flask.jsonify(response)
    
def handleUserChara(endpoint):
    if endpoint.startswith('sale'):
        return sale()
    elif endpoint.startswith('visualize'):
        return visualize()
    else:
        print('userChara/'+endpoint)
        flask.abort(501, description="Not implemented")