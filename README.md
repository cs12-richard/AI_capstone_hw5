# AI Capstone 作業 5 - 第 09 組

這個倉庫是 AI Capstone Homework 5 的本體式語意對應提交內容，包含本體、推論結果、SPARQL 查詢與報告。

## 內容

- `course-affordance.ttl`：課程共用本體，包含 `cap:GraspableObject` 的定義。
- `course-alignment.ttl`：課程層級的 SKOS 對應說明。
- `ontology/group-ontology.ttl`：第 09 組自行建模的本體，包含物件個體與 affordance 個體。
- `ontology/inferred-results.ttl`：推論後產生的 `cap:GraspableObject` 成員關係。
- `queries/graspable_objects.rq`：查詢推論後可抓取物件的 SPARQL。
- `results/graspable_objects_output.txt`：查詢輸出結果。
- `report.md`：作業報告。

## 第 09 組建模內容

第 09 組只涵蓋作業中的基礎任務：

- 杯子堆疊：`blueCup01`、`pinkCup01`
- 餐具排列：`knife01`、`fork01`、`plate01`
- 積木收集：`block01`、`basket01`

本組本體使用 `https://hcis.io/ontology/aicapstone/2026/group09/`，前綴為 `g09:`。課程共用詞彙，例如 `cap:Cup`、`cap:Knife`、`cap:GraspingAffordance`、`cap:GraspableObject`，都保留在 `cap:` 命名空間。

## 推論模式

`cap:GraspableObject` 在 `course-affordance.ttl` 中被定義為：具有至少一個 `cap:hasAffordance`，且該 affordance 的型別為 `cap:GraspingAffordance` 的物理物件。

本組本體針對杯子、刀子、叉子與積木建立 grasping affordance 個體，因此這些物件會被推論成 `cap:GraspableObject`。盤子與籃子只配置 support 與 containment affordance，所以不會出現在可抓取物件的查詢結果中。

## SPARQL 查詢

SPARQL 查詢位於 `queries/graspable_objects.rq`，應該在「包含 course ontology 與 group ontology 的推論圖」上執行。

範例查詢：

```sparql
PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?obj ?label ?role
WHERE {
  ?obj a cap:GraspableObject .
  OPTIONAL { ?obj rdfs:label ?label . }
  OPTIONAL { ?obj cap:hasTaskRole ?role . }
}
ORDER BY ?obj
```

## 預期結果

預期會出現的推論結果如下：

- `blueCup01`
- `pinkCup01`
- `knife01`
- `fork01`
- `block01`

`plate01` 與 `basket01` 不應出現在結果中，因為它們不是用 grasping affordance 建模。

## 產生與驗證說明

`ontology/inferred-results.ttl` 會記錄第 09 組推論出的 `cap:GraspableObject` 成員。
這個檔案是由 Python workflow 產生的推論輸出，也會搭配查詢結果一起提交。

## 推理機制

本作業使用一個可重現的 Python workflow，基於 RDFLib 來 materialize `cap:GraspableObject`。

腳本會對每個候選物件檢查兩個條件：

1. 該物件是 `cap:PhysicalObject`，或是其子類別
2. 該物件至少有一個 `cap:hasAffordance`，而且該 affordance 的型別是 `cap:GraspingAffordance`，或其子類別

若兩個條件都成立，就會把 `?obj a cap:GraspableObject` 加入推論圖。

這是一個輕量級推理機制，不是完整 OWL-DL reasoner。因為作業允許使用 RDFLib-based workflow，只要清楚說明額外使用的推理機制，就可以接受。

## 如何執行

### 方式 A：建立並啟用 venv

如果你還沒有虛擬環境，可以先建立：

```powershell
python -m venv .venv
```

在 Windows PowerShell 啟用：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 不允許執行腳本，可以先執行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 方式 B：安裝套件並執行推論

```powershell
python -m pip install -r requirements.txt
python src/reason_and_export.py
```

## 如何驗證

1. 確認 `ontology/inferred-results.ttl` 有重新產生。
2. 確認 `results/graspable_objects_output.txt` 有 5 筆預期結果。
3. 如有需要，可以重新執行 `queries/graspable_objects.rq`，確認查詢結果一致。
4. 若你有用 Widoco，確認 `docs/group09/doc/index-en.html` 已經成功生成，且頁面中有 classes、properties、named individuals 等區塊。

## Widoco 文件產生與查看

如果你要重新產生 ontology 文件，可以用 Widoco 針對 `ontology/group-ontology.ttl` 生成 HTML 文件。

前提：電腦上要先有 Java 17，因為 Widoco 需要 Java 執行環境。

執行指令範例：

```powershell
java -jar "widoco-1.4.25-jar-with-dependencies_JDK-17.jar" -ontFile "ontology/group-ontology.ttl" -outFolder "docs/group09" -rewriteAll -uniteSections
```

產生完成後，主要頁面會在：

- `docs/group09/doc/index-en.html`

如果要本機直接開啟查看，可以在 `docs/group09/doc` 目錄下啟動簡單伺服器：

```powershell
python -m http.server 8000
```

然後用瀏覽器開啟：

- `http://localhost:8000/index-en.html`

## 可重現流程

- **需求**：Python 3.8 以上、`rdflib`，以及本機的 `venv`（建議使用）。
- **執行**：先啟用 `venv`，再執行 `python -m pip install -r requirements.txt` 和 `python src/reason_and_export.py`。
- **輸出**：會重新產生 `ontology/inferred-results.ttl` 與 `results/graspable_objects_output.txt`。

## 組員

- 請在繳交前把下面兩行改成實際組員姓名。
- 組員 1：徐柏安
- 組員 2：YOUR NAME
