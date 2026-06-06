# Homework 5 報告 - 第 09 組

## 1. 專題概述

本次作業使用一個小型本體來表達 AI Capstone 作業中的基礎任務與 advanced-level 物件，並進行 semantic grounding、graspability inference 與 pressability inference。

涵蓋任務如下：

- 杯子堆疊
- 餐具排列
- 積木收集
- 幫浦瓶按壓（advanced level）

**組員：**

- 組員 1：徐柏安
- 組員 2：鄭家齊
- 組員 3：許維也
- 組員 4：顏名柔
- 組員 5：鄒政昇
- 組員 6：黃柏翔

## 2. 本體設計

共用課程本體定義在 `ontology/imports/course-affordance.ttl`，包含課程中使用的主要詞彙（classes、properties、course objects）。
第 09 組自定義的物件與任務個體則定義在 `ontology/group-ontology.ttl`，使用 `g09:` 命名空間。

本設計區分為：

- 物件類別，例如 `cap:Cup`、`cap:Knife`、`cap:Fork`、`cap:Plate`、`cap:ToyBlock`、`cap:Basket`、`g09:PumpBottle`
- 任務角色類別，例如 `cap:TargetObject`、`cap:ReferenceObject`、`cap:ContainerTarget`、`cap:CollectableObject`
- affordance 類別，例如 `cap:GraspingAffordance`、`cap:SupportAffordance`、`cap:ContainmentAffordance`、`cap:StackabilityAffordance`，以及組別擴充的 `g09:PressingAffordance`
- 推論類別：`cap:GraspableObject` 與 `g09:PressableObject`，使用 `owl:equivalentClass` 定義
- 物件個體，例如 `g09:blueCup01`、`g09:pinkCup01`、`g09:block01`
- 任務個體，例如 `g09:cupStackingTask`、`g09:cutleryArrangementTask`、`g09:blockCollectionTask`、`g09:pumpBottlePressTask`

## 2.1 Advanced-Level Extension

本組在既有的 graspability 建模之外，額外建立 pressability 相關語意。新增:
- `g09:PumpBottle`
- `g09:PressingAffordance`
- `g09:PressableObject`
- `g09:pumpBottlePressTask`
- `g09:pumpBottle01`

`g09:PumpBottle` 代表進階任務中的幫浦瓶物件； 

`g09:PressingAffordance` 用於描述物件具有可按壓特性；

`g09:PressableObject` 則透過 OWL 推論規則自動產生，用來表示具備按壓能力的物件。

### GraspableObject 與 PressableObject 定義


`cap:GraspableObject` 在 `ontology/group-ontology.ttl` 中使用 OWL 等價類定義：


$cap:GraspableObject \equiv cap:PhysicalObject \sqcap \exists cap:hasAffordance.cap:GraspingAffordance$


OWL/Turtle 序列化如下：

```turtle
cap:GraspableObject
    a owl:Class ;
    rdfs:subClassOf cap:PhysicalObject ;
    owl:equivalentClass [
        a owl:Class ;
        owl:intersectionOf (
            cap:PhysicalObject
            [ a owl:Restriction ;
              owl:onProperty cap:hasAffordance ;
              owl:someValuesFrom cap:GraspingAffordance
            ]
        )
    ] .
```

`g09:PressableObject` 也使用相同結構定義，只是把限制目標改成 `g09:PressingAffordance`。因此 graspability 與 pressability 都不是手動直接標註，而是透過推論得到。

### 組別自定義 Properties

除了使用課程共用 properties 外，第 09 組另外定義了兩個 group-specific properties：

- `g09:usedInTask`（`owl:ObjectProperty`）：將物件連結到它所屬的操作任務。
- `g09:hasGripWidthMM`（`owl:DatatypeProperty`）：記錄夾取該物件時的近似夾取寬度（毫米）。

### OWL 資源使用摘要

| OWL/RDFS 資源 | 使用位置 |
| --- | --- |
| `owl:Class` | `cap:GraspableObject`、`g09:PressableObject`、`g09:PumpBottle`、`g09:PressingAffordance` |
| `owl:ObjectProperty` | `g09:usedInTask` |
| `owl:DatatypeProperty` | `g09:hasGripWidthMM` |
| `rdfs:subClassOf` | `cap:GraspableObject rdfs:subClassOf cap:PhysicalObject`、`g09:PressableObject rdfs:subClassOf cap:PhysicalObject` |
| `rdfs:label` | 所有 classes、properties、individuals |
| `rdfs:comment` | 所有 classes、properties、individuals |
| `owl:equivalentClass` + `owl:Restriction` | `cap:GraspableObject` 與 `g09:PressableObject` 的推論定義 |

## 3. 物件與 affordance 對應

| 物件 | 類型 | 角色 | affordance | 是否可抓取 | 是否可按壓 |
| --- | --- | --- | --- | --- | --- |
| `blueCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | 是 | 否 |
| `pinkCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | 是 | 否 |
| `knife01` | `cap:Knife` | `cap:TargetObject` | grasping | 是 | 否 |
| `fork01` | `cap:Fork` | `cap:TargetObject` | grasping | 是 | 否 |
| `plate01` | `cap:Plate` | `cap:ReferenceObject` | support | 否 | 否 |
| `block01` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | 是 | 否 |
| `basket01` | `cap:Basket` | `cap:ContainerTarget` | containment | 否 | 否 |
| `pumpBottle01` | `g09:PumpBottle` | `cap:TargetObject` | pressing | 否 | 是 |

## 4. 命名空間說明

- 共用課程詞彙：`cap:` = `https://hcis.io/ontology/aicapstone/2026/`
- 第 09 組詞彙：`g09:` = `https://hcis.io/ontology/aicapstone/2026/group09/`

第 09 組本體會把 local 物件個體、affordance 個體、gripper 個體、任務個體與組別自定義 properties 都放在 `g09:` 下；共用類別與屬性則維持在 `cap:` 下。`cap:GraspableObject` 的 OWL 等價類定義放在 group ontology 中，因為課程本體未提供此定義。

## 5. 查詢流程

SPARQL 查詢位於 `queries/graspable_objects.rq` 與 `queries/pressable_objects.rq`，應該在包含共用課程本體與第 09 組本體的推論圖上執行。

兩個查詢會分別回傳所有型別為 `cap:GraspableObject` 與 `g09:PressableObject` 的個體，並附帶可選的 label 與 task role。

### 5.1 Advanced Level Query

除了查詢可抓取物件之外，本組另外建立 PressableObject 查詢，用來驗證進階任務中的 Pump Bottle 是否正確完成推論。

查詢內容如下：

```sparql
PREFIX cap: <https://hcis.io/ontology/aicapstone/2026/>
PREFIX g09: <https://hcis.io/ontology/aicapstone/2026/group09/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?obj ?label ?role
WHERE {
    ?obj a g09:PressableObject .

    OPTIONAL { ?obj rdfs:label ?label . }
    OPTIONAL { ?obj cap:hasTaskRole ?role . }
}
ORDER BY ?obj
```

預期結果應包含：

* `g09:pumpBottle01`

代表系統已成功根據 `PressingAffordance` 推論出 `PressableObject `類別。

## 6. 預期結果

預期會被推論為可抓取物件的有：

- `g09:blueCup01`
- `g09:pinkCup01`
- `g09:knife01`
- `g09:fork01`
- `g09:block01`

`plate01`、`basket01` 與 `pumpBottle01` 不應出現在 graspable-object 的結果中，因為它們不是用 grasping affordance 來建模。

預期會被推論為可按壓物件的有：

- `g09:pumpBottle01`

Advanced level 的 `pumpBottle01` 參考自 `aicapstone` 中的 `pump_bottle_press` 任務。該任務的正式描述是 `press the pump bottle once.`。因此本組在 HW5 中加入 `g09:PressingAffordance` 與 `g09:PressableObject`，用來語意化表達這是一個可按壓的 advanced object，同時保留 `cap:hasObjectLabel` 與 `cap:hasPoseFrame` 等對作業有用的資訊。

## 7. 推論輸出

`ontology/inferred-results.ttl` 會記錄 `cap:GraspableObject` 與 `g09:PressableObject` 的推論結果。
它代表推論後的 graph export，可直接用於查詢驗證。

可重現流程：執行 `python src/reason_and_export.py`（需要 `requirements.txt` 裡的 `rdflib`），即可重新產生 `ontology/inferred-results.ttl`、`results/graspable_objects_output.txt` 與 `results/pressable_objects_output.txt`。

## 8. 推理機制與驗證

`cap:GraspableObject` 與 `g09:PressableObject` 在 `ontology/group-ontology.ttl` 中都有正式的 OWL `owl:equivalentClass` 定義。由於 RDFLib 不支援完整 OWL-DL 推理，本提交使用一個輕量級 Python materializer，其推理邏輯忠實反映了本體中的 OWL 語意：
1. 先檢查每個物件是否為 `cap:PhysicalObject`（含子類別）。
2. 再檢查該物件是否有 `cap:hasAffordance` 指向目標 affordance 類型的個體
3. 當兩個條件同時成立時，就會在推論圖中加入對應的推論類別。

(作業明確允許 Python/RDFLib-based workflow，前提是清楚說明額外推理機制。)

驗證步驟：

- 重新執行 `python src/reason_and_export.py`
- 檢查 `ontology/inferred-results.ttl`，確認是否有五個 graspable 成員與一個 pressable 成員
- 檢查 `results/graspable_objects_output.txt` 與 `results/pressable_objects_output.txt`，確認 SPARQL 查詢結果是否一致
- 如果有使用 Widoco，則檢查 `docs/group09/doc/index-en.html` 是否已正確產生 ontology 文件

### 8.1 PressableObject 推論範例

Pump Bottle 的推論流程如下：

首先，系統定義 `g09:pumpBottle01` 為 `g09:PumpBottle` 類別的個體，並透過 `cap:hasAffordance` 連結至 `g09:pumpBottlePressingAffordance`。

```turtle
g09:pumpBottle01
    cap:hasAffordance
        g09:pumpBottlePressingAffordance .

g09:pumpBottlePressingAffordance
    a g09:PressingAffordance .
```

由於本體中定義：

$g09:PressableObject \equiv cap:PhysicalObject \sqcap \exists cap:hasAffordance.g09:PressingAffordance$

因此當推理程式檢查到：

1. 該物件屬於 PhysicalObject
2. 該物件具有 PressingAffordance

兩項條件同時成立時，便會自動加入：

```turtle
g09:pumpBottle01
    rdf:type
        g09:PressableObject .
```

此推論結果後續可透過 SPARQL 查詢進行驗證。

## 9. Limitations
雖然本小組成功建立並驗證了包含 `GraspableObject` 與進階 `PressableObject` 的本體模型，但在現有架構下仍存在以下侷限性：

1. 推理機能力限制：
由於本作業採用 RDFLib 搭配自定義的輕量級 Materializer 進行推理，而非使用標準的 OWL-DL 推理機。這導致系統無法原生處理複雜的描述邏輯的邏輯來模擬 `owl:equivalentClass` 的交集與存在量化限制。

2. 靜態語意與動態物理狀態的脫鉤：
目前的本體設計屬於靜態知識庫。在實際的 AI Capstone 機器人操作中，Affordance 往往會隨著環境動態改變。例如：一個幫浦瓶 `g09:pumpBottle01`被判定為 PressableObject，但如果它的蓋子被鎖住，或者機器人手臂的夾爪角度不對，該 Affordance 在物理層面上便會失效。目前本體缺乏表達動態前後置條件與環境脈絡的機制。

3. 缺乏資料驗證機制：
本專案目前未引入 SHACL 或 ShEx。雖然可以透過 OWL 的限制條件定義等價類，但無法在資料輸入階段強制驗證圖資料的結構完整性。

4. 幾何與空間資訊的簡化：
雖然本組擴充了 `g09:hasGripWidthMM` 作為 Datatype Property，但對於三維空間中的操作任務而言，單一的一維度夾取寬度不足以描述複雜的物體幾何形狀。本體尚未與 3D 網格或點雲等低階感測資料進行深度的語意連結。

## 10. Venv 使用說明

建議使用 Python 虛擬環境來執行這份作業。

建立 venv：

```powershell
python -m venv .venv
```

啟用 venv：

```powershell
.\.venv\Scripts\Activate.ps1
```

若 PowerShell 阻擋腳本執行，可先設定：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

安裝與執行：

```powershell
python -m pip install -r requirements.txt
python src/reason_and_export.py
```

## 11. Discussion & Future Work
針對本次作業的設計過程與語意網在機器人領域的應用，本小組提出以下幾點討論：

1. Advanced-Level 建模的擴展性討論

    在本次作業中，我們將 `g09:PressingAffordance` 與 `g09:PressableObject` 作為進階任務的核心。這種設計模式展示了本體論的強大擴展性：當機器人需要學習新任務時，我們不需要重構整個底層架構，而只需要引入新的 Affordance 類別與等價類推理規則。 這種基於 Affordance 的建模方式，能讓機器人更好地泛化到未見過的物件。例如，未來若出現「按壓式開關」或「鍵盤按鍵」，只要賦予其 PressingAffordance，機器人便能自動將其歸類為 PressableObject。

2. 異質知識的整合：T-Box、A-Box 與 機器人控制

    在實作過程中，我們體會到知識圖譜中 T-Box與 A-Box 分離的好處。

    * 課程共用本體（cap:）作為頂層本體（Upper Ontology），規範了標準任務流程。

    * 組別本體（g09:） 則作為領域本體（Domain Ontology），定義了具體的物理場景。

    這種架構在實際應用中，可以作為機器人任務規劃器的語意大腦。透過 SPARQL 查詢，機器人可以先在語意層面決定該拿什麼以及該按什麼，再將查詢結果的數值（如 g09:hasGripWidthMM）傳遞給低階的運動規劃演算法，實現高低階控制的解耦。
