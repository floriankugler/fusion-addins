# Viewport.setCurrentAsHome Method

Parent Object: [Viewport](Viewport.md)  

## Description

Sets the "home" view to be the current view orientation.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
returnValue = viewport_var.setCurrentAsHome(isFitToView)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if setting the view orientation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isFitToView | boolean | Specifies if when the view goes "home" if the view should be fit to the model or not. True indicates the view will be fit to the model. |

## Version

Introduced in version September 2022  

