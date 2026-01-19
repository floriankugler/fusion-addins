# NamedViews.itemByName Method

Parent Object: [NamedViews](NamedViews.md)  

## Description

Returns the specified named view using the name of the named view. The four standard named views ("TOP", "FRONT", "RIGHT", and "HOME") are not accessible through this method. For the predefined view use the properties on this collection that provide direct access to the specific named view.

## Syntax

"namedViews_var" is a variable referencing a [NamedViews](NamedViews.md) object.

```python
returnValue = namedViews_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [NamedView](NamedView.md) | Returns null if the specified name was not found. |

## Parameters

| Name | Type   | Description                                                 |
|------|--------|-------------------------------------------------------------|
| name | string | The name of the named view within the collection to return. |

## Version

Introduced in version September 2023  

