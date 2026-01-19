# WorkingModel.findEntityByToken Method

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Returns the entities associated with the provided token. The return is an array of entities. In most cases an array containing a single entity will be returned but there are cases where more than one entity can be returned. An example of this is where a token is obtained from a face and subsequent modeling operations cause the face to be split into two or more pieces. All of the faces that represent the original face will be returned with the first face being the most logical match to the original face.

## Syntax

"workingModel_var" is a variable referencing a [WorkingModel](WorkingModel.md) object.

```python
returnValue = workingModel_var.findEntityByToken(entityToken)
```

## Return Value

| Type | Description |
|----|----|
| [Base](Base.md)\[\] | Returns an array of entities associated with the provided token, or an empty array in the case where there are no matches. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entityToken | string | The input entity token you want to find the matching entity for. |

## Version

Introduced in version January 2024  

