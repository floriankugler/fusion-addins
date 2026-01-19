# Gets all properties using GraphQL

## Description

Fetches bulk component properties of the root component and from occurrences via single GraphQL query.

## Code Samples

| Copy Code |
|----------:|

```python
"""This file acts as the main module for this script."""

import traceback
import adsk.core
import adsk.fusion
import json

''' 
Overview of the steps demonstrated.
1. Register the mfgdmDataReady event.
   Before accessing cloud metadata such as mfgdmModelId, ensure the data is ready.
   Register the MFGDMDataReadyEventHandler at the beginning of your script execution
   in the mfgdm_data_ready() method.
2. Implement the MFGDMDataReadyEventHandler
   This event fires when the cloud model data is fully initialized and accessible.
   Use the notify method to access mfgdmModelId from the design or component level.
3. Access Model IDs and Timestamps
   Inside the event handler, the script retrieves rootDataComponent from the design.
   If the mfgdmModelId is available, it stores the model ID and timestamp pair in modelIdsWithTime.
4. Fetch Bulk Properties Using GraphQL
   The bulkCompProps function constructs and sends a GraphQL request to the MFGDM
   service using the collected modelIdsWithTime. It retrieves properties like part
   numbers and descriptions and logs them.
'''

# Initialize the global variables for the Application and UserInterface objects.
app = adsk.core.Application.get()
ui  = app.userInterface
mfgdm_url = 'mfgdm://v3'


def run(_context: str):
    """This function is called by Fusion when the script is run."""

    try:
        mfgdm_data_ready()
        adsk.autoTerminate(False)
    except:  #pylint:disable=bare-except
        app.log(f'Failed:\n{traceback.format_exc()}')


mfgdmDataReadyHandler: adsk.core.MFGDMDataEventHandler = None


class MFGDMDataReadyEventHandler(adsk.core.MFGDMDataEventHandler):
    """This class handles the mfgdm data ready event."""

    def notify(self, args: adsk.core.MFGDMDataEventArgs):
        """This method is called when the mfgdmDataReady event occurs."""
        
        modelIdsWithTime = set()

        # Get the active design from the document provided by the event.
        design: adsk.fusion.Design = args.document.products.itemByProductType('DesignProductType')
        
        # Get the DataComponent from the root component and add its MFGDM ID and timestamp to the set.
        data = design.rootDataComponent
        if data.mfgdmModelId:
            modelIdsWithTime.add((data.mfgdmModelId, data.timestamp))

        # Add the MFGDM ID and timestamp of each occurrence.
        for occ in design.rootComponent.allOccurrences:
            if data := occ.dataComponent:
                modelIdsWithTime.add((data.mfgdmModelId, data.timestamp))
        
        # Check if modelIdsWithTime is empty before proceeding to fetch comp properties
        if not modelIdsWithTime:
            app.log('No model ID to fetch component ID.')
        else:
            # Call the function to get the properties.
            bulkCompProps(list(modelIdsWithTime))

# Connect to the mfgdmDataReady event.            
def mfgdm_data_ready():
    global mfgdmDataReadyHandler
    mfgdmDataReadyHandler = MFGDMDataReadyEventHandler()
    app.mfgdmDataReady.add(mfgdmDataReadyHandler)


# Divide the query into chunks.
def divide_into_chunks(lst, n=50):
    """Divides a list into chunks of size n (default is 50) as bulk models has limit of 50 models per request."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n ]


def bulkCompProps(componentIdsAtTime):
    """Fetches component properties from the GraphQL endpoint using modelId and time."""

    for chunk in divide_into_chunks(componentIdsAtTime):
        # Use HTTP Request to query for the properties of each chunk.
        request = adsk.core.HttpRequest.create(mfgdm_url, adsk.core.HttpMethods.PostMethod)
        request.setHeader('Content-type', 'application/json; charset=utf-8')

        # Define the GraphQL query as a string
        graphql_query = '''
            query ($input:[BulkModelsQueryInput!]!) {
                bulkModels(input: $input) {
                    model {
                        component {
                            description {
                                value
                            }
                            partNumber {
                                value
                            }
                        }
                    }
                }
            }
        '''
    
        inputArr = [{'modelId': modelId} if not time else {'modelId': modelId, 'time': time} for modelId, time in chunk]

        # Convert the payload to a JSON string
        payload = {
            'query': graphql_query,
            'variables': {'input': inputArr}
        }

        request.data = json.dumps(payload)
        app.log(f'json_payload: {request.data}')

        headers = request.headers()
        app.log(f'headers: {str(headers)}')
        response = request.executeSync()
        app.log(f'Response Code: {response.statusCode}')

        if response.statusCode == 200:
            # Write the result to the TEXT COMMAND window.
            response_json = json.loads(response.data)
            app.log(f'Response JSON:\n{json.dumps(response_json)}')
        else:
            app.log(f'Failed to fetch properties with status code {response.statusCode}')
```

