# ListItem.deleteMe Method

Parent Object: [ListItem](ListItem.md)  

## Description

Deletes this item from the list. In cases where there is the concept of active item in the list, like with a DropDownCommandInput, this method will fail if the item you're attempting to delete is currently active. You need to make another item active first, and then you can delete the item.

## Syntax

"listItem_var" is a variable referencing a [ListItem](ListItem.md) object.

```python
returnValue = listItem_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version January 2015  

