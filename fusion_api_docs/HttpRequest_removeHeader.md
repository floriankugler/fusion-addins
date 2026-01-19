# HttpRequest.removeHeader Method

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Removes a header from the request.

## Syntax

"httpRequest_var" is a variable referencing a [HttpRequest](HttpRequest.md) object.

```python
returnValue = httpRequest_var.removeHeader(name)
```

## Return Value

| Type    | Description                                       |
|---------|---------------------------------------------------|
| boolean | Returns true if the header was found and removed. |

## Parameters

| Name | Type   | Description                              |
|------|--------|------------------------------------------|
| name | string | The case insensitive name of the header. |

## Version

Introduced in version January 2024  

