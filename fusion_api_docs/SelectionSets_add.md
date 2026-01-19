# SelectionSets.add Method

Parent Object: [SelectionSets](SelectionSets.md)  

## Description

Adds a new SelectionSet to the parent product.

## Syntax

"selectionSets_var" is a variable referencing a [SelectionSets](SelectionSets.md) object.

```python
# Uses no optional arguments.
returnValue = selectionSets_var.add(entities)

# Uses optional arguments.
returnValue = selectionSets_var.add(entities, name)
```

## Return Value

| Type | Description |
|----|----|
| [SelectionSet](SelectionSet.md) | Returns the created selection set or null in the case the selection set couldn't be created. This method can fail in the case where no entities are provided or if any of the provided entities are not selectable. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entities | Base[] | An array of entities that will be in the created selection set. All entities must be in the context of the root component. This means if the entity isn't directly owned by the root component, it must be a proxy. |
| name | string | The name of the selection set. This is an optional argument is if not specified, or an empty string is provided, Fusion will create a name for the selection set. If provided, the name should be unique with respect to other selection sets in the product. If a name is provided that is the same as an existing selection set, Fusion will append a counter to the name to make the name unique. This is an optional argument whose default value is "". |

## Version

Introduced in version May 2022  

