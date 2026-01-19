# UserInterface.selectEntity Method

Parent Object: [UserInterface](UserInterface.md)  

## Description

Supports the selection of a single entity. This provides a simple way to prompt the user for for a selection in a script. If you need more control over the selection a command should be created and a SelectionCommandInput used.

## Remarks

The selectEntity method is not supported within any of the Command related events.

## Syntax

"userInterface_var" is a variable referencing a [UserInterface](UserInterface.md) object.

```python
returnValue = userInterface_var.selectEntity(prompt, filter)
```

## Return Value

| Type | Description |
|----|----|
| [Selection](Selection.md) | Returns a Selection object that provides access the selected entity through it's "entity" property along with the location in space where the entity was selected. Asserts if the selection is aborted. |

## Parameters

| Name | Type | Description |
|----|----|----|
| prompt | string | The prompt displayed to the user during the selection. |
| filter | string | A string defining the types of entities valid for selection. The valid list of selection filters can be found here: [Selection Filters](SelectionFilters_UM.md). You can combine multiple types by using a comma delimiter. For example, the string "PlanarFaces,ConstructionPlanes" will allow the selection of either a planar face or a construction plane. |

## Version

Introduced in version August 2014  

