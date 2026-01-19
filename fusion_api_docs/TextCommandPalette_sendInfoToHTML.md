# TextCommandPalette.sendInfoToHTML Method

Parent Object: [TextCommandPalette](TextCommandPalette.md)  

## Description

Sends the string to the JavaScript associated with the loaded HTML.

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

"textCommandPalette_var" is a variable referencing a [TextCommandPalette](TextCommandPalette.md) object.

```python
returnValue = textCommandPalette_var.sendInfoToHTML(action, data)
```

## Return Value

| Type | Description |
| --- | --- |
| string | Returns a string that can be anything that your JavaScript code generates. The JavaScript should always return some content because an empty string is used to indicate a failure. If useNewWebBrowser flag is set to true while creating the palette control this API call will be asynchronous and an empty string is returned. Response will come in data field of HTMLEvent with action equal to 'response'. |

## Parameters

| Name | Type | Description |
|----|----|----|
| action | string | The "action" string to pass to the JavaScript associated with the HTML. This string can be anything but will typically be JSON formatted information. |
| data | string | The "data" string to pass to the JavaScript associated with the HTML. This string can be anything but will typically be JSON formatted information. |

## Version

Introduced in version August 2017  

