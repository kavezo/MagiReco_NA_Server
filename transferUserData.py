import json
import os
import sys
import uuid
import requests

host = 'https://android.magica-us.com'
userDir = 'data/user'

data1 = ['giftList', 'itemList', 'pieceList', 'gameUser', 'user', 'userCardList', 'userChapterList',
         'userCharaList', 'userDailyChallengeList', 'userDeckList', 'userDoppelList', 'userFollowList',
         'userFormationSheetList', 'userGiftList', 'userItemList']
data2 = ['userLimitedChallengeList', 'userList', 'userLive2dList', 'userPieceList', 'userPieceSetList',
         'userPieceCollectionList', 'userQuestAdventureList', 'userQuestBattleList', 'userSectionList',
         'userArenaBattle', 'userShopItem', 'userStatusList', 'userTotalChallengeList', 'userGachaGroupList']


def fetchData(transferId, transferPassword):
    os.makedirs(userDir)
    myUuid = uuid.uuid4()
    createResponse = post('/magica/api/user/create', myUuid)
    if json.loads(createResponse)['resultCode'] != 'success':
        raise ValueError(f'Error ${createResponse}')
    print(createResponse)
    transferResponse = post('/magica/api/user/transfer', myUuid,
                            {'password': transferPassword, 'personalId': transferId})
    if json.loads(transferResponse)['resultCode'] != 'success':
        raise ValueError(f'Error ${transferResponse}')
    print(transferResponse)
    fetchDataSet(myUuid, data1)
    fetchDataSet(myUuid, data2)
    fetchStoryCollection(myUuid)
    print('\nDone getting data')


def fetchStoryCollection(myUuid):
    dataResponse = get('/magica/api/page/StoryCollection', myUuid)
    dataBody = json.loads(dataResponse)
    print(f'Writing story collection...')
    with open(f'{userDir}/StoryCollection.json', 'w+', encoding='utf-8') as f:
        json.dump(dataBody, f, ensure_ascii=False)


def fetchDataSet(myUuid, dataSet):
    dataResponse = get('/magica/api/page/TopPage?value=' + ','.join(dataSet), myUuid)
    dataBody = json.loads(dataResponse)
    for dataName in dataSet:
        if dataName not in dataBody:
            continue
        with open(f'{userDir}/{dataName}.json', 'w+', encoding='utf-8') as f:
            print(f'Writing {dataName}...')
            json.dump(dataBody[dataName], f, ensure_ascii=False)


def post(path, reqUuid, jsonData=None):
    print(f'POST {host + path}')
    headers = {
        'client-os-ver': '5.1.1',
        'origin': 'https://android.magica-us.com',
        'x-platform-host': 'android.magica-us.com',
        'user-id-fba9x88mae': str(reqUuid),
        'client-model-name': 'SM-G965N',
        'user-agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G965N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
        'content-type': 'application/JSON',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'webview-session-id': '20201024222909',
        'x-requested-with': 'XMLHttpRequest',
        'client-session-id': '1',
        'f4s-client-ver': '1.2.0',
        'referer': 'https://android.magica-us.com/magica/index.html',
        'accept-encoding': 'gzip, deflate',
        'accept-language': '*'
    }
    response = requests.post(host + path, json=jsonData, headers=headers)
    if response.status_code not in range(200, 300):
        raise ValueError(f'Wrong POST response status: ${response.status_code}, body: ${response.text}')
    return response.text


def get(path, reqUuid):
    print(f'GET {host + path}')
    headers = {
        'user-id-fba9x88mae': str(reqUuid),
        'f4s-client-ver': '1.2.0'
    }
    response = requests.get(host + path, headers=headers)
    if response.status_code not in range(200, 300):
        raise ValueError(f'Wrong GET response status: ${response.status_code}, body: ${response.text}')
    return response.text


if __name__ == '__main__':
    if len(sys.argv) != 3:
        transferId = input("Enter Transfer ID: ")
        transferPassword = input("Enter Password: ")
        fetchData(transferId, transferPassword)
    else:
        fetchData(sys.argv[1], sys.argv[2])
