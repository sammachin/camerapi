import json

def loadcams():
    with open('cameras.json') as f:
        cameras = json.loads(f.read())
    return cameras
    
def lambda_handler(event, context):
    access_token = event['payload']['accessToken']

    if event['header']['namespace'] == 'Alexa.ConnectedHome.Discovery':
        return handleDiscovery(context, event)

    elif event['header']['namespace'] == 'Alexa.ConnectedHome.Query':
        return handleQuery(context, event)

def handleDiscovery(context, event):
    cameras= loadcams()
    message_id = event['header']['messageId']
    header = {
        "namespace": "Alexa.ConnectedHome.Discovery",
        "name": "DiscoverAppliancesResponse",
        "payloadVersion": "2",
        "messageId": message_id
        }
    if event['header']['name'] == 'DiscoverAppliancesRequest':
        appliances = []
        for c in cameras:
            a = {
                       "manufacturerName": "CameraPi",
                       "modelName": "CameraPi",
                       "version": "1.0",                  
                       "isReachable": True,
                       "actions": [
                           "retrieveCameraStreamUri"
                       ],
                       "applianceTypes":[
                           "CAMERA"
                       ]
                   }
            a["applianceId"] = c
            a["friendlyName"] =  cameras[c]['friendlyName']
            a["friendlyDescription"] = cameras[c]['friendlyDescription']
            appliances.append(a)
        payload = {"discoveredAppliances": appliances}
    return { 'header': header, 'payload': payload }

def handleQuery(context, event):
    cameras= loadcams()
    device_id = event['payload']['appliance']['applianceId']
    message_id = event['header']['messageId']
    header = {
        "namespace":"Alexa.ConnectedHome.Query",
        "name":"RetrieveCameraStreamUriResponse",
        "payloadVersion":"2",
        "messageId": message_id
        }
    if event['header']['name'] == 'RetrieveCameraStreamUriRequest':
        payload = {
          "uri": {
              "value": cameras[device_id]["uri"]
          },
          "imageUri": {
              "value":"https://s3.sammachin.com/loading.jpg"

            }
        }
    return { 'header': header, 'payload': payload }