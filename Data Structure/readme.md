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

Blob storage 구조 (예정)
---

![data structure](./img/datastructure.png)
