# BrowserCommandInput.sendInfoToHTML Method

Parent Object: [BrowserCommandInput](BrowserCommandInput.md)  

## Description

Sends a string to the JavaScript associated with the loaded HTML.

## Remarks

A variation of the event handler below should be implemented in the JavaScript associated with the HTML to receive the data. The event will be triggered by Fusion whenever the sendInfoToHTML method is called.  

```python
window.fusionJavaScriptHandler = {
   handle: function(actionString, dataString){
       confirm('Action from Fusion: ' + actionString);
       confirm('Data from Fusion: ' + dataString);

       // Build up JSON return string.
       var result = {};
       result.status = 'OK';
       var response = JSON.stringify(result);
       return response;
   }
};
```

Your JavaScript code should always return something in response because an empty string response is assumed to be a failure.

## Syntax

"browserCommandInput_var" is a variable referencing a [BrowserCommandInput](BrowserCommandInput.md) object.

```python
returnValue = browserCommandInput_var.sendInfoToHTML(action, data)
```

## Return Value

| Type | Description |
|----|----|
| boolean | This API call is asynchronous and true is returned if the send was successful. Any response from the JavaScript response will be returned through the incomingFromHTML event using the data field of the provided HTMLEvent object where the action property is "response". |

## Parameters

| Name | Type | Description |
|----|----|----|
| action | string | The "action" string to pass to the JavaScript associated with the HTML. This string can be anything but will typically be JSON formatted information. |
| data | string | The "data" string to pass to the JavaScript associated with the HTML. This string can be anything but will typically be JSON formatted information. |

## Version

Introduced in version July 2021  

