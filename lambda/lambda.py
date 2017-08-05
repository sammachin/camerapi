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
    message_id = event['header']['messageId']
    payload = ''
    header = {
        "namespace": "Alexa.ConnectedHome.Discovery",
        "name": "DiscoverAppliancesResponse",
        "payloadVersion": "2",
        "messageId": message_id
        
        }
    if event['header']['name'] == 'DiscoverAppliancesRequest':
        payload = {
                   "discoveredAppliances": [
                   {
                       "applianceId": "001",
                       "manufacturerName": "CameraPi",
                       "modelName": "CameraPi",
                       "version": "0.9",
                       "friendlyName": "office camera",
                       "friendlyDescription": "Camera Pi in Office",
                       "isReachable": True,
                       "actions": [
                           "retrieveCameraStreamUri"
                       ],
                       "applianceTypes":[
                           "CAMERA"
                       ],
                       "additionalApplianceDetails": {
                           "extraDetail1": "None"
                       }
                   }
                ]
            }
    return { 'header': header, 'payload': payload }

def handleQuery(context, event):
    payload = ''
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
              "value":"rtsp://officecamerapi.dev-cloud.co.uk:443/h264"
          },
          "imageUri": {
              "value":"https://s3.sammachin.com/loading.jpg"

            }
        }
    return { 'header': header, 'payload': payload }