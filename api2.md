# API CONTRACTS

## SELLERS

> ### GET seller info from sellers with seller_id

* HTTP Method - **GET**

* Endpoint - **`/sellers/{seller_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
{
    "seller_name": "Apple Inc.",
    "seller_email": "xyz@gmail.com",
    "seller_address": "California"
}
```

> ### POST seller info to sellers

* HTTP Method - **POST**

* Endpoint - **`/sellers`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "seller_name": "Apple Inc.",
    "seller_email": "xyz@gmail.com",
    "seller_address": "California"
}
```  

Sample Response:

```json
{
    "seller_id": 1
}
```

> ### DELETE seller info from sellers with seller_id

* HTTP Method - **DELETE**

* Endpoint - **`/sellers/{seller_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
```

## SELLERS LIST

> ### GET list of seller objects from sellers

* HTTP Method - **GET**

* Endpoint - **`/sellers`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
[
    {
        "seller_id": 1,
        "seller_name": "Apple Inc.",
        "seller_email": "apple@gmail.com",
        "seller_address": "California"
    },
    {
        "seller_id": 2,
        "seller_name": "Microsoft",
        "seller_email": "microsoft@gmail.com",
        "seller_address": "California"
    }
]
```

## ITEM ATTRIBUTES

> ### GET list of attribute_id from item_attributes with item_id

* HTTP Method - **GET**

* Endpoint - **`/item_attributes/{item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
[1, 2, 4]
```

> ### POST attribute_id to item_attributes with item_id

* HTTP Method - **POST**

* Endpoint - **`/item_attributes/{item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`  

Example Request:

```json
1
```  

Sample Response:

```json
```

> ### DELETE attribute_id from item_attributes with item_id

* HTTP Method - **DELETE**

* Endpoint - **`/item_attributes/{item_id}/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
```

## ATTRIBUTES

> ### GET attribute_name and attribute_value_type from attribute_id

* HTTP Method - **GET**

* Endpoint - **`/attributes/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
    {
        "attribute_id": 1,
        "attribute_name": "color",
        "attribute_value_type": "enum_type",
    }
```

> ### POST attribute_name and attribute_value_type

* HTTP Method - **POST**

* Endpoint - **`/attributes`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "attribute_name": "color",
    "attribute_value_type": "enum_type",
}
```  

Sample Response:

```json
{
    "attribute_id": 1
}
```

> ### DELETE attribute from attributes with attrubute_id

* HTTP Method - **POST**

* Endpoint - **`/attributes/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
```

## ATTRIBUTE VALUE OPTIONS

> ### GET attribute_value_options from attribute_id

* HTTP Method - **GET**

* Endpoint - **`/attribute_value_options/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
    {
        "attribute_value": ["White", "Black"]
    }
```

> ### POST attribute_value_options for attribute_id

* HTTP Method - **POST**

* Endpoint - **`/attribute_value_options/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "attribute_value": "White"
}
```  

Sample Response:

```json
```

> ### DELETE attribute_value_options for attribute_id

* HTTP Method - **DELETE**

* Endpoint - **`/attribute_value_options/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "attribute_value": "White"
}
```  

Sample Response:

```json
```

## MEASUREMENT UNITS

> ### GET measurement unit object with measurement_unit_id

* HTTP Method - **GET**

* Endpoint - **`/measurement_units/{measurement_unit_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
{
    "measurement_unit_primary_name": "m",
    "measurement_unit_category": "Lenght",
    "measurement_unit_value_type": "numeric"
}
```

> ### POST measurement unit object

* HTTP Method - **POST**

* Endpoint - **`/measurement_units`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "measurement_unit_primary_name": "m",
    "measurement_unit_category": "Lenght",
    "measurement_unit_value_type": "numeric"
}
```  

Sample Response:

```json
{
    "measurement_unit_id": 1
}
```

> ### DELETE measurement unit object with measurement_unit_id

* HTTP Method - **DELETE**

* Endpoint - **`/measurement_units/{measurement_unit_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
```

## BUYER ITEMS

> ### GET buyer_item details with buyer_item_id and enterprise_id

* HTTP Method - **GET**

* Endpoint - **`/buyer_items/{enterprise_id}/{buyer_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
    {
        "item_id": 1534,
        "buyer_item_id": "10021",
        "enterprise_id": 1,
        "search_display_name": "Item 10021 - iPhone 12 - 256GB - Black"
    }
```

### POST buyer_item details with buyer_item_id and enterprise_id

* HTTP Method - **POST**

* Endpoint - **`/buyer_items/{enterprise_id}/{buyer_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
{
    "item_id": 1534,
    "buyer_item_id": "10021",
    "enterprise_id": 1,
    "buyer_item_name": "Item 10021 - iPhone 12 - 256GB - Black"
}
```  

Sample Response:

```json
{
    "buyer_items_id": 1
}
```

### DELETE buyer_item details with buyer_item_id and enterprise_id

* HTTP Method - **POST**

* Endpoint - **`/buyer_items/{enterprise_id}/{buyer_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
```

## BUYER ITEM ATTRIBUTE VALUES

> ### GET buyer_item_attribute_values with buyer_items_entry_id

* HTTP Method - **GET**

* Endpoint - **`/buyer_item_attribute_values/{buyer_items_entry_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
[
    {
        "attribute_id": 1,
        "attribute_value": "Black"
    },
    {
        "attribute_id": 2,
        "attribute_value": "Apple"
    }
]
```

> ### POST buyer_item_attribute_values with buyer_items_entry_id

* HTTP Method - **POST**

* Endpoint - **`/buyer_item_attribute_values/{buyer_items_entry_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
{
    "attribute_id": 1,
    "attribute_value": "Black"
}
```  

Sample Response:

```json
```

> ### DELETE buyer_item_attribute_values with buyer_items_entry_id and attribute_id

* HTTP Method - **DELETE**

* Endpoint - **`/buyer_item_attribute_values/{buyer_items_entry_id}/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
```

## ENTITY ADDRESSES

> ### GET entity addresses

* HTTP Method - **GET**

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

> ### GET list of buyer_items with respect to keyword

* HTTP Method - **GET**

* Endpoint - **`/buyer_items/{keyword}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
[
    {
        "item_id": 1534,
        "buyer_item_id": "10021",
        "enterprise_id": 1,
        "search_display_name": "Item 10021 - iPhone 12 - 256GB - Black"
    },
    {
        "item_id": 1534,
        "buyer_item_id": "10022",
        "enterprise_id": 1,
        "search_display_name": "Item 10022 - iPhone 12 - 256GB - White"
    }
]
```

## EVENT ITEMS

> ### GET event_item with event_line_item_id

* HTTP Method - **GET**

* Endpoint - **`/event_items/{event_id}/{event_line_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
{
    "item_id": "1",
    "item_name": "iPhone 12",
    "desired_quantity": "500",
    "measurement_unit": "units",
    "attributes": {
        "color": "Black",
        "manufacturer": "Apple"
    },
    "desired_price": "995",
    "currency_code": "USD",
    "delivery_date": "2021-07-11",
}
```

> ### POST event item details in event items

* HTTP Method - **POST**

* Endpoint - **`/event_items/{event_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `405`
  * **Code** - `409`  

Example Request:

```json
```  

Sample Response:

```json
{
    "item_id": "1",
    "item_name": "iPhone 12",
    "desired_quantity": "500",
    "measurement_unit": "units",
    "attributes": {
        "color": "Black",
        "manufacturer": "Apple"
    },
    "desired_price": "995",
    "currency_code": "USD",
    "delivery_date": "2021-07-11",
}
```

> ### PATCH event_item with event_id

* HTTP Method - **PATCH**

* Endpoint - **`/event_items/{event_id}/{event_line_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
{
    "item_id": "1",
    "item_name": "iPhone 12",
    "desired_quantity": "500",
    "measurement_unit": "units",
    "attributes": {
        "color": "Black",
        "RAM": "4GB",
        "manufacturer": "Apple"
    },
    "desired_price": "1000",
    "currency_code": "USD",
    "delivery_date": "2021-07-11",
}
```  

Sample Response:

```json
{
    "event_line_item_id": 1
}
```

> ### DELETE event_item with event_line_item_id

* HTTP Method - **PATCH**

* Endpoint - **`/event_items/{event_id}/{event_line_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  

  * **Code** - `404`  
  * **Code** - `401`  

Example Request:

```json
```  

Sample Response:

```json
```

## EVENT ITEM ATTRIBUTES

> ### GET list of attribute_id and value with respect to event_line_item_id

* HTTP Method - **GET**

* Endpoint - **`/event_item_attributes/{event_line_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
[
    {
        "attribute_id": 1,
        "attribute_value": "Black",
    },
    {
        "attribute_id": 2,
        "attribute_value": "Apple"
    }
]
```

> ### POST attribute_id and value with respect to event_line_item_id

* HTTP Method - **POST**

* Endpoint - **`/event_item_attributes/{event_line_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "attribute_id": 1,
    "attribute_value": "Black",
}
```  

Sample Response:

```json
```

> ### DELETE attribute_id and value with respect to event_line_item_id

* HTTP Method - **DELETE**

* Endpoint - **`/event_item_attributes/{event_line_item_id}/{attribute_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
```

## EVENT ITEM ATTACHMENTS

> ### GET list of attachments from event_item_attachments with event_line_item_id

* HTTP Method - **GET**

* Endpoint - **`/event_item_attachments/{event_line_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
[
    {
        "attachment_id": 1,
        "attachment_name": "manual1.pdf",
        "attachment_url": "xyz1.com"
    },
    {
        "attachment_id": 2,
        "attachment_name": "manual2.pdf",
        "attachment_url": "xyz2.com"
    }
]
```

## EVENT ITEM SELLERS

> ### GET list of seller_id from event_item_sellers added with event_line_item_id

* HTTP Method - **GET**

* Endpoint - **`/event_item_sellers/{event_line_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
{
    "event_item_seller_ids": [1, 2, 3, 4]
}
```

> ### POST seller to event_item_sellers added with event_line_item_id and seller_id

* HTTP Method - **POST**

* Endpoint - **`/event_item_sellers/{event_line_item_id}/{seller_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "seller_id": 1,
    "approved_by_user": 12,
    "invitation_status": "pending"
}
```  

Sample Response:

```json
```

> ### DELETE seller from event_item_sellers added with event_line_item_id and seller_id

* HTTP Method - **DELETE**

* Endpoint - **`/event_item_sellers/{event_line_item_id}/{seller_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
```

## ENTERPRISE CURRENT SELLERS

> ### GET list of seller_id from enterprise_current_sellers with enterprise_id

* HTTP Method - **DELETE**

* Endpoint - **`/enterprise_current_sellers/{enterprise_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
[1, 2, 3]
```

> ### POST seller_id to enterprise_current_sellers with enterprise_id

* HTTP Method - **DELETE**

* Endpoint - **`/enterprise_current_sellers/{enterprise_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `201`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
{
    "seller_id": 1
}
```  

Sample Response:

```json
```

> ### DELETE seller_id to enterprise_current_sellers with enterprise_id

* HTTP Method - **DELETE**

* Endpoint - **`/enterprise_current_sellers/{enterprise_id}/{seller_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
```

## FOR PAGES

> ### GET list of event_id in which event_item is present with respect to buyer_item_id

* HTTP Method - **DELETE**

* Endpoint - **`/event_items/{buyer_item_id}`**

* Headers  
    Content-Type: application/json  
    Authorization: Bearer `Token`

* Success Response  
  * **Code** - `200`

* Error Responses  
  
  * **Code** - `401`
  * **Code** - `403`  

Example Request:

```json
```  

Sample Response:

```json
{
    "event_ids": [1, 2, 3, 4]
}
```
