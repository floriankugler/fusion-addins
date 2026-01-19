# DropDownCommandInput.selectedItem Property

Parent Object: [DropDownCommandInput](DropDownCommandInput.md)  

## Description

Gets the item in the list that is currently selected. This can return null in the case where no item in the list has been selected. This should be ignored for CheckBoxDropDownStyle style drop-downs because multiple items can be selected and each LiteItem should be checked individually.

## Syntax

"dropDownCommandInput_var" is a variable referencing a DropDownCommandInput object.  

```python
# Get the value of the property.
propertyValue = dropDownCommandInput_var.selectedItem
```

## Property Value

This is a read only property whose value is a [ListItem](ListItem.md).

## Version

Introduced in version January 2015  

