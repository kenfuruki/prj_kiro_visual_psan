       IDENTIFICATION DIVISION.
       PROGRAM-ID. QB71RC.
      *---------------------------------------------------------
      * 職域＆e-Auto：料率TBL保持プログラム
      * ※6文字IDかつ末尾2文字アルファベット
      *---------------------------------------------------------
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      * VCOPY句で料率マスター値を展開
           COPY VB73C100.
       LINKAGE SECTION.
       01  LK-計算基本項目.
           05  LK-基本保険料       PIC 9(7).
           05  LK-特約保険料       PIC 9(7).
       PROCEDURE DIVISION USING LK-計算基本項目.
       RATE-GET-ROUTINE.
      * VCOPYで展開されたテーブルを検索して値をセットする想定
           MOVE 10000 TO LK-基本保険料.
           EXIT PROGRAM.
