# Setup.additiveContainerByType Method

Parent Object: [Setup](Setup.md)  

## Description

Returns the additive container with the specified type.

## Syntax

"setup_var" is a variable referencing a [Setup](Setup.md) object.

```python
returnValue = setup_var.additiveContainerByType(containerType)
```

## Return Value

| Type | Description |
|----|----|
| [CAMAdditiveContainer](CAMAdditiveContainer.md) | Returns the specified container or null in the case where there is no container with the specified type. |

## Parameters

| Name | Type | Description |
|----|----|----|
| containerType | [CAMAdditiveContainerTypes](CAMAdditiveContainerTypes.md) | The type of the container |

## Version

Introduced in version July 2024  

