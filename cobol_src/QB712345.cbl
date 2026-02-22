       IDENTIFICATION DIVISION.
       PROGRAM-ID. QB712345.
      *---------------------------------------------------------
      * 自火超更新・帳票バッチ共通：特約計算サブモジュール
      *---------------------------------------------------------
       DATA DIVISION.
       LINKAGE SECTION.
       01  LK-計算基本項目.
           05  LK-基本保険料       PIC 9(7).
           05  LK-特約保険料       PIC 9(7).
       PROCEDURE DIVISION USING LK-計算基本項目.
       SUB-ROUTINE.
      * 1. 料率TBL保持プログラムから最新の料率を取得
           CALL 'QB71RC' USING LK-計算基本項目.
      * 2. 取得した料率を基に特約保険料を算出 (ダミー処理)
           COMPUTE LK-特約保険料 = LK-基本保険料 * 1.5.
           EXIT PROGRAM.
