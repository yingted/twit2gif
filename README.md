# Twitter to GIF
## API
### HTTP
#### bluemix
##### POST /entities
Content type: `application/json`
Content:
```js
[ // Paragraphs
	'Patrick Ryan was hired by IBM in 2004. He works in New York.',
	...
]
```
Response:
```js
[ // Paragraphs
	[ // Sentences
		'_NNP was_VBD hired_VBN by_IN _NNP in_IN #_CD _.', // Entities (opaque strings)
		...
	],
	...
]
```
#### web
##### POST /query
Content type: `application/x-www-form-urlencoded` or `application/json`
Content:
```
text=...
```
Response:
```js
{
	"quote": "...",
	"url": "...",
}
```
##### GET /render/{id}.gif
Lazily renders subtitle `id`.
