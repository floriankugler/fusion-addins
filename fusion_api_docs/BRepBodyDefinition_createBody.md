# BRepBodyDefinition.createBody Method

Parent Object: [BRepBodyDefinition](BRepBodyDefinition.md)  

## Description

Attempts to create a temporary BRepBody object using the definition provided by this BRepBodyDefinition object. Properties on this BRepBodyDefinition are used to define some of the criteria that control how the body is created.

## Syntax

"bRepBodyDefinition_var" is a variable referencing a [BRepBodyDefinition](BRepBodyDefinition.md) object.

```python
returnValue = bRepBodyDefinition_var.createBody()
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the newly created BRepBody object if successful, otherwise null is returned. Information about the body creation can be obtained by using the outcomeInfo property. The outcom info is especially useful when initially writing and debugging your code to understand why the creation of the body is failing. |

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

