# AI Capstone 作業 5 - 第 09 組

這個倉庫是 AI Capstone Homework 5 的本體式語意對應提交內容，包含本體、推論結果、SPARQL 查詢與報告。

## 內容

- `ontology/imports/course-affordance.ttl`：課程共用本體，包含 `cap:GraspableObject` 所需的基礎詞彙。
- `ontology/imports/course-alignment.ttl`：課程層級的 SKOS 對應說明。
- `ontology/group-ontology.ttl`：第 09 組自行建模的本體，包含 `cap:GraspableObject` 的 OWL 等價類定義、物件個體、affordance 個體、任務個體，以及組別自定義的 properties。
- `ontology/inferred-results.ttl`：推論後產生的 `cap:GraspableObject` 成員關係。
- `queries/graspable_objects.rq`：查詢推論後可抓取物件的 SPARQL。
- `results/graspable_objects_output.txt`：查詢輸出結果。
- `src/reason_and_export.py`：Python materializer，用來推論 `cap:GraspableObject` 並匯出結果。
- `report.md`：作業報告。

## 第 09 組建模內容

第 09 組涵蓋作業中的三個基礎任務：

- 杯子堆疊：`blueCup01`、`pinkCup01`
- 餐具排列：`knife01`、`fork01`、`plate01`
- 積木收集：`block01`、`basket01`

本組本體使用 `https://hcis.io/ontology/aicapstone/2026/group09/`，前綴為 `g09:`。課程共用詞彙，例如 `cap:Cup`、`cap:Knife`、`cap:GraspingAffordance`、`cap:GraspableObject`，都保留在 `cap:` 命名空間。

## 物件與 Affordance 對應表

| 物件 | 類型 | 任務角色 | Affordance | 是否可抓取（推論） |
| --- | --- | --- | --- | --- |
| `g09:blueCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | ✅ 是 |
| `g09:pinkCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | ✅ 是 |
| `g09:knife01` | `cap:Knife` | `cap:TargetObject` | grasping | ✅ 是 |
| `g09:fork01` | `cap:Fork` | `cap:TargetObject` | grasping | ✅ 是 |
| `g09:plate01` | `cap:Plate` | `cap:ReferenceObject` | support | ❌ 否 |
| `g09:block01` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | ✅ 是 |
| `g09:basket01` | `cap:Basket` | `cap:ContainerTarget` | containment | ❌ 否 |

## 推論模式

`cap:GraspableObject` 在 `ontology/group-ontology.ttl` 中使用 OWL `owl:equivalentClass` 定義為：

```
cap:GraspableObject ≡ cap:PhysicalObject ⊓ ∃cap:hasAffordance.cap:GraspingAffordance
```

即一個物理物件若至少有一個 `cap:hasAffordance` 且該 affordance 的型別為 `cap:GraspingAffordance`，就會被推論成 `cap:GraspableObject`。

本組本體針對杯子、刀子、叉子與積木建立 grasping affordance 個體，因此這些物件會被推論成 `cap:GraspableObject`。盤子與籃子只配置 support 與 containment affordance，所以不會出現在可抓取物件的查詢結果中。

## 命名空間說明

- 共用課程詞彙：`cap:` = `https://hcis.io/ontology/aicapstone/2026/`
- 第 09 組詞彙：`g09:` = `https://hcis.io/ontology/aicapstone/2026/group09/`

第 09 組本體會把 local 物件個體、affordance 個體、gripper 個體、任務個體與組別自定義 properties（`g09:usedInTask`、`g09:hasGripWidthMM`）都放在 `g09:` 下；共用類別與屬性則維持在 `cap:` 下。`cap:GraspableObject` 的 OWL 等價類定義也放在 group ontology 中，因為課程本體未提供此定義。

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

- `g09:blueCup01`
- `g09:pinkCup01`
- `g09:knife01`
- `g09:fork01`
- `g09:block01`

`plate01` 與 `basket01` 不應出現在結果中，因為它們不是用 grasping affordance 建模。

## 產生與驗證說明

`ontology/inferred-results.ttl` 會記錄第 09 組推論出的 `cap:GraspableObject` 成員。
這個檔案是由 Python workflow 產生的推論輸出，也會搭配查詢結果一起提交。

## 推理機制

本作業使用一個可重現的 Python workflow，基於 RDFLib 來 materialize `cap:GraspableObject`。

`cap:GraspableObject` 在 `ontology/group-ontology.ttl` 中有正式的 OWL `owl:equivalentClass` 定義。由於 RDFLib 不支援完整 OWL-DL 推理，腳本會對每個候選物件檢查兩個條件：

1. 該物件是 `cap:PhysicalObject`，或是其子類別
2. 該物件至少有一個 `cap:hasAffordance`，而且該 affordance 的型別是 `cap:GraspingAffordance`，或其子類別

若兩個條件都成立，就會把 `?obj a cap:GraspableObject` 加入推論圖。

這個推理邏輯忠實地反映了本體中 `owl:equivalentClass` 的語意。作業允許使用 RDFLib-based workflow，只要清楚說明額外使用的推理機制。

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
cd docs/group09/doc
python -m http.server 8000
```

然後用瀏覽器開啟：

- `http://localhost:8000/index-en.html`

或者直接用瀏覽器開檔案（不需要伺服器）：

```powershell
start docs/group09/doc/index-en.html
```

### 如何確認 Widoco 文件是正確的

開啟 `index-en.html` 後，請確認頁面中有以下區塊：

1. **標題**：頁面上方顯示 「AI Capstone 2026 Group 09 Ontology」，Release 日期為 2026-05-27。
2. **Overview**：可以看到本體 URI `https://hcis.io/ontology/aicapstone/2026/group09/` 與 `owl:imports` 連結。
3. **Cross-reference**：列出以下項目：
   - Class：`graspable object`（`cap:GraspableObject`），應包含 `owl:equivalentClass` 定義
   - Object Property：`used in task`（`g09:usedInTask`），顯示 domain / range
   - Data Property：`has grip width in millimeters`（`g09:hasGripWidthMM`），顯示 domain / range
4. **Named Individuals**：應列出所有個體，包括：
   - 物件：blue cup 01、pink cup 01、knife 01、fork 01、plate 01、toy block 01、basket 01
   - 任務：cup stacking task、cutlery arrangement task、toy block collection task
   - 其他：group 09 gripper，以及各物件的 affordance 個體

如果頁面空白或缺少上述任何區塊，請重新執行 Widoco 指令。

## 檔案連結

| 檔案 | 說明 |
| --- | --- |
| [group-ontology.ttl](ontology/group-ontology.ttl) | 第 09 組本體（含 GraspableObject 定義） |
| [inferred-results.ttl](ontology/inferred-results.ttl) | 推論結果 |
| [course-affordance.ttl](ontology/imports/course-affordance.ttl) | 課程共用本體（imported） |
| [course-alignment.ttl](ontology/imports/course-alignment.ttl) | SKOS 對應（imported） |
| [graspable_objects.rq](queries/graspable_objects.rq) | SPARQL 查詢 |
| [graspable_objects_output.txt](results/graspable_objects_output.txt) | 查詢輸出 |
| [reason_and_export.py](src/reason_and_export.py) | 推論腳本 |
| [report.md](report.md) | 作業報告 |

## 可重現流程

- **需求**：Python 3.8 以上、`rdflib`，以及本機的 `venv`（建議使用）。
- **執行**：先啟用 `venv`，再執行 `python -m pip install -r requirements.txt` 和 `python src/reason_and_export.py`。
- **輸出**：會重新產生 `ontology/inferred-results.ttl` 與 `results/graspable_objects_output.txt`。

## 組員

- 組員 1：徐柏安
- 組員 2：鄭家齊
- 組員 3：許維也
- 組員 4：顏名柔
- 組員 5：鄒政昇
- 組員 6：黃柏翔
