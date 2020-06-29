# 亦搜规则  

![update mainfest on push](https://github.com/mabDc/eso_source/workflows/update%20mainfest%20on%20push/badge.svg?branch=master)

这个仓库用于存放亦搜规则。

[merge.sh](https://github.com/mabDc/eso_source/blob/master/merge.sh)是自动合并脚本

[mainfest](https://raw.githubusercontent.com/mabDc/eso_source/master/manifest) 是合并后的规则，链接：

`https://raw.githubusercontent.com/mabDc/eso_source/master/manifest`

可以使用cdn [jsdelivr cdn](https://cdn.jsdelivr.net/gh/mabDc/eso_source/manifest)，链接：

`https://cdn.jsdelivr.net/gh/mabDc/eso_source/manifest`

下面是规则编写说明。主要是三类：地址规则、取元素规则、取字符串规则。

## 地址规则

请用`源编辑界面`的`地址模版`，

```javascript
@js:
(() => {
  var url = `/xx${keyword}xx${page}`;
  var method = "get"; // or "post"
  var body = {};
  var headers = {};
  // var encoding = "gbk";
  return {url, method, body, headers};
})();
```

需要对搜索关键词进行中文编码则为

```javascript
@js:
(() => {
  var url = `/xx${keyword}xx${page}`;
  var method = "get"; // or "post"
  var body = {};
  var headers = {};
  var encoding = "gbk";
  return {url, method, body, encoding, headers};
})();
```

响应解码由app内部自动处理，无需了解。

## 取元素规则

使用`jsonpath`、`xpath`、`css`或者`js`编写，其中前三种可以网页右键复制路径，app自动识别。

如`$..item.*`或者`//li`或者`li`等，若用`js`，最后应输出`Array`对象


## 取字符串规则

形如 `rule##replaceRegex##replacement##replaceFirst`

其中 `rule` 可以是 `js` 或 `css` 或 `xpath` 或 `jsonpath` , 形式如下:

`@js:js code`

`@json:$.name` 或 `$.name`（省略`@json:`）

`@css:.name@text` 或 `.name@text`（省略`@css:`）

`@xpath://*[class=name]/text()` 或 `//*[class=name]/text()`（省略`@xpath:`）

`:regex`

建议省略`@json:`，`@css:`，`@xpath:`，由app自动识别。

如果需要拼接则用`aaa{{rulexxx}}bbb{{ruleyyy}}ccc`

## 其他规则

1. 所有规则含`host`，除搜索和发现地址都含有`result`，除地址都含有`baseUrl`。

2. `结果规则`会成为下一条`地址规则`的`result`，成为下一条除地址规则的`lastResult`。地址规则的响应会成为其他规则的`result`。

3. 地址规则不用js时，使用`$加变量名`来动态替换实际内容，包含`$keyword`，`$page`,`$result`,`$host`等。地址规则使用js时请写变量名，不需要带`$`。

4. 可以用`http.get(url)`来获取请求。

5. 规则搜索部分共用一个js上下文，目录部分也共用一个js上下文。同一个上下文的规则的全局变量可以直接相互获取。（如用于目录列表设置id，章节结果获取所设置的id）



## 基础

  + JSONPath 
    - 形式 `@JSon:$.jsonPath` 或 `@JSon:jsonPath` 或 `$.jsonPath`
    - 标准规范 [goessner JSONPath - XPath for JSON](https://goessner.net/articles/JsonPath/)
    - 实现库 [dart-json-path](https://github.com/qhzhyt/dart-json-path.git)
    - 在线测试 [Jayway JsonPath Evaluator](http://jsonpath.herokuapp.com/)
  + XPath
    - 形式 `@XPath:xpath` 或 `//xpath`
    - 标准规范 [W3C XPATH 1.0](https://www.w3.org/TR/1999/REC-xpath-19991116/) 
    - 实现库 [xpath_parse](https://pub.flutter-io.cn/packages/xpath_parse)
  + CSS
    - 形式 `@css:css` 或 `css`
    - 实现库 [csslib](https://pub.flutter-io.cn/packages/csslib)
    - 在线测试 [Try jsoup online: Java HTML parser and CSS debugger](https://try.jsoup.org/)
  + 正则
    - 形式 `##replaceRegex##replacement##replaceFirst`
    - 教程 [veedrin/horseshoe 2018-10 | Regex专题](https://github.com/veedrin/horseshoe#2018-10--regex%E4%B8%93%E9%A2%98)
      > [语法](https://github.com/veedrin/horseshoe/blob/master/regex/%E8%AF%AD%E6%B3%95.md)
      > [方法](https://github.com/veedrin/horseshoe/blob/master/regex/%E6%96%B9%E6%B3%95.md)
      > [引擎](https://github.com/veedrin/horseshoe/blob/master/regex/%E5%BC%95%E6%93%8E.md)
  + 自定义三种连接符：`&&, ||, %%`
  + 不支持动态内容，所有的规则解析以静态加载的内容为准。
  + 动态与静态的问题 [多多猫插件开发指南](https://www.kancloud.cn/magicdmer/ddcat_plugin_develop/1036896) 解释的很清楚
    > **2.5.2 插件的调试**<br>
    > ...<br>
    > **注意：** Ctrl+u和F12开发者工具Elements面板中显示源代码的的区别是前者显示的是不加载js的html源代码，后者显示的是加载内部外部js后的html代码。sited引擎读取前者代码，所以有时候在浏览器开发者工具（Console面板）能找出数据，在app里却报错，就是因为Ctrl+u源代码中没有相应数据。
  + 规则形式为 `rule##replaceRegex##replacement##replaceFirst`

###  JSONPath 与 XPath 参考 
- 提供给书写时查阅，可当作使用手册，无需记住具体写法。
- 来源是 [goessner JSONPath - XPath for JSON](https://goessner.net/articles/JsonPath/)

**数据文件**

```JSON
{ "store": {
    "book": [ 
      { "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      { "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      },
      { "category": "fiction",
        "author": "Herman Melville",
        "title": "Moby Dick",
        "isbn": "0-553-21311-3",
        "price": 8.99
      },
      { "category": "fiction",
        "author": "J. R. R. Tolkien",
        "title": "The Lord of the Rings",
        "isbn": "0-395-19395-8",
        "price": 22.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  }
}
```

**操作符**

XPath | JSONPath | Description
:--: | :--: | :---
`/` | `$` | the root object/element
`.` | `@` | the current object/element
`/` | `. or []` | child operator
`..` | `n/a` | parent operator
`//` | `..` | recursive descent. JSONPath borrows this syntax from E4X.
`*` | `*` | wildcard. All objects/elements regardless their names.
`@` | `n/a` | attribute access. JSON structures don't have attributes.
`[]` | `[]` | subscript operator. XPath uses it to iterate over element collections and for predicates. In Javascript and JSON it is the native array operator.
&#124; | `[,]` | Union operator in XPath results in a combination of node sets. JSONPath allows alternate names or array indices as a set.
`n/a` | `[start:end:step]` | array slice operator borrowed from ES4.
`[]` | `?()` | applies a filter (script) expression.
`n/a` | `()` | script expression, using the underlying script engine.
`()` | `n/a` | grouping in Xpath

**示例对比**

XPath | JSONPath | Result
:--: | :--: | :---
`/store/book/author` | `$.store.book[*].author` | the authors of all books in the store
`//author` | `$..author` | all authors
`/store/*` | `$.store.*` | all things in store, which are some books and a red bicycle.
`/store//price` | `$.store..price` | the price of everything in the store.
`//book[3]` | `$..book[2]` | the third book
`//book[last()]` | `$..book[(@.length-1)]`<br>`$..book[-1:]` | the last book in order.
`//book[position()<3]` | `$..book[0,1]`<br>`$..book[:2]` | the first two books
`//book[isbn]` | `$..book[?(@.isbn)]` | filter all books with isbn number
`//book[price<10]` | `$..book[?(@.price<10)]` | filter all books cheapier than 10
`//*` | `$..*` | all Elements in XML document. All members of JSON structure.

