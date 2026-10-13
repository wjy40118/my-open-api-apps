# Open API 作业包 —— 提交说明

课程：Arts and Advanced Big Data ｜ Step-by-Step Guide: Open API ｜ Prof. Jahwan Koo

这份作业按讲义《Open-API-Step-by-Step-Guide-01》的 7 个步骤做，最终产出是三个可以公开访问的网页应用。

## 一、文件清单

| 文件 | 对应步骤 | 作用 |
| --- | --- | --- |
| `met_app.py` | Step 4 | 服务 1：搜索大都会博物馆藏品并显示图片（无需密钥） |
| `weather_map.py` | Step 6 | 服务 2：点地图任意位置，查该地逐小时气温并画折线图（无需密钥） |
| `secret_demo.py` | Step 7 | 服务 3：API 密钥的安全写法演示（密钥存 Secrets，不写进代码） |
| `requirements.txt` | Step 5 | 依赖清单，三个应用共用这一份 |

## 二、本地试跑（可选）

```bash
pip install -r requirements.txt
streamlit run met_app.py
streamlit run weather_map.py
streamlit run secret_demo.py
```

浏览器会自动打开 `http://localhost:8501`。

## 三、部署上线（Step 5 / Step 6 / Step 7）

1. 在 GitHub 新建一个 **public** 仓库，例如 `my-open-api-apps`。
2. 把上面 4 个文件上传到仓库根目录（`requirements.txt` 一份就够，Service 2 的包已经写在里面）。
3. 打开 <https://share.streamlit.io>，点 **Create app** → **Yup, I have an app**。
4. 选择你的仓库和分支，**Main file path** 分别填 `met_app.py`、`weather_map.py`、`secret_demo.py`，点 **Deploy**。
5. 一个仓库可以部署多个应用，重复第 3–4 步即可，三个应用得到三个链接。
6. 给 `secret_demo.py` 添加密钥：应用页面右上角 **Settings → Secrets**，加一行
   `MY_API_KEY = "abcd1234"`（练习阶段用假值即可），保存后重新加载。

## 四、自测清单（讲义 Step 5 / Step 6）

- 服务 1：搜 `flower`、`cat`、`ocean`、`gold`，图片和文字正常显示；搜 `zzzzqq` 出现友好的"没有结果"提示，而不是报错。
- 服务 2：依次点首尔、釜山、海面，三张气温图的曲线和高低温数字会跟着变化。
- 服务 3：没配 Secrets 时提示 `No API key found`；配好之后显示 `API key found`，并且只显示密钥前 3 位。
- 用手机打开应用链接，确认能正常访问。

## 五、Step 2 / Step 3 的实测记录（可写进报告）

以下结果是 2026-10-13 实际调用得到的，可以直接作为讲义 Step 2、Step 3 的证据。

Step 2：浏览器里直接访问 Open-Meteo 的地址

```text
https://api.open-meteo.com/v1/forecast?latitude=37.57&longitude=126.98&hourly=temperature_2m&forecast_days=1&timezone=auto
```

- 状态码 200，返回 JSON，其中 `hourly.time` 与 `hourly.temperature_2m` 各有 24 个值（首尔未来 24 小时）——讲义的"首尔天气"一例成立。
- 把经纬度换成东京 (35.68, 139.65)，同一地址返回东京的数据：地址不变、参数变，结果就变。

Step 2：大都会博物馆两步式查询

```text
第 1 步搜索：https://collectionapi.metmuseum.org/public/collection/v1.1/search?q=flower&hasImages=true&limit=3
第 2 步详情：https://collectionapi.metmuseum.org/public/collection/v1/objects/196563
```

- 搜索返回 `total = 39446`，`objectIDs = [196563, 196560, 198662]`。
- 用 196563 查详情，得到 `title = "Plate"`、`artistDisplayName = "Joseph Flower"`、`objectDate = "ca. 1750"`，且 `primaryImageSmall` 有图片地址。
- 注意：搜索必须用 `v1.1`，旧的 `v1/search` 按讲义说法已于 2026 年 10 月退役。

## 六、容易踩的坑

- `404` / 搜不到：确认搜索地址用的是 `v1.1`，详情地址结尾是真实的数字 ID。
- `KeyError`：字段名拼错或该藏品没有这个字段，改用 `.get()`。
- `ModuleNotFoundError: folium / streamlit_folium`：`requirements.txt` 里缺包，补上后重新部署。
- `429 Too Many Requests`：请求太快，靠 `st.cache_data` 缓存来缓解。
- AI 生成的地址打不开：模型会编接口，务必拿官方文档和 Step 2 浏览器里看到的结果核对（提示词里要给出真实地址和真实字段名）。

## 七、提示词配方（Step 4 要求掌握的四要素）

**Source（真实地址）→ Fields（真实字段名）→ Display（用户看到什么）→ Failure（出错怎么办）**。
两个应用的提示词原文见讲义 Step 4 和 Step 6，可以直接照抄改写。
