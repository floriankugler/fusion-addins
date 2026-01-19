# URL.join Method

Parent Object: [URL](URL.md)  

## Description

Join this URL with the given path and return the resulting URL. The operation does not alter the current URL. Join inserts a slash '/' to properly extend the path, so that "http://foo".join("bar") will return "http://foo/bar", not "http://foobar".

## Syntax

"uRL_var" is a variable referencing a [URL](URL.md) object.

```python
returnValue = uRL_var.join(path)
```

## Return Value

| Type           | Description             |
|----------------|-------------------------|
| [URL](URL.md) | Returns the joined URL. |

## Parameters

| Name | Type   | Description                   |
|------|--------|-------------------------------|
| path | string | The path to join to this URL. |

## Version

Introduced in version April 2023  

