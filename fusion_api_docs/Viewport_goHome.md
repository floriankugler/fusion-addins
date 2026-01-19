# Viewport.goHome Method

Parent Object: [Viewport](Viewport.md)  

## Description

Sets the camera of the viewport to the defined "home" position.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
# Uses no optional arguments.
returnValue = viewport_var.goHome()

# Uses optional arguments.
returnValue = viewport_var.goHome(transition)
```

## Return Value

| Type    | Description                                                  |
|---------|--------------------------------------------------------------|
| boolean | Returns true if setting the view orientation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| transition | boolean | If this is true it will do a smooth transition from the current camera position to the home position. If false, the view will jump to the home position with no intermediate steps. This is an optional argument whose default value is True. |

## Version

Introduced in version September 2022  

