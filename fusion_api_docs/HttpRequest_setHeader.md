# HttpRequest.setHeader Method

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Sets a header for the request.

## Syntax

"httpRequest_var" is a variable referencing a [HttpRequest](HttpRequest.md) object.

```python
returnValue = httpRequest_var.setHeader(name, value)
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if setting the header succeeds. |

## Parameters

| Name  | Type   | Description                   |
|-------|--------|-------------------------------|
| name  | string | The name of the header value. |
| value | string | The header's value.           |

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version January 2024  

