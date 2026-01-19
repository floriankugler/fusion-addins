# ManufacturingModel.deleteMe Method

Parent Object: [ManufacturingModel](ManufacturingModel.md)  

## Description

Deletes this ManufacturingModel. If this is part of a setup, the reference to this will be lost. The deletion makes that reference invalid.

## Syntax

"manufacturingModel_var" is a variable referencing a [ManufacturingModel](ManufacturingModel.md) object.

```python
returnValue = manufacturingModel_var.deleteMe()
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns true if the delete is successful. |

## Version

Introduced in version April 2023  

