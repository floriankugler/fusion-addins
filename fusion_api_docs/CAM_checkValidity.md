# CAM.checkValidity Method

Parent Object: [CAM](CAM.md)  

## Description

Checks whether the models used by the operations have changed in the mean time and invalidates the affected operations if needed. Should be used for cases where the automatic detection does not work yet, for instance when design changes are expected before a Manufacture API call. Also recommended at the beginning of a script or the beginning of an event handler.

## Syntax

"cAM_var" is a variable referencing a [CAM](CAM.md) object.

```python
returnValue = cAM_var.checkValidity()
```

## Version

Introduced in version July 2023  

