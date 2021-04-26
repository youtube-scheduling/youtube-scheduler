테스트 (Data Gathering)
===

used file & service
---

- \_\_init__.py
- function.json
- azure storage account(container, table)
- azure functions

environment
---

local 에서 진행   
HttpExample: 임시 function name   
table entity의 RowKey를 search_key로 사용

***

### Request

    http://localhost:7071/api/HttpExample?search_key=0001

### Return

    videos/1.avi thumbnails/thumbnail.png
