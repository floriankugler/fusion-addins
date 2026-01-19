# RadialMarkingMenu.create Method

Parent Object: [RadialMarkingMenu](RadialMarkingMenu.md)  

## Description

This is used to create a sub-menu in a marking menu. This method creates a new, empty marking menu which can then be assigned to a position in the displayed marking menu to define the sub-menu.

## Syntax

"radialMarkingMenu_var" is a variable referencing a [RadialMarkingMenu](RadialMarkingMenu.md) object.

```python
returnValue = radialMarkingMenu_var.create(text)
```

## Return Value

| Type | Description |
|----|----|
| [RadialMarkingMenu](RadialMarkingMenu.md) | Returns the newly created marking menu or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| text | string | The text that will be displayed in the parent menu to access this menu. |

## Samples

| Name | Description |
|----|----|
| [Marking Menu API Sample](MarkingMenuSample_Sample.md) | Demonstrates how to customize marking menu and context menu. This sample is an add-in. To use it, create a new add-in using the "Scrips and Add-Ins" command. Use any name you would like for the add-in. In the folder where the add-in was created edit the *add-in name*.py file and replace it's entire contents with the sample code below. You can also delete all the other files that were created for the add-in except for *add-in name*.manifiest. Start the add-in from the "Scripts and Add-Ins" dialog. Now, with the add-in running, whenever you right-click in the Fusion window, you'll get an entirely customized context menu. The default marking menu has been modified by the add-in by removing the existing commands and adding some custom commands. |

## Version

Introduced in version January 2017  

