# HttpRequest.hasHeader Method

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Gets if the request has a header with the given name. This is useful to distinguish between the case where a header is not set and the case where a header is set to an empty string.

## Syntax

"httpRequest_var" is a variable referencing a [HttpRequest](HttpRequest.md) object.

```python
returnValue = httpRequest_var.hasHeader(name)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if a header with this name was set in the response. |

## Parameters

| Name | Type   | Description                              |
|------|--------|------------------------------------------|
| name | string | The case insensitive name of the header. |

## Version

Introduced in version January 2024  

