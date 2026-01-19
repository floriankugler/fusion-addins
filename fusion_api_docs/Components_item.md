# Components.item Method

Parent Object: [Components](Components.md)  

## Description

Function that returns the specified component using an index into the collection.

## Syntax

"components_var" is a variable referencing a [Components](Components.md) object.

```python
returnValue = components_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [Component](Component.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Samples

| Name | Description |
| --- | --- |
| [Library Item API Sample](LibraryItemSample_Sample.md) | Demonstrates how to examine library items using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the existing default code. The script will search for and record all components and library items in the current project. They are displayed in a dialog when the script has finished. |

## Version

Introduced in version August 2014  

