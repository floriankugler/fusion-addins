# HttpRequest.headers Method

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Get the request headers.

## Syntax

"httpRequest_var" is a variable referencing a [HttpRequest](HttpRequest.md) object.  

```python
(returnValue, names, values) = httpRequest_var.headers()
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

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version January 2024  

