# ManufacturingModels.syncAllManufacturingModels Method

Parent Object: [ManufacturingModels](ManufacturingModels.md)  

## Description

Checks wether changes to the original design have been made. If so, all manufacturing models are synchronized with their sources.

## Syntax

"manufacturingModels_var" is a variable referencing a [ManufacturingModels](ManufacturingModels.md) object.

```python
returnValue = manufacturingModels_var.syncAllManufacturingModels()
```

## Return Value

| Type    | Description                                               |
|---------|-----------------------------------------------------------|
| boolean | Returns true if any manufacturing model needed an update. |

## Version

Introduced in version March 2024  

