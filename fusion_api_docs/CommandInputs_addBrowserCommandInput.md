# CommandInputs.addBrowserCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new command input to the command that behaves as a browser.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
# Uses no optional arguments.
returnValue = commandInputs_var.addBrowserCommandInput(id, name, htmlFileURL, minimumHeight)

# Uses optional arguments.
returnValue = commandInputs_var.addBrowserCommandInput(id, name, htmlFileURL, minimumHeight, maximumHeight)
```

## Return Value

| Type | Description |
|----|----|
| [BrowserCommandInput](BrowserCommandInput.md) | Returns the created BrowserCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| name | string | The displayed label of this input as seen in the dialog. If a name is not specified (an empty string), the input will be centered horizontally within it's row in the dialog. If a name is specified, the name will appear as a left justified label aligned with the other command input labels, and the left side of the input will be aligned with the other command inputs. |
| htmlFileURL | string | Specifies the URL to the HTML file that will be displayed in the tab. This can be a local file or on the web. |
| minimumHeight | integer | Defines the minimum height of the browser within the command dialog. As the user resizes the dialog, the area taken up by the browser will shrink and grow to fit within the defined space. It will never shrink to be less than the minimum height or expand to be larger than the maximum height. If the dialog can't fit the browser at the minimum size a scroll bar will appear for the dialog to allow the user to scroll to access all the inputs in the dialog. |
| maximumHeight | integer | An optional parameter that specifies the maximum height of the browser within the command dialog. As the user resizes the dialog, the area taken up by the browser will shrink and grow to fit within the defined space. It will never shrink to be less than the minimum height or expand to be larger than the maximum height. If the content displayed within the browser does not fit within the current area, a scroll bar will appear to allow the user to scroll to see the entire browser content. The default value of zero sets no maximum height, so the browser will expand to the maximum extent available. This is an optional argument whose default value is 0. |

## Version

Introduced in version July 2021  

