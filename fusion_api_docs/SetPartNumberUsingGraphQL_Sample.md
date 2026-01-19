# Set part number using GraphQL

## Description

Sets part number of root component and from occurrences via GQL query.

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
3. Access Model IDs
   Inside the event handler, the script retrieves rootDataComponent from the design.
   If the mfgdmModelId is available, it stores the model ID in modelIds set.
4. Set Part Numbers Using GraphQL
   The setPNFromGql function constructs and sends a GraphQL mutation request to the MFGDM
   service using the collected modelIds. It sets part numbers and logs them.
   Part numbers are set sequentially like PN-1, PN-2, depending on the number of components.
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
        
        # Empty set to collect unique modelIds.
        modelIds = set()

        # Get the active design from the document provided by the event.
        design: adsk.fusion.Design = args.document.products.itemByProductType('DesignProductType')
        
        # Get the DataComponent from the root component and add its MFGDM ID to the set.
        data = design.rootDataComponent
        app.log(f'root model id: {data.mfgdmModelId}, timestamp: {data.timestamp}')
        if data.mfgdmModelId:
            modelIds.add(data.mfgdmModelId)
        else:
            app.log(f'Root Component does not have a valid mfgdmModelId.')
        
        # Add the MFGDM ID and timestamp of each occurrence.
        for occ in design.rootComponent.allOccurrences:
            if data := occ.dataComponent:
                app.log(f'occurrence: {occ.fullPathName}, model id: {data.mfgdmModelId}, timestamp: {data.timestamp}')
                modelIds.add(data.mfgdmModelId)
            else:
                app.log(f'Occurrence does not have DataComponent')
        
        # Log information for all components
        for comp in design.allComponents:
            app.log(f'comp: {comp.name}, model id: {comp.mfgdmModelId}')

        # Check if modelIds is empty before proceeding to set part numbers
        if not modelIds:
            app.log('No model ID to set part number.')
        else:
            # Call the funtion tp set PartNumber for each unique modelId
            # Part numbers are set sequentially like PN-1, PN-2, depending on the number of components.
            for index, modelId in enumerate(modelIds, start=1):
                partNumber = f'PN-{index}'
                setPNFromGql(modelId, partNumber)

# Connect to the mfgdmDataReady event.
def mfgdm_data_ready():
    """Register the MFGDMData ready event handler."""
    global mfgdmDataReadyHandler
    mfgdmDataReadyHandler = MFGDMDataReadyEventHandler()
    app.mfgdmDataReady.add(mfgdmDataReadyHandler)

def setPNFromGql(modelId, partNumber):
    """Set part number from the GraphQL endpoint using modelId."""

    # Use HTTP Request for mutation call to set the part number.
    request = adsk.core.HttpRequest.create(mfgdm_url, adsk.core.HttpMethods.PostMethod)
    request.setHeader('Content-type', 'application/json; charset=utf-8')

    # Define the GraphQL query as a string
    graphql_query = '''
        mutation ($input: AssignPartNumberInput!) {
            assignModelPartNumber(input: $input) {
                model {
                    component {
                        partNumber {
                            displayValue
                        }
                    }
                }
            }   
        }
    '''

    # Create a dictionary to represent the GraphQL request payload
    input = {'modelId': modelId, 'partNumber': partNumber}
    payload = {
        'query': graphql_query,
        'variables': {'input': input}
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
        app.log(f'Failed to set part number with status code {response.statusCode}')
```

