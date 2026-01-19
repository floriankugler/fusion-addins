# HttpResponse.hasHeader Method

Parent Object: [HttpResponse](HttpResponse.md)  

## Description

Gets if the response has a header with the given name. This is useful to distinguish between the case where a header is not set and the case where a header is set to an empty string.

## Syntax

"httpResponse_var" is a variable referencing a [HttpResponse](HttpResponse.md) object.

```python
returnValue = httpResponse_var.hasHeader(name)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | True if a header with this name was set in the response. |

## Parameters

| Name | Type   | Description                              |
|------|--------|------------------------------------------|
| name | string | The case insensitive name of the header. |

## Version

Introduced in version January 2024  

