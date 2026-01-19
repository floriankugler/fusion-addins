# HttpRequest.getHeader Method

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Gets the value of the specified header and returns the value.

## Syntax

"httpRequest_var" is a variable referencing a [HttpRequest](HttpRequest.md) object.

```python
returnValue = httpRequest_var.getHeader(name)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the value of the header, or empty if the header was not found. You can use the hasHeader method to determine if the header exists before getting it. This is especially useful in the case where the header exists but has an empty string value. |

## Parameters

| Name | Type   | Description                              |
|------|--------|------------------------------------------|
| name | string | The case insensitive name of the header. |

## Version

Introduced in version January 2024  

