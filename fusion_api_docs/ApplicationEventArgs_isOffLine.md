# ApplicationEventArgs.isOffLine Property

Parent Object: [ApplicationEventArgs](ApplicationEventArgs.md)  

## Description

Gets and sets if Fusion is offline or not.

## Syntax

"applicationEventArgs_var" is a variable referencing an ApplicationEventArgs object.  

```python
# Get the value of the property.
propertyValue = applicationEventArgs_var.isOffLine

# Set the value of the property.
applicationEventArgs_var.isOffLine = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Application Event API Sample](ApplicationEventSample_Sample.md) | Add-In that demonstrates application events. To use this sample, create a new folder using the name you want to use for the new add-in. Inside the folder, create a new file that is the same name as the folder but has a .py extension. Copy the code below into the .py file. Create another file that is the same name as the folder but has a .manifest extension and copy the JSON data below into that file. { "autodeskProduct": "Fusion360", "type": "addin", "author": "", "description": { "": "" }, "supportedOS": "windows\|mac", "editEnabled": true } Run the "Scripts and Add-Ins" command and click the green plus button near the top of the dialog. Browse to the location where you created the folder and select the folder. The add-in should now be displayed in the list of add-ins on the "Add-Ins" tab of the dialog. Select the add-in and click the "Run" button. This will load the add-in and when any of the application events occurr that it is watching for it will report them in the TEXT COMMAND window. |

## Version

Introduced in version January 2016  

