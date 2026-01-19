# CommandDefinitions.addListDefinition Method

Parent Object: [CommandDefinitions](CommandDefinitions.md)  

## Description

Creates a new command definition that can be used to create a list of check boxes, radio buttons, or text with an icon within a pop-up.  

When the list is of check boxes any combinations of items in the list can be checked. The drop-down also remains displayed allowing the user to check and uncheck multiple items however a CommandCreated event is fired for every change.  

When the list is of radio buttons or a list of text items, only one item in the list can be selected at a time. When an item is selected the drop-down is immediately dismissed.  

The items in the list and their initial state are defined using functionality on the associated ListControlDefinition, which is accessible through the returned CommandDefinition.

## Syntax

"commandDefinitions_var" is a variable referencing a [CommandDefinitions](CommandDefinitions.md) object.

```python
# Uses no optional arguments.
returnValue = commandDefinitions_var.addListDefinition(id, name, listControlDisplayType)

# Uses optional arguments.
returnValue = commandDefinitions_var.addListDefinition(id, name, listControlDisplayType, resourceFolder)
```

## Return Value

| Type | Description |
|----|----|
| [CommandDefinition](CommandDefinition.md) | Returns the created CommandDefinition object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The unique identifier for this command definition. It must be unique with respect to all other command definitions and is limited to the following set of characters, [A-Z][a-z][0-9] and _. |
| name | string | The name displayed in the UI for the associated selected check box list control. |
| listControlDisplayType | [ListControlDisplayTypes](ListControlDisplayTypes.md) | Specifies the type of controls to be displayed within the list. |
| resourceFolder | string | This argument defines the resource folder that contains the images used as the icon for items in the list. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). This is an optional argument whose default value is "". |

## Version

Introduced in version August 2014  

