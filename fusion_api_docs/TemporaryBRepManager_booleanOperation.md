# TemporaryBRepManager.booleanOperation Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Performs the specified Boolean operation between the two input bodies. The input bodies need not be solid but can be faces that are combined or trimmed.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.booleanOperation(targetBody, toolBody, booleanType)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if the operation was successful. If successful, the target body is modified as a result of the Boolean operation. Because of this the targetBody must always be a temporary BRepBody. The toolbody is not modified. This is analogous to a machining operation where you have the target that is being machined and the tool that removes material. |

## Parameters

| Name | Type | Description |
|----|----|----|
| targetBody | [BRepBody](BRepBody.md) | The target body that will be modified as a result of the Boolean operation. |
| toolBody | [BRepBody](BRepBody.md) | The tool body that will be used to operate on the target body. |
| booleanType | [BooleanTypes](BooleanTypes.md) | The type of Boolean operation to perform. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

