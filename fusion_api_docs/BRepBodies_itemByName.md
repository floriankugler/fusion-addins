# BRepBodies.itemByName Method

Parent Object: [BRepBodies](BRepBodies.md)  

## Description

Returns a specific body using the name of the body within the collection.

## Syntax

"bRepBodies_var" is a variable referencing a [BRepBodies](BRepBodies.md) object.

```python
returnValue = bRepBodies_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | The BRepBody or null if a body with the defined name is not found. |

## Parameters

| Name | Type   | Description                                              |
|------|--------|----------------------------------------------------------|
| name | string | The name of the body, as seen in the browser, to return. |

## Version

Introduced in version August 2014  

