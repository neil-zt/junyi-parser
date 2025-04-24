# 均一教育平台 Open Content API 資料處理

將均一教育平台（@junyiacademy）的 Open Content API 資料去除過多的分類層級後，轉換為更易懂的格式，用來產生一個 LLM 易懂的學習內容清單、單元列表。

> 這個 repository 只提中了一個暫時性的解決方案。我們依然需要有人將台灣十二年國民基本教育的課綱、課程目錄、課程內容轉化為 LLM 易懂的形式，並持續更新這些資料，以加快 AI 應用於教育的速度。若有想法，請 Email 我：`hi@neillu.com`

## 使用方法

### 1. 獲取均一 Open Content API 資料

您可以直接使用這個 repository 中的 `contents.json` 檔案，或是至均一的官方 API 獲取最新的資料。API 如下所列，建議使用 `<depth>=5` 來獲取完整的資料：

```
https://www.junyiacademy.org/api/v2/open/sub-tree/root?depth=<depth>
```

詳細使用說明請見均一的官方文件：[Open Content API](https://junyiacademy.notion.site/For-Developers-70572b991b614b03a2a93fbf73d0b089)。

### 2. 直接執行 Python 腳本

在本地端安裝 Python 3.x 環境後，將 `junyi_parser.py` 腳本下載至本地端，並執行。請自行修改其中的變數設定。執行完成後，應當可見如範例檔案 `contents_flat.json` 的檔案。這個檔案是將均一的 Open Content API 資料轉換為更易懂的格式，並去除過多的分類層級後的結果。

### 3. 使用最終檔案

完成後的 JSON 可用於各種用途，例如：讓 LLM 更容易理解學習內容、單元列表等。您可以將這些資料用於自己的應用程式或服務中，唯請注意遵守均一的資料使用條款，並給予適當的引用。

## 使用授權

The author of this repository does not claim copyright over the Python scripts in this repository. Therefore, the script `junyi_parser.py` is released into the public domain. 

Example data, however, are subject to the license of the original data source: Junyi Academy. The data is licensed under the [CC BY-NC-SA 3.0 TW](https://creativecommons.org/licenses/by-nc-sa/3.0/tw/) license. You are free to share and adapt the data, but you MUST give appropriate credit, provide a link to the license, and indicate if changes were made. You may not use the material for commercial purposes. If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

The Python scripts are not considered as a derivative work of the data, but is instead only a tool to process the data. Therefore, the author of this repository does not impose any additional restrictions on the use of the scripts, and does not share it under the same license as the original data. 

Please see the [License](https://www.junyiacademy.org/about/licence) for the original data.