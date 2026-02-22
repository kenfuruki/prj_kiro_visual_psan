       IDENTIFICATION DIVISION.
       PROGRAM-ID. QB7000.
      *---------------------------------------------------------
      * 火災＆超保険：メイン保険料計算処理 (現行チーム管轄)
      * ※現行の１キー＝１セグメント木構造のDBから
      * 基本データを取得する想定
      *---------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WS-計算基本項目.
           05  WS-基本保険料       PIC 9(7)  VALUE ZERO.
           05  WS-特約保険料       PIC 9(7)  VALUE ZERO.
       PROCEDURE DIVISION.
       MAIN-ROUTINE.
      * 1. 自火超更新・帳票バッチ共通のサブモジュールを呼出
           CALL 'QB712345' USING WS-計算基本項目.
      * 2. 職域＆e-Auto側の料率モジュールを直接呼出
           CALL 'QB71RC' USING WS-計算基本項目.
           STOP RUN.
