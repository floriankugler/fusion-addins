# WebRequestEventArgs.isCanceled Property

Parent Object: [WebRequestEventArgs](WebRequestEventArgs.md)  

## Description

Used during the insertingFromURL and openingFromURL events to get or set if the insert or open should be allowed to continue. This defaults to false, which will allow the operation to continue as normal. This property should be ignored for all events besides the insertingFromURL and openingFromURL events.

## Syntax

"webRequestEventArgs_var" is a variable referencing a WebRequestEventArgs object.  

```python
# Get the value of the property.
propertyValue = webRequestEventArgs_var.isCanceled

# Set the value of the property.
webRequestEventArgs_var.isCanceled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2016  

