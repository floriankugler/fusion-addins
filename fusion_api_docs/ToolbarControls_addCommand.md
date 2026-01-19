# ToolbarControls.addCommand Method

Parent Object: [ToolbarControls](ToolbarControls.md)  

## Description

Adds a button to the controls in the toolbar, panel, or drop-down. The ID of the created command control is inherited from the associated command definition.

## Syntax

"toolbarControls_var" is a variable referencing a [ToolbarControls](ToolbarControls.md) object.

```python
# Uses no optional arguments.
returnValue = toolbarControls_var.addCommand(commandDefinition)

# Uses optional arguments.
returnValue = toolbarControls_var.addCommand(commandDefinition, positionID, isBefore)
```

## Return Value

| Type | Description |
|----|----|
| [CommandControl](CommandControl.md) | Returns the newly created CommandControl object or null if the creation fails. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| commandDefinition | [CommandDefinition](CommandDefinition.md) | The associated CommandDefinition that defines the resources and receives events related to this control. |
| positionID | string | Specifies the reference id of the control to position this control relative to. Not setting this value indicates that the control will be created at the end of all other controls in toolbar. The isBefore parameter specifies whether to place the control before or after the reference control. This is an optional argument whose default value is "". |
| isBefore | boolean | Specifies whether to place the control before or after the reference control specified by the positionID parameter. This argument is ignored is positionID is not specified. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
| --- | --- |
| [Palette Sample](PaletteSample_Sample.md) | Demonstrates how to create a palette, how to dock and snap palettes and how Fusion communicates with the palette HTML. The sample is an add-in. To use it, create a new Python add-in and replace the code with the code below. You also need to create an html file using the name and code below. The html file needs to be in the same folder as the py file. When you load the add-in, you'll see two new commands under the ADD-INS panel of the TOOLS tab. The "Show Custom Palette" command will cause the custom palette to be displayed. It will remain displayed until you click its Close button. Clicking the "Click to send info to Fusion" button on the palette, will send information to your add-in, which uses the API to display that information in a message box. Running the "Send Info to HTML" command to send data to the javascript running in the palette, which uses it to update the content of a paragraph. palette.html      Click the button below to send data to Fusion. Click to send info to Fusion Run the "Send Info to HTML" command in the ADD-INS panel to update this text.      function sendInfoToFusion(){ var today = new Date(); var dd = String(today.getDate()).padStart(2, '0'); var mm = String(today.getMonth() + 1).padStart(2, '0'); var yyyy = today.getFullYear(); var hours = String(today.getHours()).padStart(2, '0'); var minutes = String(today.getMinutes()).padStart(2, '0'); var seconds = String(today.getSeconds()).padStart(2, '0'); var date = dd + '/' + mm + '/' + yyyy; var time = hours + ':' + minutes + ':' + seconds; var args = { arg1 : "Sample argument 1", arg2 : "Sample argument 2" }; adsk.fusionSendData('send', JSON.stringify(args)); } window.fusionJavaScriptHandler = {handle: function(action, data){ try { if (action == 'send') { // Update a paragraph with the data passed in. document.getElementById('p1').innerHTML = data; } else if (action == 'debugger') { debugger; } else { return 'Unexpected command type: ' + action; } } catch (e) { console.log(e); console.log('exception caught with command: ' + action + ', data: ' + data); } return 'OK'; }};   |
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2014  

