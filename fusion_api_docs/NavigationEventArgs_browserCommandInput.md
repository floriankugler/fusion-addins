# NavigationEventArgs.browserCommandInput Property

Parent Object: [NavigationEventArgs](NavigationEventArgs.md)  

## Description

When the event is fired from a BrowserCommandInput object, this property returns the specific BrowserCommandInput that caused the event to fire. In all other cases this property returns null.

## Syntax

"navigationEventArgs_var" is a variable referencing a NavigationEventArgs object.  

```python
# Get the value of the property.
propertyValue = navigationEventArgs_var.browserCommandInput
```

## Property Value

This is a read only property whose value is a [BrowserCommandInput](BrowserCommandInput.md).

## Version

Introduced in version July 2021  

