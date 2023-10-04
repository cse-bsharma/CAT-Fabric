sql_queries = [	 """select count_big(*) from(
SELECT
       L_RETURNFLAG,
       L_LINESTATUS,
       SUM(L_QUANTITY) AS SUM_QTY,
       SUM(L_EXTENDEDPRICE) AS SUM_BASE_PRICE,
       SUM(L_EXTENDEDPRICE * (1-L_DISCOUNT)) AS SUM_DISC_PRICE,
       SUM(L_EXTENDEDPRICE * (1-L_DISCOUNT) * (1+L_TAX)) AS SUM_CHARGE,
       AVG(L_QUANTITY) AS AVG_QTY,
       AVG(L_EXTENDEDPRICE) AS AVG_PRICE,
       AVG(L_DISCOUNT) AS AVG_DISC,
       COUNT_big(*) AS COUNT_ORDER
 FROM
       tpch.lineitem
 WHERE
       L_SHIPDATE <= dateadd(day, -90,'1998-12-01')
 GROUP BY
       L_RETURNFLAG,
       L_LINESTATUS
)ab""",
"""select count(*) from(
SELECT 
     S_ACCTBAL,
     S_NAME,
     N_NAME,
     P_PARTKEY,
     P_MFGR,
     S_ADDRESS,
     S_PHONE,
     S_COMMENT
 FROM tpch.part, tpch.supplier, tpch.partsupp, tpch.nation, tpch.region
WHERE
     P_PARTKEY = PS_PARTKEY
     AND S_SUPPKEY = PS_SUPPKEY
     AND P_SIZE = 15
     AND P_TYPE LIKE '%BRASS'
     AND S_NATIONKEY = N_NATIONKEY
     AND N_REGIONKEY = R_REGIONKEY
     AND R_NAME = 'EUROPE'
     AND PS_SUPPLYCOST = (
		SELECT
			MIN(PS_SUPPLYCOST)
		FROM
			tpch.partsupp,
			tpch.supplier,
			tpch.nation,
			tpch.region
		WHERE
			P_PARTKEY = PS_PARTKEY
			AND S_SUPPKEY = PS_SUPPKEY
			AND S_NATIONKEY = N_NATIONKEY
			AND N_REGIONKEY = R_REGIONKEY
			AND R_NAME = 'EUROPE'
     ))ab""",
"""SELECT COUNT_BIG(*) FROM(
SELECT 
     L_ORDERKEY,
     SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE,
     O_ORDERDATE,
     O_SHIPPRIORITY
 FROM  tpch.customer, tpch.orders, tpch.lineitem
WHERE C_MKTSEGMENT = 'BUILDING'
  AND C_CUSTKEY = O_CUSTKEY
  AND L_ORDERKEY = O_ORDERKEY
  AND O_ORDERDATE < '1995-3-15'
  AND L_SHIPDATE > '1995-3-15'
GROUP BY L_ORDERKEY, O_ORDERDATE, O_SHIPPRIORITY
)ab""",
"""select count_big(*) from(SELECT O_ORDERPRIORITY, COUNT(*) AS ORDER_COUNT
  FROM tpch.orders
 WHERE O_ORDERDATE >= '1993-07-01' 
   AND O_ORDERDATE <  DATEADD(MONTH,3,'1993-07-01')
   AND EXISTS (
      SELECT *
        FROM tpch.lineitem
       WHERE L_ORDERKEY = O_ORDERKEY
         AND L_COMMITDATE < L_RECEIPTDATE
     )
GROUP BY O_ORDERPRIORITY
)ab""",
"""select count_big(*) from(
SELECT N_NAME, SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE
  FROM tpch.customer, tpch.orders, tpch.lineitem, tpch.supplier, tpch.nation, tpch.region
 WHERE C_CUSTKEY = O_CUSTKEY
   AND L_ORDERKEY = O_ORDERKEY
   AND L_SUPPKEY = S_SUPPKEY
   AND C_NATIONKEY = S_NATIONKEY
   AND S_NATIONKEY = N_NATIONKEY
   AND N_REGIONKEY = R_REGIONKEY
   AND R_NAME = 'ASIA'
   AND O_ORDERDATE >= '1994-01-01'
   AND O_ORDERDATE < DATEADD(YEAR,1,'1994-01-01')
GROUP BY N_NAME
)ab""",
"""select count_big(*) from(
SELECT
     SUM(L_EXTENDEDPRICE * L_DISCOUNT) AS REVENUE
FROM
     tpch.lineitem
WHERE
     L_SHIPDATE >= '1994-01-01'
     AND L_SHIPDATE < DATEADD(YEAR,1,'1994-01-01')
     AND L_DISCOUNT BETWEEN .06 - 0.01 AND .06 + 0.010001
     AND L_QUANTITY < 24
)ab""",
"""select count_big(*) from(
SELECT
     SUPP_NATION,
     CUST_NATION,
     L_YEAR,
     SUM(VOLUME) AS REVENUE
FROM
     (
		SELECT
			N1.N_NAME AS SUPP_NATION,
			N2.N_NAME AS CUST_NATION,
			YEAR(L_SHIPDATE) AS L_YEAR,
			L_EXTENDEDPRICE * (1 - L_DISCOUNT) AS VOLUME
		FROM
			tpch.supplier,
			tpch.lineitem,
			tpch.orders,
			tpch.customer,
			tpch.nation N1,
			tpch.nation N2
		WHERE
			S_SUPPKEY = L_SUPPKEY
			AND O_ORDERKEY = L_ORDERKEY
			AND C_CUSTKEY = O_CUSTKEY
			AND S_NATIONKEY = N1.N_NATIONKEY
			AND C_NATIONKEY = N2.N_NATIONKEY
			AND (
				(N1.N_NAME = 'FRANCE' AND N2.N_NAME = 'GERMANY')
				OR (N1.N_NAME = 'GERMANY' AND N2.N_NAME = 'FRANCE')
			)
			AND L_SHIPDATE BETWEEN '1995-01-01' AND  '1996-12-31'
     ) AS SHIPPING
GROUP BY
     SUPP_NATION,
     CUST_NATION,
     L_YEAR
)ab""",
"""select count_big(*) from(
SELECT
     O_YEAR,
     SUM(CASE
		WHEN NATION = 'BRAZIL' THEN VOLUME
		ELSE 0
     END) / SUM(VOLUME) AS MKT_SHARE
FROM
     (
		SELECT
			YEAR(O_ORDERDATE) AS O_YEAR,
			L_EXTENDEDPRICE * (1 - L_DISCOUNT) AS VOLUME,
			N2.N_NAME AS NATION
		FROM
			tpch.part,
			tpch.supplier,
			tpch.lineitem,
			tpch.orders,
			tpch.customer,
			tpch.nation N1,
			tpch.nation N2,
			tpch.region
		WHERE
			P_PARTKEY = L_PARTKEY
			AND S_SUPPKEY = L_SUPPKEY
			AND L_ORDERKEY = O_ORDERKEY
			AND O_CUSTKEY = C_CUSTKEY
			AND C_NATIONKEY = N1.N_NATIONKEY
			AND N1.N_REGIONKEY = R_REGIONKEY
			AND R_NAME = 'AMERICA'
			AND S_NATIONKEY = N2.N_NATIONKEY
			AND O_ORDERDATE BETWEEN '1995-01-01' AND '1996-12-31'
			AND P_TYPE = 'ECONOMY ANODIZED STEEL'
     ) AS ALL_NATIONS
GROUP BY
     O_YEAR
)ab""",
"""
select count_big(*) from(
SELECT
     NATION,
     O_YEAR,
     SUM(AMOUNT) AS SUM_PROFIT
FROM
     (
		SELECT
			N_NAME AS NATION,
			YEAR(O_ORDERDATE) AS O_YEAR,
			L_EXTENDEDPRICE * (1 - L_DISCOUNT) - PS_SUPPLYCOST * L_QUANTITY AS AMOUNT
		FROM
			tpch.part,
			tpch.supplier,
			tpch.lineitem,
			tpch.partsupp,
			tpch.orders,
			tpch.nation
		WHERE
			S_SUPPKEY = L_SUPPKEY
			AND PS_SUPPKEY = L_SUPPKEY
			AND PS_PARTKEY = L_PARTKEY
			AND P_PARTKEY = L_PARTKEY
			AND O_ORDERKEY = L_ORDERKEY
			AND S_NATIONKEY = N_NATIONKEY
			AND P_NAME LIKE '%GREEN%'
     ) AS PROFIT
GROUP BY
     NATION,
     O_YEAR
)ab""",
"""select count(*) from (SELECT 
     C_CUSTKEY,
     C_NAME,
     SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE,
     C_ACCTBAL,
     N_NAME,
     C_ADDRESS,
     C_PHONE,
     C_COMMENT
FROM
     tpch.customer,
     tpch.orders,
     tpch.lineitem,
     tpch.nation
WHERE
     C_CUSTKEY = O_CUSTKEY
     AND L_ORDERKEY = O_ORDERKEY
     AND O_ORDERDATE >= '1993-10-01'
     AND O_ORDERDATE < DATEADD(MONTH,3,'1993-10-01')
     AND L_RETURNFLAG = 'R'
     AND C_NATIONKEY = N_NATIONKEY
GROUP BY
     C_CUSTKEY,
     C_NAME,
     C_ACCTBAL,
     C_PHONE,
     N_NAME,
     C_ADDRESS,
     C_COMMENT
)ab"""]
