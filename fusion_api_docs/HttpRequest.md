# HttpRequest Object

Derived from: [Base](Base.md) Object  

## Description

Supports the ability to make HTTP requests.

## Methods

| Name | Description |
|----|----|
| [classType](HttpRequest_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](HttpRequest_create.md) | Creates a new HttpRequest object. |
| [execute](HttpRequest_execute.md) | Execute this request asynchronously. The response will be sent to the completed event. |
| [executeSync](HttpRequest_executeSync.md) | Execute this request synchronously. This will block the thread until the request completes. |
| [getHeader](HttpRequest_getHeader.md) | Gets the value of the specified header and returns the value. |
| [hasHeader](HttpRequest_hasHeader.md) | Gets if the request has a header with the given name. This is useful to distinguish between the case where a header is not set and the case where a header is set to an empty string. |
| [headers](HttpRequest_headers.md) | Get the request headers. |
| [removeHeader](HttpRequest_removeHeader.md) | Removes a header from the request. |
| [setHeader](HttpRequest_setHeader.md) | Sets a header for the request. |

## Properties

| Name | Description |
| --- | --- |
| [data](HttpRequest_data.md) | Gets and sets the body data to send with this request. |
| [isValid](HttpRequest_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [method](HttpRequest_method.md) | Gets and sets the method to use for the request. |
| [objectType](HttpRequest_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [url](HttpRequest_url.md) | Gets and sets the URL to make the request to. |

## Events

| Name | Description |
|----|----|
| [completed](HttpRequest_completed.md) | The completed event fires when the request has completed. This event will fire on successful or failure. |

## Accessed From

[HttpRequest.create](HttpRequest_create.md), [HttpResponse.request](HttpResponse_request.md)

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version January 2024  

