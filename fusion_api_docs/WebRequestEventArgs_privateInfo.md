# WebRequestEventArgs.privateInfo Property

Parent Object: [WebRequestEventArgs](WebRequestEventArgs.md)  

## Description

Returns the value specified as the "privateInfo" parameter in the URL. This will be decoded and can be an empty string if the "privateInfo" parameter was not specified in the URL.

## Syntax

"webRequestEventArgs_var" is a variable referencing a WebRequestEventArgs object.  

```python
# Get the value of the property.
propertyValue = webRequestEventArgs_var.privateInfo
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version May 2016  

