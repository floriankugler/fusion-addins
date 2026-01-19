# ClearanceHoleInfo.create Method

Parent Object: [ClearanceHoleInfo](ClearanceHoleInfo.md)  

## Description

Method that creates a new ClearanceHoleInfo object to use in creating clearance holes. The ClearanceHoleInfo object defines the type, size, and fit of the clearance hole to create. Fusion uses this information to look up the full details of the clearance hole in tables delivered with Fusion. The ClearanceHoleDataQuery object can be used to determine valid input for this information. It's statically created using the ClearanceHoleDataQuery.create method.

## Syntax

This is a static method.  

```python

returnValue = adsk.fusion.ClearanceHoleInfo.create(standard, fastenerType, size, fit)
```

## Return Value

| Type | Description |
|----|----|
| [ClearanceHoleInfo](ClearanceHoleInfo.md) | Returns the newly created ClearanceHoleInfo object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| standard | string | Input string that specifies the standard. |
| fastenerType | string | Input string that specifies the fastener type. |
| size | string | Input string that specifies the fastener size. |
| fit | [ClearanceHoleFits](ClearanceHoleFits.md) | Input enum value that specifies the fit of the fastener within the hole. |

## Version

Introduced in version September 2025  

