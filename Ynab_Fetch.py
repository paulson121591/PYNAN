from __future__ import print_function
import time
import ynab
from ynab.rest import ApiException
from pprint import pprint
import easygui
import ToNotion
import datetime
from datetime import date, timedelta
import keyyah


token=keyyah.YNAB_API
configuration = ynab.Configuration()
configuration.api_key['Authorization'] =token
configuration.api_key_prefix['Authorization'] = 'Bearer'
configuration.host = "https://api.youneedabudget.com/v1"

api_instance = ynab.AccountsApi(ynab.ApiClient(configuration))
budget_id = 'ea49f28d-e5d6-4c75-a89d-773acd1e9509'
c_account_id = '6aff5e43-085e-4c50-8f6c-705fee38dd0a'
s_account_id='b0d223ab-a8c1-4b62-bd37-4257f5cbe05e'


def dic_decoder(x):
    return [i for i in x]

def get_check_bal():
    try:
        # Single account
        #api_response =api_instance.get_accounts(budget_id)
        api_response = api_instance.get_account_by_id(budget_id, c_account_id)
        account_data= api_response.data.to_dict()
        c_account_bal=account_data['account']['balance']
        c_account_bal = int(c_account_bal)/1000

    except ApiException as e:
        print("Exception when calling AccountsApi->get_account_by_id: %s\n" % e)
        c_account_bal=88888888

    return c_account_bal

def get_save_bal():
    try:
        # Single account
        #api_response =api_instance.get_accounts(budget_id)
        api_response = api_instance.get_account_by_id(budget_id, s_account_id)
        account_data= api_response.data.to_dict()
        s_account_bal=account_data['account']['balance']
        s_account_bal = int(s_account_bal)/1000

    except ApiException as e:
        print("Exception when calling AccountsApi->get_account_by_id: %s\n" % e)
        s_account_bal=8888888888888

    return s_account_bal

def get_categories():
    api_instance = ynab.CategoriesApi( ynab.ApiClient( configuration ) )
    try:
        api_response = api_instance.get_categories( budget_id )
        categories_info=api_response.data.to_dict()
        # pprint( categories_info['category_groups'] [0]['categories'])
        d=categories_info['category_groups']
        # category_name = categories_info['category_groups'][info]['categories'][num_2]['name']
        warning_list=[]
        cat = {}
        for v in d:
            x=v['categories']
            print( '\n' )
            print(v['name'])
            for sv in x:
                name =sv['name']
                balance=sv['balance']
                balance=balance/1000
                cat[name]=balance
                print(cat.values())
                if balance < 0:
                    warning_list.append(name)



        return cat







    except ApiException as e:
        print( "Exception when calling CategoriesApi->get_categories: %s\n" % e )




def waringing_list_maker(cat):
    waringing_list=[]
    for i in cat:
        print(cat)
        val=cat.get(i)
        print(type(val))
        if val < 0:
            print(i)
            waringing_list.append(i+": "+str(val)+"\n")
    return waringing_list



def category_orginizer(cat):
    item = 0
    item_list=[]
    for i in cat:
        value=cat.get(i)
        item_list.append(i+": "+ str(value)+'\n')
    return item_list


def transactions():
    get_date=date.today()- timedelta(5)
    api_instance = ynab.TransactionsApi( ynab.ApiClient( configuration ) )
    api_response = api_instance.get_transactions( budget_id, since_date=get_date )
    trans_info=api_response.data.to_dict()

    trans=trans_info['transactions']
    recent_transactions=[]
    for t in trans:
        category_name=t['category_name']
        payee_name=t['payee_name']
        account_name=t['account_name']
        amount=t['amount']/1000
        recent_transactions.append(payee_name + ": $" + str( amount )+"\n")
    return recent_transactions




def gui():
    action=easygui.buttonbox('What would you like to do?','Actions',
                             ['See Categories','See Warning Categories' ,'Get Account Balances'
                                ,'Recent Transactions',
                              'Upload info to notion'])
    if action == 'See Categories':
        categories_info = get_categories()
        categories_info_pretty = category_orginizer( categories_info )

        easygui.codebox( "Categories", 'Info', categories_info_pretty )
        gui()
    if action == 'See Warning Categories':
        categories_info = get_categories()
        waringing_list = waringing_list_maker( categories_info )

        easygui.codebox( 'WARNINGS', 'Info', waringing_list )
        gui()

    if action == 'Get Account Balances':
        bal_s = get_save_bal()
        bal_c = get_check_bal()
        easygui.codebox( 'Account Balances', 'Account Balances','Checking: $'+str(bal_c)+
                         '\n'+'Savings: $'+str(bal_s) )
        gui()
    if action=='Recent Transactions':
        recent_transactions=transactions()
        easygui.codebox( 'Recent Transactions', 'Recent Transactions', recent_transactions )
        gui()


    if action == 'Upload info to notion':
        ToNotion.update()
        gui()
    return action





# get_save_bal()
# get_check_bal()
# wl=get_categories(









