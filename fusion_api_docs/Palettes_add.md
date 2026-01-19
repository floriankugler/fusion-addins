# Palettes.add Method

Parent Object: [Palettes](Palettes.md)  

## Description

Creates a new Palette.

## Syntax

"palettes_var" is a variable referencing a [Palettes](Palettes.md) object.

```python
# Uses no optional arguments.
returnValue = palettes_var.add(id, name, htmlFileURL, isVisible, showCloseButton, isResizable)

# Uses optional arguments.
returnValue = palettes_var.add(id, name, htmlFileURL, isVisible, showCloseButton, isResizable, width, height, useNewWebBrowser)
```

## Return Value

| Type | Description |
|----|----|
| [Palette](Palette.md) | Returns the newly created palette or null in the case the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique id for this palette. The id must be unique with respect to all of the palettes. |
| name | string | The displayed name of this palette. This is the name visible in the user interface. |
| htmlFileURL | string | Specifies the URL to the HTML file that will be displayed in the palette. This can be a local file or on the web. |
| isVisible | boolean | Specifies if the palette is initially visible or not. It's useful to create it invisibly, change other desired properties and then use the isVisible property to finally make it visible to the user. |
| showCloseButton | boolean | Specifies if a "Close" button should be displayed on the palette to allow the user to easily close it. |
| isResizable | boolean | Specifies if the palette can be resized by the user or not. |
| width | integer | Specifies the width of the palette in pixels. If no width is specified a default width will be used. This is an optional argument whose default value is 200. |
| height | integer | Specifies the height of the palette in pixels. If no height is specified a default height will be used. This is an optional argument whose default value is 200. |
| useNewWebBrowser | boolean | Specifies if you want to use the old or new web browser. A palette is essentially a dialog that hosts a web browser. To support this type of functionality, Fusion has used CEF (Chromium Embedded Framework). Fusion is in the process of switching to the Qt Web Browser wherever an embedded browser is needed in the product. As this transition occurs, Fusion is supporting both web browsers. This argument is optional and defaults to False, which means the palette will behave as before and use the CEF browser. Setting the argument to True will cause the palette to use the new QT Web Browser. When Fusion completes the transition to the QT Web Browser, support for the CEF browser will be removed from Fusion, and you will always get a QT Web Browser regardless of how the argument is set. Because of this, it is highly recommended you set this argument to true to use the new browser because when support for the CEF browser is removed you will automatically be forced to use the QT Web Browser. This argument is no longer used because the new QT Web Browser is always used regardless of this parameter's value. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
| --- | --- |
| [Palette Sample](PaletteSample_Sample.md) | Demonstrates how to create a palette, how to dock and snap palettes and how Fusion communicates with the palette HTML. The sample is an add-in. To use it, create a new Python add-in and replace the code with the code below. You also need to create an html file using the name and code below. The html file needs to be in the same folder as the py file. When you load the add-in, you'll see two new commands under the ADD-INS panel of the TOOLS tab. The "Show Custom Palette" command will cause the custom palette to be displayed. It will remain displayed until you click its Close button. Clicking the "Click to send info to Fusion" button on the palette, will send information to your add-in, which uses the API to display that information in a message box. Running the "Send Info to HTML" command to send data to the javascript running in the palette, which uses it to update the content of a paragraph. palette.html      Click the button below to send data to Fusion. Click to send info to Fusion Run the "Send Info to HTML" command in the ADD-INS panel to update this text.      function sendInfoToFusion(){ var today = new Date(); var dd = String(today.getDate()).padStart(2, '0'); var mm = String(today.getMonth() + 1).padStart(2, '0'); var yyyy = today.getFullYear(); var hours = String(today.getHours()).padStart(2, '0'); var minutes = String(today.getMinutes()).padStart(2, '0'); var seconds = String(today.getSeconds()).padStart(2, '0'); var date = dd + '/' + mm + '/' + yyyy; var time = hours + ':' + minutes + ':' + seconds; var args = { arg1 : "Sample argument 1", arg2 : "Sample argument 2" }; adsk.fusionSendData('send', JSON.stringify(args)); } window.fusionJavaScriptHandler = {handle: function(action, data){ try { if (action == 'send') { // Update a paragraph with the data passed in. document.getElementById('p1').innerHTML = data; } else if (action == 'debugger') { debugger; } else { return 'Unexpected command type: ' + action; } } catch (e) { console.log(e); console.log('exception caught with command: ' + action + ', data: ' + data); } return 'OK'; }};   |

## Version

Introduced in version March 2017  

