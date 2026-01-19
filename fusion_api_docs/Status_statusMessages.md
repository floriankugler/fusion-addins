# Status.statusMessages Property

Parent Object: [Status](Status.md)  

## Description

the status messages associated with this status. These messages are displayed to the user in the alert dialog. Each status message can have children status messages that will be displayed as a tree structure in the alert dialog.

## Syntax

"status_var" is a variable referencing a Status object.  

```python
# Get the value of the property.
propertyValue = status_var.statusMessages
```

## Property Value

This is a read only property whose value is a [StatusMessages](StatusMessages.md).

## Version

Introduced in version July 2021  

