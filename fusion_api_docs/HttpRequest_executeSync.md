# HttpRequest.executeSync Method

Parent Object: [HttpRequest](HttpRequest.md)  

## Description

Execute this request synchronously. This will block the thread until the request completes.

## Syntax

"httpRequest_var" is a variable referencing a [HttpRequest](HttpRequest.md) object.

```python
returnValue = httpRequest_var.executeSync()
```

## Return Value

| Type | Description |
|----|----|
| [HttpResponse](HttpResponse.md) | Returns the response from making this request, or null if an error prevents the request from starting. |

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version January 2024  

