# 亦搜规则  

![update mainfest on push](https://github.com/mabDc/eso_source/workflows/update%20mainfest%20on%20push/badge.svg?branch=master)

## （亦搜为个人创作，社区驱动，从未有任何官网和公众号，更新渠道为github和频道和群。

该仓库用于存放规则文件、合并脚本、规则编写说明与[wiki](https://github.com/mabDc/eso_source/wiki/)，可以网络导入，可以是单个规则，也可以是合并后的规则。规则长期更新，欢迎成为协作者或者提交pr参与规则编写。

### 一般请无视其他直接添加该地址 https://cdn.jsdelivr.net/gh/mabDc/eso_source/manifest 

[merge.py](https://github.com/mabDc/eso_source/blob/master/.github/script/merge.py)是自动合并脚本，合并分类中的文件时会忽略其中的文件夹（含`失效`文件夹）、`*.md`文件和`sub.json`文件，修复失效源后，将其移除`失效`文件夹才会被合并

[mainfest](https://raw.githubusercontent.com/mabDc/eso_source/master/manifest) 是所有源合并后的规则，链接：

`https://raw.githubusercontent.com/mabDc/eso_source/master/manifest`

网络问题可以使用[jsdelivr cdn](https://www.jsdelivr.com/?docs=gh)，即[mainfest from jsdelivr](https://cdn.jsdelivr.net/gh/mabDc/eso_source/manifest)，链接：

`https://cdn.jsdelivr.net/gh/mabDc/eso_source/manifest`

[所有图片源](https://raw.githubusercontent.com/mabDc/eso_source/master/图片/sub.json)合并后的规则链接：

`https://raw.githubusercontent.com/mabDc/eso_source/master/图片/sub.json`

[所有文字源](https://raw.githubusercontent.com/mabDc/eso_source/master/文字/sub.json)合并后的规则链接：

`https://raw.githubusercontent.com/mabDc/eso_source/master/文字/sub.json`

[所有视频源](https://raw.githubusercontent.com/mabDc/eso_source/master/视频/sub.json)合并后的规则链接：

`https://raw.githubusercontent.com/mabDc/eso_source/master/视频/sub.json`

[所有音频源](https://raw.githubusercontent.com/mabDc/eso_source/master/音频/sub.json)合并后的规则链接：

`https://raw.githubusercontent.com/mabDc/eso_source/master/音频/sub.json`


下面是规则编写说明。主要是三类：地址规则、取元素规则、取字符串规则。

响应解析目前仅支持静态，不支持动态，同多多猫，[多多猫插件开发指南](https://www.kancloud.cn/magicdmer/ddcat_plugin_develop/1036896) 解释的很清楚
> **2.5.2 插件的调试**<br>
> ...<br>
> **注意：** Ctrl+u和F12开发者工具Elements面板中显示源代码的的区别是前者显示的是不加载js的html源代码，后者显示的是加载内部外部js后的html代码。sited引擎读取前者代码，所以有时候在浏览器开发者工具（Console面板）能找出数据，在app里却报错，就是因为Ctrl+u源代码中没有相应数据。

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


## 更多内容请查阅 [wiki](https://github.com/mabDc/eso_source/wiki/)