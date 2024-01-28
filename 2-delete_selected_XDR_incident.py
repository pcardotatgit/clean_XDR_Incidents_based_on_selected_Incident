'''
    utils for deleting demo XDR incidents, sightings, judgments and relationships in the XDRs tenant
    this script delete every objects ID contained into the following files
    
    ./result/z_sightings_id_list.txt
    ./result/z_incidents_id_list.txt
    ./result/z_relationships_id_list.txt
'''
import requests
import json
from crayons import *
import sys

host = ""
host_for_token=""
ctr_client_id=""
ctr_client_password=""

item_list=[]

def parse_config(text_content):
    text_lines=text_content.split('\n')
    conf_result=['','','','','','','']
    for line in text_lines:
        print(green(line,bold=True))
        if 'ctr_client_id' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[0]=line.split('=')[1]
                conf_result[0]=conf_result[0].replace('"','')
                conf_result[0]=conf_result[0].replace("'","")
            else:
                conf_result[0]=""
        elif 'ctr_client_password' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[1]=line.split('=')[1]
                conf_result[1]=conf_result[1].replace('"','')
                conf_result[1]=conf_result[1].replace("'","")
            else:
                conf_result[1]=""        
        elif '.eu.amp.cisco.com' in line:
            conf_result[2]="https://private.intel.eu.amp.cisco.com" 
            conf_result[6]="https://visibility.eu.amp.cisco.com"
        elif '.intel.amp.cisco.com' in line:
            conf_result[2]="https://private.intel.amp.cisco.com"   
            conf_result[6]="https://visibility.amp.cisco.com"
        elif '.apjc.amp.cisco.com' in line:
            conf_result[2]="https://private.intel.apjc.amp.cisco.com"
            conf_result[6]="https://visibility.apjc.amp.cisco.com"
        elif 'SecureX_Webhook_url' in line:
            words=line.split('=')
            if len(words)==2:        
                print(yellow(words))        
                conf_result[3]=words[1]
                conf_result[3]=conf_result[3].replace('"','')
                conf_result[3]=conf_result[3].replace("'","")                
            else:
                conf_result[3]=""
        elif 'webex_bot_token' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[5]=line.split('=')[1]
                conf_result[5]=conf_result[5].replace('"','')
                conf_result[5]=conf_result[5].replace("'","")
            else:
                conf_result[5]=""        
        elif 'webex_room_id' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[4]=line.split('=')[1]
                conf_result[4]=conf_result[4].replace('"','')
                conf_result[4]=conf_result[4].replace("'","")
            else:
                conf_result[4]=""        
    print(yellow(conf_result))
    return conf_result
    
def read_api_keys(service):   
    # read API credentials from an external file on this laptop ( API keys are not shared with the flask application )
    if service=="webex":
        with open('../keys/webex_keys.txt') as creds:
            text=creds.read()
            cles=text.split('\n')
            ACCESS_TOKEN=cles[0].split('=')[1].strip()
            ROOM_ID=cles[1].split('=')[1].strip()
            #print(ACCESS_TOKEN,ROOM_ID) 
            return(ACCESS_TOKEN,ROOM_ID)
    if service=="ctr":
        if ctr_client_id=='paste_CTR_client_ID_here':
            with open('../keys/ctr_api_keys.txt') as creds:
                text=creds.read()
                cles=text.split('\n')
                client_id=cles[0].split('=')[1]
                client_password=cles[1].split('=')[1]
                #access_token = get_token()
                #print(access_token) 
        else:
            client_id=ctr_client_id
            client_password=ctr_client_password
        return(client_id,client_password)
    if service=="kenna":
        if kenna_token=='paste_kenna_token_here':
            with open('../keys/kenna.txt') as creds:
                access_token=creds.read()
                #print(access_token)          
        else:
            access_token=kenna_token   
        return(access_token)

def get_ctr_token(host_for_token,ctr_client_id,ctr_client_password):
    print(yellow('Asking for new CTR token',bold=True))
    url = f'{host_for_token}/iroh/oauth2/token'
    #url = 'https://visibility.eu.amp.cisco.com/iroh/oauth2/token'
    print()
    print(url)
    print()    
    headers = {'Content-Type':'application/x-www-form-urlencoded', 'Accept':'application/json'}
    payload = {'grant_type':'client_credentials'}
    print()
    print('ctr_client_id : ',green(ctr_client_id,bold=True))
    print('ctr_client_password : ',green(ctr_client_password,bold=True))
    response = requests.post(url, headers=headers, auth=(ctr_client_id, ctr_client_password), data=payload)
    #print(response.json())
    reponse_list=response.text.split('","')
    token=reponse_list[0].split('":"')
    print(token[1])
    fa = open("ctr_token.txt", "w")
    fa.write(token[1])
    fa.close()
    return (token[1])
    
def delete_incidents(access_token):
    headers = {'Authorization':'Bearer {}'.format(access_token), 'Content-Type':'application/json', 'Accept':'application/json'}
    line_content = []
    with open('./result/z_incidents_id_list.txt') as inputfile:
    	for line in inputfile:
    		line_content.append(line.strip())

    # loop through all urls in z_judgements_id_list.txt ( judgment ids ) and delete them
    for url in line_content:
        #  notice url in z_judgements_id_list.txt are actually the full url with judgment IDs
        print (green(url,bold=True))
        response = requests.delete(url, headers=headers)
        print()
        print (yellow(response,bold=True))     
        
def delete_sightings(access_token):
    headers = {'Authorization':'Bearer {}'.format(access_token), 'Content-Type':'application/json', 'Accept':'application/json'}
    line_content = []
    with open('./result/z_sightings_id_list.txt') as inputfile:
    	for line in inputfile:
    		line_content.append(line.strip())

    # loop through all urls in z_judgements_id_list.txt ( judgment ids ) and delete them
    for url in line_content:
        #  notice url in z_judgements_id_list.txt are actually the full url with judgment IDs
        print (green(url,bold=True))
        response = requests.delete(url, headers=headers)
        print()
        print (yellow(response,bold=True))      
        
def delete_judgments(access_token):
    headers = {'Authorization':'Bearer {}'.format(access_token), 'Content-Type':'application/json', 'Accept':'application/json'}
    line_content = []
    with open('./result/z_judgements_id_list.txt') as inputfile:
    	for line in inputfile:
    		line_content.append(line.strip())

    # loop through all urls in z_judgements_id_list.txt ( judgment ids ) and delete them
    for url in line_content:
        #  notice url in z_judgements_id_list.txt are actually the full url with judgment IDs
        print (green(url,bold=True))
        response = requests.delete(url, headers=headers)
        print()
        print (yellow(response,bold=True))  

def delete_relationships(access_token):
    headers = {'Authorization':'Bearer {}'.format(access_token), 'Content-Type':'application/json', 'Accept':'application/json'}
    line_content = []
    with open('./result/z_relationships_id_list.txt') as inputfile:
    	for line in inputfile:
    		line_content.append(line.strip())
    for url in line_content:
        print (green(url,bold=True))
        response = requests.delete(url, headers=headers)
        print()
        print (yellow(response,bold=True))         

def main():
    with open('config.txt','r') as file:
        text_content=file.read()
    ctr_client_id,ctr_client_password,host,SecureX_Webhook_url,DESTINATION_ROOM_ID,BOT_ACCESS_TOKEN,host_for_token = parse_config(text_content)
    print('host : ',host)
    print(yellow("Step 1 ask for an access token to CTR",bold=True))
    access_token=get_ctr_token(host_for_token,ctr_client_id,ctr_client_password)
    print(green("Ok Token = Success",bold=True))
    print(yellow("Step 2 delete incidents",bold=True))     
    delete_incidents(access_token)
    print(green("Ok Success",bold=True))    
    print(yellow("Step 3 delete sightings",bold=True))     
    delete_sightings(access_token)
    print(green("Ok Success",bold=True))
    print(yellow("Step 4 delete relationships",bold=True))   
    delete_relationships(access_token)
    print(yellow("Step 5 delete judgments : WE DONT DELETE JUDGMENTS YET !!",bold=True))   
    #delete_judgments(access_token)
    print(green("Ok All Done ",bold=True))
if __name__ == "__main__":
    main()
