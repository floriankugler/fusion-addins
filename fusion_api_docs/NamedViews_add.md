# NamedViews.add Method

Parent Object: [NamedViews](NamedViews.md)  

## Description

Creates a new named view.

## Syntax

"namedViews_var" is a variable referencing a [NamedViews](NamedViews.md) object.

```python
# Uses no optional arguments.
returnValue = namedViews_var.add(camera)

# Uses optional arguments.
returnValue = namedViews_var.add(camera, name)
```

## Return Value

| Type | Description |
|----|----|
| [NamedView](NamedView.md) | Returns the newly created NamedView object or fails if invalid input was provided. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| camera | [Camera](Camera.md) | The camera that defines the view. To create a named view for the active viewport you can get a camera from the active viewport and provide it as input to this method. |
| name | string | The name of the named view. This must be unique with respect to other named views in the product. This is optional and if not provided a default unique name will be generated. This is an optional argument whose default value is "". |

## Version

Introduced in version September 2023  

