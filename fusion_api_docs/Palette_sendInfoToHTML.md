# Palette.sendInfoToHTML Method

Parent Object: [Palette](Palette.md)  

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

"palette_var" is a variable referencing a [Palette](Palette.md) object.

```python
returnValue = palette_var.sendInfoToHTML(action, data)
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

## Samples

| Name | Description |
| --- | --- |
| [Palette Sample](PaletteSample_Sample.md) | Demonstrates how to create a palette, how to dock and snap palettes and how Fusion communicates with the palette HTML. The sample is an add-in. To use it, create a new Python add-in and replace the code with the code below. You also need to create an html file using the name and code below. The html file needs to be in the same folder as the py file. When you load the add-in, you'll see two new commands under the ADD-INS panel of the TOOLS tab. The "Show Custom Palette" command will cause the custom palette to be displayed. It will remain displayed until you click its Close button. Clicking the "Click to send info to Fusion" button on the palette, will send information to your add-in, which uses the API to display that information in a message box. Running the "Send Info to HTML" command to send data to the javascript running in the palette, which uses it to update the content of a paragraph. palette.html      Click the button below to send data to Fusion. Click to send info to Fusion Run the "Send Info to HTML" command in the ADD-INS panel to update this text.      function sendInfoToFusion(){ var today = new Date(); var dd = String(today.getDate()).padStart(2, '0'); var mm = String(today.getMonth() + 1).padStart(2, '0'); var yyyy = today.getFullYear(); var hours = String(today.getHours()).padStart(2, '0'); var minutes = String(today.getMinutes()).padStart(2, '0'); var seconds = String(today.getSeconds()).padStart(2, '0'); var date = dd + '/' + mm + '/' + yyyy; var time = hours + ':' + minutes + ':' + seconds; var args = { arg1 : "Sample argument 1", arg2 : "Sample argument 2" }; adsk.fusionSendData('send', JSON.stringify(args)); } window.fusionJavaScriptHandler = {handle: function(action, data){ try { if (action == 'send') { // Update a paragraph with the data passed in. document.getElementById('p1').innerHTML = data; } else if (action == 'debugger') { debugger; } else { return 'Unexpected command type: ' + action; } } catch (e) { console.log(e); console.log('exception caught with command: ' + action + ', data: ' + data); } return 'OK'; }};   |

## Version

Introduced in version March 2017  

