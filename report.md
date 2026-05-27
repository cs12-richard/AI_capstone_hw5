# Homework 5 報告 - 第 09 組

## 1. 專題概述

本次作業使用一個小型本體來表達 AI Capstone 作業中的基礎任務，並進行 semantic grounding 與 graspability inference。

涵蓋任務如下：

- 杯子堆疊
- 餐具排列
- 積木收集

**組員：**

- 組員 1：YOUR NAME
- 組員 2：YOUR NAME

## 2. 本體設計

共用課程本體定義在 `course-affordance.ttl`，包含課程中使用的主要詞彙。
第 09 組自定義的物件與任務個體則定義在 `ontology/group-ontology.ttl`，使用 `g09:` 命名空間。

本設計區分為：

- 物件類別，例如 `cap:Cup`、`cap:Knife`、`cap:Fork`、`cap:Plate`、`cap:ToyBlock`、`cap:Basket`
- 任務角色類別，例如 `cap:TargetObject`、`cap:ReferenceObject`、`cap:ContainerTarget`、`cap:CollectableObject`
- affordance 類別，例如 `cap:GraspingAffordance`、`cap:SupportAffordance`、`cap:ContainmentAffordance`、`cap:StackabilityAffordance`
- 物件個體，例如 `g09:blueCup01`、`g09:pinkCup01`、`g09:block01`

`cap:GraspableObject` 使用 OWL 等價類定義：

- `cap:PhysicalObject`
- 且 `cap:hasAffordance some cap:GraspingAffordance`

因此 graspability 不是手動直接標註，而是透過推論得到。

## 3. 物件與 affordance 對應

| 物件 | 類型 | 角色 | affordance | 是否可抓取 |
| --- | --- | --- | --- | --- |
| `blueCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | 是 |
| `pinkCup01` | `cap:Cup` | `cap:TargetObject` | grasping, stackability | 是 |
| `knife01` | `cap:Knife` | `cap:TargetObject` | grasping | 是 |
| `fork01` | `cap:Fork` | `cap:TargetObject` | grasping | 是 |
| `plate01` | `cap:Plate` | `cap:ReferenceObject` | support | 否 |
| `block01` | `cap:ToyBlock` | `cap:CollectableObject` | grasping | 是 |
| `basket01` | `cap:Basket` | `cap:ContainerTarget` | containment | 否 |

## 4. 命名空間說明

- 共用課程詞彙：`cap:` = `https://hcis.io/ontology/aicapstone/2026/`
- 第 09 組詞彙：`g09:` = `https://hcis.io/ontology/aicapstone/2026/group09/`

第 09 組本體會把 local 物件個體、affordance 個體與 gripper 個體都放在 `g09:` 下；共用類別與屬性則維持在 `cap:` 下。

## 5. 查詢流程

SPARQL 查詢位於 `queries/graspable_objects.rq`，應該在包含共用課程本體與第 09 組本體的推論圖上執行。

這個查詢會回傳所有型別為 `cap:GraspableObject` 的個體，並附帶可選的 label 與 task role。

## 6. 預期結果

預期會被推論為可抓取物件的有：

- `g09:blueCup01`
- `g09:pinkCup01`
- `g09:knife01`
- `g09:fork01`
- `g09:block01`

`plate01` 與 `basket01` 不應出現在 graspable-object 的結果中，因為它們是用 support / containment affordance 來建模，而不是 grasping affordance。

## 7. 推論輸出

`ontology/inferred-results.ttl` 會記錄上述五個物件的 `cap:GraspableObject` 推論結果。
它代表推論後的 graph export，可直接用於查詢驗證。

可重現流程：執行 `python src/reason_and_export.py`（需要 `requirements.txt` 裡的 `rdflib`），即可重新產生 `ontology/inferred-results.ttl` 與 `results/graspable_objects_output.txt`。

## 8. 推理機制與驗證

本作業接受 RDFLib-based workflow，但前提是必須清楚說明額外的推理機制。
本提交使用一個輕量級 Python materializer：它會先檢查每個物件是否為 `cap:PhysicalObject`，再檢查該物件是否有 `cap:hasAffordance` 指向一個型別為 `cap:GraspingAffordance` 的個體；當兩個條件同時成立時，就會在推論圖中加入 `cap:GraspableObject`。

驗證步驟：

- 重新執行 `python src/reason_and_export.py`
- 檢查 `ontology/inferred-results.ttl`，確認是否有五個推論成員
- 檢查 `results/graspable_objects_output.txt`，確認 SPARQL 查詢結果是否一致
- 如果有使用 Widoco，則檢查 `docs/group09/doc/index-en.html` 是否已正確產生 ontology 文件

## 9. 侷限性

這份提交的範圍是基礎任務，不包含進階延伸任務、額外 validation shapes，或圖像截圖。
如果課程流程要求特定 reasoner 的輸出，仍可依相同 ontology 與查詢結構重新產生 `inferred-results.ttl`。

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
