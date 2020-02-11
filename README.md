# Synced_2019-nCov

## Get Started

* 先安装依赖项
  * Django
  * apscheduler==2.1.2
* http://106.15.226.129:8080/show/?date=2020-02-11&hour=14

- http://106.15.226.129:8080/api/?date=2020-02-11&hour=14 返回结果如下所示

```
{
    "confirmed_case": 42715,
    "suspected_case": 21675,
    "cured_case": 4022,
    "death_case": 1017,
    "serious_case": 7333,
    "confirmedIncr": 2491,
    "suspectedIncr": 3536,
    "curedIncr": 740,
    "deadIncr": 108,
    "seriousIncr": 108,
    "time": "2020-02-11 14:20:07"
}
```

- ~~目前存在的不足是直接把 https://lab.isaaclin.cn/nCoV/ 的 API 包了一层（不相关字段太多），每次需要请求 https://lab.isaaclin.cn/nCoV/ 的所有数据，请求时间较长，大概需要 25 s 左右的时间才能渲染完上图内容~~

- 目前在服务刚运行的时候请求一次 https://lab.isaaclin.cn/nCoV/ 并保存至 json 数据至本地，之后每小时请求一次新的数据保存，以本地的数据进行查询

- 目前流程：

- - 根据 api 的两个参数去构建一个 10 位的时间戳

  - - date（例如 2020-02-11）
    - hour（例如 14）

  - 以 https://lab.isaaclin.cn/nCoV/ 返回结果中的 13 位时间戳（取 10 位）与用户输入时间所生成的时间戳绝对值的最小值作为最相关的数据

- 根据 https://lab.isaaclin.cn/nCoV/ 返回的结果还有一条重症相关的，暂时没有进行添加