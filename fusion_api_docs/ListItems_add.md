# ListItems.add Method

Parent Object: [ListItems](ListItems.md)  

## Description

Adds a new item to the list.

## Syntax

"listItems_var" is a variable referencing a [ListItems](ListItems.md) object.

```python
# Uses no optional arguments.
returnValue = listItems_var.add(name, isSelected)

# Uses optional arguments.
returnValue = listItems_var.add(name, isSelected, icon, beforeIndex)
```

## Return Value

| Type | Description |
|----|----|
| [ListItem](ListItem.md) | Returns the new ListControlItem or null in the case of a failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| name | string | The name of this item as it is displayed in the list. |
| isSelected | boolean | Sets whether this item is selected or not. If this list is associated with a control or input that can only have one item selected any other selected items will be unselected and this one will be the only selected item. |
| icon | string | The path to the folder containing the image files to use for the icon. This is an optional argument but is required in the case of ButtonRowCommandInput objects. It is optional in the case of a DropDownCommandInput whose style is LabeledIconDropDownStyle and for ListControlType whose type is not RadioButtonListType. In other cases it is not used and is ignored. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). This is an optional argument whose default value is "". |
| beforeIndex | integer | The position of the item within the list. This value indicates the index of the current item to insert this new item just before. For example, a value of 0 will insert it before the first item in the list. An index of -1 will position the button at the bottom of the list. This is an optional argument whose default value is -1. |

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2015  

