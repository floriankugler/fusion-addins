# ClearanceHoleInfo.redefine Method

Parent Object: [ClearanceHoleInfo](ClearanceHoleInfo.md)  

## Description

Method that redefines the values associated with an existing ClearanceHoleInfo object. This is done to modify an existing clearance hole. The ClearanceHoleInfo object defines the type, size, and fit of the clearance hole to create. Fusion uses this information to look up the full details of the clearance hole in tables delivered with Fusion. The ClearanceHoleDataQuery object can be used to determine valid input for this information.

## Syntax

"clearanceHoleInfo_var" is a variable referencing a [ClearanceHoleInfo](ClearanceHoleInfo.md) object.

```python
returnValue = clearanceHoleInfo_var.redefine(standard, fastenerType, size, fit)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if the redefinition was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| standard | string | Input string that specifies the standard. |
| fastenerType | string | Input string that specifies the fastener type. |
| size | string | Input string that specifies the fastener size. |
| fit | [ClearanceHoleFits](ClearanceHoleFits.md) | Input enum value that specifies the amount of clearance between the hole and the fastener. |

## Version

Introduced in version September 2025  

