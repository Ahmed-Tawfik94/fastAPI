all the data validation is performed under the hood by Pydantic
by using type declaration as `str` `float` `bool` and many other complex data types

### order matters

if situation accured and need paths as
* users/me
* users/{user_id}
because paths are evaluated