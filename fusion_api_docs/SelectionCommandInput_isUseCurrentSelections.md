# SelectionCommandInput.isUseCurrentSelections Property

Parent Object: [SelectionCommandInput](SelectionCommandInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Determines if any selections the user has made before starting the command can be used by the command's selection inputs. The default is true, which means the active selections will be added to the first selection input whose selection filter allows for that entity type. For example, if you have two selection inputs that have filters to select any number of faces and there are four faces selected when the command is started, those four faces will be selected by the selection input. If there's another selection input for the same command that has the filter set to select sketch curves, and there are faces and sketch curves selected when you start the command, the faces will be selected by the selection input filtering for faces, and the sketch curves will be selected by the selection input filtering for sketch curves.  

You can programmatically control which selected entities will be added to the selection inputs by using the preSelect event of the command. The preSelect event will fire for each entity that was already selected before it's added to the selection input, and you can use it to control if it will be added to the selection input.

## Syntax

"selectionCommandInput_var" is a variable referencing a SelectionCommandInput object.  

```python
# Get the value of the property.
propertyValue = selectionCommandInput_var.isUseCurrentSelections

# Set the value of the property.
selectionCommandInput_var.isUseCurrentSelections = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2024  

