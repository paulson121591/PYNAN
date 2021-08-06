import json

import requests

import Ynab_Fetch
import keyyah


key=keyyah.NOTION_API
base_url = "https://api.notion.com/v1/databases/"
db_id = "0f8c25150551494480ce4036087dc795"
query={}
header = {
    "Authorization": "Bearer " + key,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"}


def dic_decoder(x):
    return [i for i in x]

def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

def createPage(databaseId, headers,check_bal,save_bal):
    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {

        "parent": {"database_id": databaseId},
        "properties": {"Name": {
                "title": [
                    {
                        "text": {
                            "content": "Update"
                        }
                    }
                ]
            },

            "Checking": {
    "number": check_bal
  },
            "Savings": {
                "number": save_bal
            }
}
    }

    data = json.dumps( newPageData )
    # print(str(uploadData))

    res = requests.request( "POST", createUrl, headers=headers, data=data )

    print( res.status_code)

def update():
    check_bal = Ynab_Fetch.get_check_bal()
    save_bal = Ynab_Fetch.get_save_bal()
    createPage(db_id,header,check_bal,save_bal)