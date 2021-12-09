# ***automate-s2p***

## ***API Documentation***

> ### **GET** addresses corresponding to entity_id

<!-- * HTTP Method - **GET** -->

* Endpoint - **`/entity_addresses/{entity_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
      Content: `{ error : "entity doesn't exist" }`
  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
```  

Sample Response:

```json
[
    {
        "address_id": 1,
        "address_nickname": "Berkeley Office",
        "country": "USA",
        "address": "215 Dwight Way, Berkeley, CA 97074",
        "is_billing_address": true,
        "is_shipping_address": true
    },
    {
        "address_id": 2,
        "address_nickname": "New York Headquarters",
        "country": "USA",
        "address": "156 Street Way, New York, NY 67809",
        "is_billing_address": true,
        "is_shipping_address": false
    }
]
```
> ### **GET** all event_info with event_id

<!-- * HTTP Method - **GET** -->

* Endpoint - **`/event_info/{event_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
      Content: `{ error : "event doesn't exist" }`
  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
```  

Sample Response:

```json
{
    "event_id" : 1,
    "event_name": "IT Solutions",
    "event_type": "RFQ",
    "event_end_date": "2021-08-11",
    "event_end_time": "16:30 pm IST",
    "created_by_name": "Matt",
    "event_billing_address_id": "1",
    "event_billing_address_nickname": "Berkeley Office",
    "event_billing_address": "215 Dwight Way, Berkeley, CA 97074",
    "event_billing_address_country": "USA",
    "event_delivery_address_id": "3",
    "event_delivery_address_nickname": "Wisconsin Factory",
    "event_delivery_address": "8140 County Rd, Colfax, WI 54730",
    "event_delivery_address_country": "USA",
    "event_delivery_date": "2021-08-11",
    "payment_terms": "90 Days",
    "status": "draft"
}
```
> ### **POST** of event_info

<!-- * HTTP Method - **POST** -->

* Endpoint - **`/event_info/{entity_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `400`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
{
    "event_name": "IT Solutions",
    "event_type": "RFQ",
    "event_end_date": "2021-08-11",
    "event_end_time": "16:30 pm IST",
    "created_by_name": "Matt",
    "event_billing_address_id": "1",
    "event_billing_address_nickname": "Berkeley Office",
    "event_billing_address": "215 Dwight Way, Berkeley, CA 97074",
    "event_billing_address_country": "USA",
    "event_delivery_address_id": "3",
    "event_delivery_address_nickname": "Wisconsin Factory",
    "event_delivery_address": "8140 County Rd, Colfax, WI 54730",
    "event_delivery_address_country": "USA",
    "event_delivery_date": "2021-08-11",
    "payment_terms": "90 Days",
    "status": "draft"
}
```  

Sample Response:

```json

```
> ### **POST** of event_info

<!-- * HTTP Method - **POST** -->

* Endpoint - **`/event_info/{entity_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `400`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
{
    "event_name": "IT Solutions",
    "event_type": "RFQ",
    "event_end_date": "2021-08-1",
    "event_end_time": "16:00 pm IST",
    "created_by_name": "Matt",
    "event_billing_address_id": "1",
    "event_billing_address_nickname": "Berkeley Office",
    "event_billing_address": "215 Dwight Way, Berkeley, CA 97074",
    "event_billing_address_country": "USA",
    "event_delivery_address_id": "3",
    "event_delivery_address_nickname": "Wisconsin Factory",
    "event_delivery_address": "8140 County Rd, Colfax, WI 54730",
    "event_delivery_address_country": "USA",
    "event_delivery_date": "2021-08-11",
    "payment_terms": "45 Days",
    "status": "draft"
}
```  

Sample Response:

```json

```

> ### **GET** list of all currency code

<!-- * HTTP Method - **GET** -->

* Endpoint - **`/currency_codes`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
```  

Sample Response:

```json
[{
        "code": "USD"
    },
    {
        "code": "INR"
    }
]
```
> ### **POST** currency code in currency_code

<!-- * HTTP Method - **POST** -->

* Endpoint - **`/currency_codes`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `400`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
[{
        "code": "USD"
    },
    {
        "code": "INR"
    }
]
```  

Sample Response:

```json

```
> ### **DELETE** of event_info

<!-- * HTTP Method - **POST** -->

* Endpoint - **`/currency_codes/{pk}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `400`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json

```  

Sample Response:

```json

```
> ### **GET** list of all measurement units from item_measurement_units

<!-- * HTTP Method - **GET** -->

* Endpoint - **`/measurement_unit/{item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
```  

Sample Response:

```json
[{
        "measurement_unit_id" : 1,
        "measurement_unit_primary_name" : "meter",
        "measurement_unit_category" : "length",
        "measurement_unit_value_type" : "dec"
    },
    {
        "measurement_unit_id" : 2,
        "measurement_unit_primary_name" : "cm",
        "measurement_unit_category" : "length",
        "measurement_unit_value_type" : "dec"
    }
]
```
> ### **POST** measurement units in item_measurement_units

<!-- * HTTP Method - **POST** -->

* Endpoint - **`/measurement_unit`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `400`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json
[{
        "measurement_unit_primary_name" : "meter",
        "measurement_unit_category" : "length",
        "measurement_unit_value_type" : "dec"
    },
    {
        "measurement_unit_primary_name" : "cm",
        "measurement_unit_category" : "length",
        "measurement_unit_value_type" : "dec"
    }
]
```  

Sample Response:

```json

```
> ### **DELETE** of event_info

<!-- * HTTP Method - **POST** -->

* Endpoint - **`/measurement_unit/{item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `400`  

  * **Code** - `401`  
      Content: `{ error : "You are unauthorized to make this request." }`

Example Request:

```json

```  

Sample Response:

```json

```
