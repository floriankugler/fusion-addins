# HttpResponse.headers Method

Parent Object: [HttpResponse](HttpResponse.md)  

## Description

Get the response headers.

## Syntax

"httpResponse_var" is a variable referencing a [HttpResponse](HttpResponse.md) object.  

```python
(returnValue, names, values) = httpResponse_var.headers()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true on success or false on error. |

## Parameters

| Name   | Type       | Description                           |
|--------|------------|---------------------------------------|
| names  | string\[\] | An array of all the header key names. |
| values | string\[\] | An array of all the header values.    |

## Version

Introduced in version January 2024  

