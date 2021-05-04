데이터
===

YouTube Data API에 사용되는  데이터
---

``` json
{
  "snippet": {
    "title": string,
    "description": string,
    "thumbnails": {
      "default": {
        "url": string,
        "width": unsigned integer,
        "height": unsigned integer
      },
      "medium": {
        "url": string,
        "width": unsigned integer,
        "height": unsigned integer
      },
      "high": {
        "url": string,
        "width": unsigned integer,
        "height": unsigned integer
      }
    },
    "channelTitle": string,
    "tags": [
      string
    ],
    "categoryId": string
  }
}
```

정형 데이터 | Table Storage
---

- PartitionKey = "data"
- RowKey = randomkey
- title
- description
- tags
- categoryId
- video file name
- thubmnail file name (default, medium, high)

비정형 데이터 | Blob Storage
---

- 동영상 파일
- 썸네일 이미지

Blob storage 구조
---

![data structure](./img/datastructure.png)

데이터 전달 과정
---

![LogicApps](./img/logicapps.png)
HTTP 요청을 수신하는 경우: UploadTime, RowKey 받음  
다음 기간까지 지연: UploadTime 까지  
HTTP: DataGather function 실행하는 URL 요청(with. RowKey)  
  
DataGather function: Table에서 RowKey에 맞는 엔터티를 찾고 YoutubeUpload function 실행하는 URL 요청(with. entity information)  
YoutubeUpload function: 받은 정보로 Blob에서 비디오와 썸네일 파일을 가져오고 YoutubeDataAPI 실행
