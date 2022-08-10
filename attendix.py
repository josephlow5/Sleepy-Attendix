import requests
import json
import glob


#>> INITIALIZING SESSION
ContentType='application/x-www-form-urlencoded'


def VerifyLogin(usr,pwd):
  s=requests.Session()
  HTTPPost=s.post('https://cas.apiit.edu.my/cas/v1/tickets',data={"username": usr, "password": pwd})
  if HTTPPost.status_code!=201: 
    return False
  else:
    return True

def SaveUser(usr,pwd,email):
  try:
    credentials={"secrets":{"usr": usr,"pwd": pwd},"personal_email":email}
    with open('users/{}.json'.format(usr),'w') as optFile:
        optFile.write(json.dumps(credentials))
    return True
  except:
    return False

def TakeAttendance(code):
  Count = 0
  for processing_user in glob.glob("users/*.json"):
    try:
      s=requests.Session()

      with open('{}'.format(processing_user),'r') as optFile:
          usr=json.load(optFile)['secrets']['usr']
      with open('{}'.format(processing_user),'r') as optFile:
          pwd=json.load(optFile)['secrets']['pwd']
      
      HTTPPost=s.post('https://cas.apiit.edu.my/cas/v1/tickets',data={'username': usr, 'password': pwd})

      #>> CREDENTIALS APPROVED, TGT CREATED 
      #>> ADVANCING THROUGH DOUBLE AUTH HANDSHAKE
      logonTicket=json.loads(str(HTTPPost.headers).replace("'", '"'))["Location"]
      initHandshake=s.post(logonTicket,headers= {"content-type": ContentType},params= {'service': 'https://cas.apiit.edu.my'})
      authTicket=s.get('https://cas.apiit.edu.my/cas/p3/serviceValidate',params={'format': 'json', 'service': 'https://cas.apiit.edu.my', 'ticket': initHandshake.text})
      print('\nLogged in as: '+str(json.loads(authTicket.text)['serviceResponse']['authenticationSuccess']['attributes']['givenName']).replace("'",''))

      #>> logon successful, build HTTP request with graphQL P/L.
      endpoint='https://attendix.apu.edu.my/graphql'
      graphqlContent='application/json'

      accessCtlReqHeaders='content-type,ticket,x-amz-user-agent,x-api-key'
      accessCtlReqMethod='POST'
      s.options(endpoint,headers={"host": 'attendix.apu.edu.my',"path": '/graphql' , "sec-fetch-dest": 'empty', "sec-fetch-mode": 'cors', "sec-fetch-site": 'same-site', "access-control-request-headers": accessCtlReqHeaders, "access-control-request-method": accessCtlReqMethod})
      agent='aws-amplify/1.0.1'
      key='da2-dv5bqitepbd2pmbmwt7keykfg4'

      # the fuck is this? at least it works only after this POST
      attendix=s.post(logonTicket,headers={"content-type": ContentType},params={'service': 'https://api.apiit.edu.my/attendix'}).text
      payload={"operationName":"updateAttendance","variables":{"otp":code},"query": "mutation updateAttendance($otp: String!) {\n  updateAttendance(otp: $otp) {\n    id\n    attendance\n    classcode\n    date\n    startTime\n    endTime\n    classType\n    __typename\n  }\n}\n"}
      attendUpdate=s.post(endpoint,headers={"host": 'attendix.apu.edu.my', "path": '/graphql', "content-type": graphqlContent, "sec-fetch-dest": 'empty', "sec-fetch-mode": 'cors', "sec-fetch-site": 'same-site', "ticket": attendix, "x-amz-user-agent": agent, "x-api-key": key},json=payload)
      try:
          feedbackMessage=((json.loads(str(attendUpdate.text))['errors'])[0])
          print(feedbackMessage['message']+'\n')
      except:
          classtyp=str(json.loads(attendUpdate.text)['data']['updateAttendance']['classType'])
          feedbackMessage="Success! Logged attendance for "+classtyp+': '+json.loads(str(attendUpdate.text))['data']['updateAttendance']['classcode']
          print(feedbackMessage)
          Count += 1
    except Exception as e:
        print(e+" ;User: "+usr)
  return Count