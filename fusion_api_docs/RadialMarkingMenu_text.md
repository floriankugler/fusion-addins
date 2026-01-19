# RadialMarkingMenu.text Property

Parent Object: [RadialMarkingMenu](RadialMarkingMenu.md)  

## Description

Gets and sets the text that is displayed in the parent marking menu to access a sub marking menu. This property is not used for the main marking menu and will return an empty string and setting it will have no effect.

## Syntax

"radialMarkingMenu_var" is a variable referencing a RadialMarkingMenu object.  

```python
# Get the value of the property.
propertyValue = radialMarkingMenu_var.text

# Set the value of the property.
radialMarkingMenu_var.text = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Marking Menu API Sample](MarkingMenuSample_Sample.md) | Demonstrates how to customize marking menu and context menu. This sample is an add-in. To use it, create a new add-in using the "Scrips and Add-Ins" command. Use any name you would like for the add-in. In the folder where the add-in was created edit the *add-in name*.py file and replace it's entire contents with the sample code below. You can also delete all the other files that were created for the add-in except for *add-in name*.manifiest. Start the add-in from the "Scripts and Add-Ins" dialog. Now, with the add-in running, whenever you right-click in the Fusion window, you'll get an entirely customized context menu. The default marking menu has been modified by the add-in by removing the existing commands and adding some custom commands. |

## Version

Introduced in version January 2017  

