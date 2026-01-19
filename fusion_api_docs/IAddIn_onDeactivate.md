# IAddIn.onDeactivate Method

Parent Object: [IAddIn](IAddIn.md)  

## Description

Lets the application do any termination when it is safe to do so. In general, if the add-in is closing, termination should be minimized.

## Syntax

"iAddIn_var" is a variable referencing an [IAddIn](IAddIn.md) object.

```python
returnValue = iAddIn_var.onDeactivate(isAppClosing)
```

## Parameters

| Name         | Type    | Description |
|--------------|---------|-------------|
| isAppClosing | boolean |             |

## Version

Introduced in version March 2022  

