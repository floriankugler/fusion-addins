# Get part number using GraphQL

## Description

Fetches part number of root component and from occurrences via GQL query.

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
Overview of the steps demonstrated:
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
4. Fetch Part Numbers Using GraphQL
   The fetchPNFromGql function constructs and sends a GraphQL request to the MFGDM
   service using the collected modelIdsWithTime. It retrieves part numbers and logs them.
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
        """This method is called when the mfgdm data ready event occurs."""
        
        # Empty set to collect unique modelId and time pairs.
        modelIdsWithTime = set()

        # Get the active design from the document provided by the event.
        design: adsk.fusion.Design = args.document.products.itemByProductType('DesignProductType')
        
        # Get the DataComponent from the root component and add its MFGDM ID and timestamp to the set.
        data = design.rootDataComponent
        app.log(f'root model id: {data.mfgdmModelId}, timestamp: {data.timestamp}')
        if data.mfgdmModelId:
            modelIdsWithTime.add((data.mfgdmModelId, data.timestamp))
        else:
            app.log(f'Root Component does not have a valid mfgdmModelId.')
        
        # Add the MFGDM ID and timestamp of each occurrence.
        for occ in design.rootComponent.allOccurrences:
            if data := occ.dataComponent:
                app.log(f'occurrence: {occ.fullPathName}, model id: {data.mfgdmModelId}, timestamp: {data.timestamp}')
                modelIdsWithTime.add((data.mfgdmModelId, data.timestamp))
            else:
                app.log(f'Occurrence does not have DataComponent')
        
        # Log information for all components
        for comp in design.allComponents:
            app.log(f'comp: {comp.name}, model id: {comp.mfgdmModelId}')

        # Check if modelIdsWithTime is empty before proceeding to fetch part numbers.
        if not modelIdsWithTime:
            app.log('No model ID to fetch part number.')
        else:
            # Call the function to get the part numbers.
            for modelId, time in modelIdsWithTime:
                fetchPNFromGql(modelId, time)

# Connect to the mfgdmDataReady event.
def mfgdm_data_ready():
    """Register the MFGDMData ready event handler."""
    global mfgdmDataReadyHandler
    mfgdmDataReadyHandler = MFGDMDataReadyEventHandler()
    app.mfgdmDataReady.add(mfgdmDataReadyHandler)

def fetchPNFromGql(modelId, time):
    """Fetch part number from the GraphQL endpoint using modelId and time."""

    # Use HTTP Request to query for the part number.
    request = adsk.core.HttpRequest.create(mfgdm_url, adsk.core.HttpMethods.PostMethod)
    request.setHeader('Content-type', 'application/json; charset=utf-8')

    # Define the GraphQL query as a string.
    graphql_query = '''
        query ($modelId: ID!, $time: DateTime) {
            model(modelId: $modelId, time: $time) {
                component {
                    partNumber {
                        displayValue
                    }
                }
            }
        }
    '''

    # Create a dictionary to represent the GraphQL request payload
    variables = {'modelId': modelId}
    # Only pass 'time' if it is not an empty string
    if time:
        variables['time'] = time

    payload = {
        'query': graphql_query,
        'variables': variables
    }

    # Convert the payload to a JSON string
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
        app.log(f'Failed to fetch part number with status code {response.statusCode}')
```

