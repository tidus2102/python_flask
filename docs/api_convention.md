API Design Guidelines
=====================

**Entities should be lower_case for words, and connected by "_"**:

*Acceptable*:

- paty
- friends
- user_profile

*Not Acceptable*

- Paty
- Friends
- userProfile

**Attributes should be lower_case for words, and connected by "_"**:

*Acceptable*:

- id
- title
- time
- address
- invited_friends

*Not Acceptable*

- ID
- Title
- Time
- Address
- Invited Friends


**String enumerations have a defined set of possible values. Must be treated as lowercase 
- Underscores instead of spaces**

*Acceptable*:

- will_go
- on_going
- at_paty

*Not Acceptable*:

- willgo
- onGoing
- AtPaty


Base URL
--------

**Development**: http://dev.upaty.vn/api/v1.0
**Production**: http://www.upaty.vn/api/v1.0


Authentication
--------------

**All endpoints need token based auth in HTTP header**

 	**X-Access-Token (required)**
	**X-Device-Id (required)**
	
Response convention
-------------------

**A success api with no result**

```
HTTP CODE RETURN: 200
{
}
```

**A success api with result**

```
HTTP CODE RETURN: 200
{
  data: [{
    my_field1: "some-value",
    my_field2: "another value"
  }]
}
```

**If there is error**

```
HTTP CODE RETURN: > 400
{
  errors: [{
    message: "An error string explained why this error is happening",
    code: "error_code" 
  }]
}
```

Error Code
----------

- invalid_request
- invalid_method
- authentication_error
- not_found
- validation_error


Request Param and Response Content
----------------------------------

- **Datetime**: "2014-01-01T12:34:00+0000"
- **Date**: "2014-01-01"
- **Field names in request and response body must be in underscore**
- **All textual data must be encoded in UTF-8**
- **API must use only JSON for request and response body for structure data**
- **For binary upload, API Caller (client) must send the binary data in request body or using multipart form data**


Use RESTFull standard (http://en.wikipedia.org/wiki/Representational_state_transfer)
-------------

**http://example.com/resources**

- GET : List the URIs and perhaps other details of the collection's members.
- PUT : Replace the entire collection with another collection.
- POST : Create a new entry in the collection. The new entry's URI is assigned automatically and is usually returned by the operation
- DELETE : Delete the entire collection.
 
**http://example.com/resources/item17**

- GET : Retrieve a representation of the addressed member of the collection, expressed in an appropriate Internet media type.
- PUT : Replace the addressed member of the collection, or if it doesn't exist, createit.
- POST : Not generally used. Treat the addressed member as a collection in its own right andcreate a new entry in it
- DELETE : Delete the addressed member of the collection.