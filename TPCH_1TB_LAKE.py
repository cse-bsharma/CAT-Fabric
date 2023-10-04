sql_queries = ["""select /*Q1*/ count_big(*) from (SELECT L_RETURNFLAG
	,L_LINESTATUS
	,SUM(L_QUANTITY) AS SUM_QTY
	,SUM(L_EXTENDEDPRICE) AS SUM_BASE_PRICE
	,SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS SUM_DISC_PRICE
	,SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT) * (1 + L_TAX)) AS SUM_CHARGE
	,AVG(L_QUANTITY) AS AVG_QTY
	,AVG(L_EXTENDEDPRICE) AS AVG_PRICE
	,AVG(L_DISCOUNT) AS AVG_DISC
	,COUNT(*) AS COUNT_ORDER
FROM tpch_lineitem
WHERE L_SHIPDATE <= dateadd(dd, - 90, cast('1998-12-01' AS DATE))
GROUP BY L_RETURNFLAG
	,L_LINESTATUS)dt""",
"""select/*Q2*/ count_big(*) from (
SELECT TOP 100 S_ACCTBAL
	,S_NAME
	,N_NAME
	,P_PARTKEY
	,P_MFGR
	,S_ADDRESS
	,S_PHONE
	,S_COMMENT
FROM tpch_part
	,tpch_supplier
	,tpch_partsupp
	,tpch_nation
	,tpch_region
WHERE P_PARTKEY = PS_PARTKEY
	AND S_SUPPKEY = PS_SUPPKEY
	AND P_SIZE = 15
	AND P_TYPE LIKE '%%BRASS'
	AND S_NATIONKEY = N_NATIONKEY
	AND N_REGIONKEY = R_REGIONKEY
	AND R_NAME = 'EUROPE'
	AND PS_SUPPLYCOST = (
		SELECT MIN(PS_SUPPLYCOST)
		FROM tpch_partsupp
			,tpch_supplier
			,tpch_nation
			,tpch_region
		WHERE P_PARTKEY = PS_PARTKEY
			AND S_SUPPKEY = PS_SUPPKEY
			AND S_NATIONKEY = N_NATIONKEY
			AND N_REGIONKEY = R_REGIONKEY
			AND R_NAME = 'EUROPE'
		))dt""",
"""select /*Q3*/count_big(*) from (
SELECT TOP 10 L_ORDERKEY
	,SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE
	,O_ORDERDATE
	,O_SHIPPRIORITY
FROM tpch_customer
	,tpch_orders
	,tpch_lineitem
WHERE C_MKTSEGMENT = 'BUILDING'
	AND C_CUSTKEY = O_CUSTKEY
	AND L_ORDERKEY = O_ORDERKEY
	AND O_ORDERDATE < '1995-03-15'
	AND L_SHIPDATE > '1995-03-15'
GROUP BY L_ORDERKEY
	,O_ORDERDATE
	,O_SHIPPRIORITY
)dt""",
"""select count_big(*) from(
SELECT /*Q4*/O_ORDERPRIORITY
	,COUNT(*) AS ORDER_COUNT
FROM tpch_orders
WHERE O_ORDERDATE >= '1993-07-01'
	AND O_ORDERDATE < dateadd(mm, 3, cast('1993-07-01' AS DATE))
	AND EXISTS (
		SELECT *
		FROM tpch_lineitem
		WHERE L_ORDERKEY = O_ORDERKEY
			AND L_COMMITDATE < L_RECEIPTDATE
		)
GROUP BY O_ORDERPRIORITY
)dt""",
"""select/*Q5*/count_big(*) from (
SELECT N_NAME
	,SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE
FROM tpch_customer
	,tpch_orders
	,tpch_lineitem
	,tpch_supplier
	,tpch_nation
	,tpch_region
WHERE C_CUSTKEY = O_CUSTKEY
	AND L_ORDERKEY = O_ORDERKEY
	AND L_SUPPKEY = S_SUPPKEY
	AND C_NATIONKEY = S_NATIONKEY
	AND S_NATIONKEY = N_NATIONKEY
	AND N_REGIONKEY = R_REGIONKEY
	AND R_NAME = 'ASIA'
	AND O_ORDERDATE >= '1994-01-01'
	AND O_ORDERDATE < DATEADD(YY, 1, cast('1994-01-01' AS DATE))
GROUP BY N_NAME
)dt""",
"""select  /*Q6*/count_big(*) from (
SELECT SUM(L_EXTENDEDPRICE * L_DISCOUNT) AS REVENUE
FROM tpch_lineitem
WHERE L_SHIPDATE >= '1994-01-01'
	AND L_SHIPDATE < dateadd(yy, 1, cast('1994-01-01' AS DATE))
	AND L_DISCOUNT BETWEEN .06 - 0.01
		AND .06 + 0.01
	AND L_QUANTITY < 24)dt""",
"""select  /*Q7*/count_big(*) from (
SELECT SUPP_NATION
	,CUST_NATION
	,L_YEAR
	,SUM(VOLUME) AS REVENUE
FROM (
	SELECT N1.N_NAME AS SUPP_NATION
		,N2.N_NAME AS CUST_NATION
		,datepart(yy, L_SHIPDATE) AS L_YEAR
		,L_EXTENDEDPRICE * (1 - L_DISCOUNT) AS VOLUME
	FROM tpch_supplier
		,tpch_lineitem
		,tpch_orders
		,tpch_customer
		,tpch_nation N1
		,tpch_nation N2
	WHERE S_SUPPKEY = L_SUPPKEY
		AND O_ORDERKEY = L_ORDERKEY
		AND C_CUSTKEY = O_CUSTKEY
		AND S_NATIONKEY = N1.N_NATIONKEY
		AND C_NATIONKEY = N2.N_NATIONKEY
		AND (
			(
				N1.N_NAME = 'FRANCE'
				AND N2.N_NAME = 'GERMANY'
				)
			OR (
				N1.N_NAME = 'GERMANY'
				AND N2.N_NAME = 'FRANCE'
				)
			)
		AND L_SHIPDATE BETWEEN '1995-01-01'
			AND '1996-12-31'
	) AS SHIPPING
GROUP BY SUPP_NATION
	,CUST_NATION
	,L_YEAR)dt""",
"""select  /*Q8*/count_big(*) from (
SELECT O_YEAR
	,SUM(CASE 
			WHEN NATION = 'BRAZIL'
				THEN VOLUME
			ELSE 0
			END) / SUM(VOLUME) AS MKT_SHARE
FROM (
	SELECT datepart(yy, O_ORDERDATE) AS O_YEAR
		,L_EXTENDEDPRICE * (1 - L_DISCOUNT) AS VOLUME
		,N2.N_NAME AS NATION
	FROM tpch_part
		,tpch_supplier
		,tpch_lineitem
		,tpch_orders
		,tpch_customer
		,tpch_nation N1
		,tpch_nation N2
		,tpch_region
	WHERE P_PARTKEY = L_PARTKEY
		AND S_SUPPKEY = L_SUPPKEY
		AND L_ORDERKEY = O_ORDERKEY
		AND O_CUSTKEY = C_CUSTKEY
		AND C_NATIONKEY = N1.N_NATIONKEY
		AND N1.N_REGIONKEY = R_REGIONKEY
		AND R_NAME = 'AMERICA'
		AND S_NATIONKEY = N2.N_NATIONKEY
		AND O_ORDERDATE BETWEEN '1995-01-01'
			AND '1996-12-31'
		AND P_TYPE = 'ECONOMY ANODIZED STEEL'
	) AS ALL_NATIONS
GROUP BY O_YEAR
)dt""",
"""select  /*Q9*/count_big(*) from (
SELECT NATION
	,O_YEAR
	,SUM(AMOUNT) AS SUM_PROFIT
FROM (
	SELECT N_NAME AS NATION
		,datepart(yy, O_ORDERDATE) AS O_YEAR
		,L_EXTENDEDPRICE * (1 - L_DISCOUNT) - PS_SUPPLYCOST * L_QUANTITY AS AMOUNT
	FROM tpch_part
		,tpch_supplier
		,tpch_lineitem
		,tpch_partsupp
		,tpch_orders
		,tpch_nation
	WHERE S_SUPPKEY = L_SUPPKEY
		AND PS_SUPPKEY = L_SUPPKEY
		AND PS_PARTKEY = L_PARTKEY
		AND P_PARTKEY = L_PARTKEY
		AND O_ORDERKEY = L_ORDERKEY
		AND S_NATIONKEY = N_NATIONKEY
		AND P_NAME LIKE '%%green%%'
	) AS PROFIT
GROUP BY NATION
	,O_YEAR
)dt""",
"""select  /*Q10*/count_big(*) from (
SELECT TOP 20 C_CUSTKEY
	,C_NAME
	,SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE
	,C_ACCTBAL
	,N_NAME
	,C_ADDRESS
	,C_PHONE
	,C_COMMENT
FROM tpch_customer
	,tpch_orders
	,tpch_lineitem
	,tpch_nation
WHERE C_CUSTKEY = O_CUSTKEY
	AND L_ORDERKEY = O_ORDERKEY
	AND O_ORDERDATE >= '1993-10-01'
	AND O_ORDERDATE < dateadd(mm, 3, cast('1993-10-01' AS DATE))
	AND L_RETURNFLAG = 'R'
	AND C_NATIONKEY = N_NATIONKEY
GROUP BY C_CUSTKEY
	,C_NAME
	,C_ACCTBAL
	,C_PHONE
	,N_NAME
	,C_ADDRESS
	,C_COMMENT
)dt""",
"""select /*Q11*/count_big(*) from (
SELECT PS_PARTKEY
	,SUM(PS_SUPPLYCOST * PS_AVAILQTY) AS VALUE
FROM tpch_partsupp
	,tpch_supplier
	,tpch_nation
WHERE PS_SUPPKEY = S_SUPPKEY
	AND S_NATIONKEY = N_NATIONKEY
	AND N_NAME = 'GERMANY'
GROUP BY PS_PARTKEY
HAVING SUM(PS_SUPPLYCOST * PS_AVAILQTY) > (
		SELECT SUM(PS_SUPPLYCOST * PS_AVAILQTY) * 0.0001000000
		FROM tpch_partsupp
			,tpch_supplier
			,tpch_nation
		WHERE PS_SUPPKEY = S_SUPPKEY
			AND S_NATIONKEY = N_NATIONKEY
			AND N_NAME = 'GERMANY'
		))dt""",
"""select  /*Q12*/count_big(*) from (
SELECT L_SHIPMODE
	,SUM(CASE 
			WHEN O_ORDERPRIORITY = '1-URGENT'
				OR O_ORDERPRIORITY = '2-HIGH'
				THEN 1
			ELSE 0
			END) AS HIGH_LINE_COUNT
	,SUM(CASE 
			WHEN O_ORDERPRIORITY <> '1-URGENT'
				AND O_ORDERPRIORITY <> '2-HIGH'
				THEN 1
			ELSE 0
			END) AS LOW_LINE_COUNT
FROM tpch_orders
	,tpch_lineitem
WHERE O_ORDERKEY = L_ORDERKEY
	AND L_SHIPMODE IN (
		'MAIL'
		,'SHIP'
		)
	AND L_COMMITDATE < L_RECEIPTDATE
	AND L_SHIPDATE < L_COMMITDATE
	AND L_RECEIPTDATE >= '1994-01-01'
	AND L_RECEIPTDATE < dateadd(mm, 1, cast('1995-09-01' AS DATE))
GROUP BY L_SHIPMODE
)dt""",
"""select  /*Q13*/count_big(*) from (
SELECT C_COUNT
	,COUNT(*) AS CUSTDIST
FROM (
	SELECT C_CUSTKEY
		,COUNT(O_ORDERKEY)
	FROM tpch_customer
	LEFT OUTER JOIN tpch_orders ON C_CUSTKEY = O_CUSTKEY
		AND O_COMMENT NOT LIKE '%%special%%requests%%'
	GROUP BY C_CUSTKEY
	) AS C_ORDERS(C_CUSTKEY, C_COUNT)
GROUP BY C_COUNT
)dt""",
"""select  /*Q14*/count_big(*) from (
SELECT 100.00 * SUM(CASE 
			WHEN P_TYPE LIKE 'PROMO%%'
				THEN L_EXTENDEDPRICE * (1 - L_DISCOUNT)
			ELSE 0
			END) / SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS PROMO_REVENUE
FROM tpch_lineitem
	,tpch_part
WHERE L_PARTKEY = P_PARTKEY
	AND L_SHIPDATE >= '1995-09-01'
	AND L_SHIPDATE < dateadd(mm, 1, '1995-09-01'))dt""",
"""select  /*Q15*/count_big(*) from (
SELECT S_SUPPKEY
	,S_NAME
	,S_ADDRESS
	,S_PHONE
	,MAX_TOTAL_REVENUE
FROM tpch_supplier
	,(select SUPPLIER_NO, MAX(TOTAL_REVENUE) as MAX_TOTAL_REVENUE from (
		SELECT L_SUPPKEY as SUPPLIER_NO
			,SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) TOTAL_REVENUE
		FROM tpch_lineitem
		WHERE L_SHIPDATE >= '1996-01-01'
			AND L_SHIPDATE < dateadd(mm, 3, cast('1996-01-01' AS DATE))
		GROUP BY L_SUPPKEY
		) dt group by SUPPLIER_NO) as REVENUE
WHERE S_SUPPKEY = SUPPLIER_NO
)dt""",
"""select  /*Q16*/count_big(*) from (
SELECT P_BRAND
	,P_TYPE
	,P_SIZE
	,COUNT(DISTINCT PS_SUPPKEY) AS SUPPLIER_CNT
FROM tpch_partsupp
	,tpch_part
WHERE P_PARTKEY = PS_PARTKEY
	AND P_BRAND <> 'Brand#45'
	AND P_TYPE NOT LIKE 'MEDIUM POLISHED%%'
	AND P_SIZE IN (
		49
		,14
		,23
		,45
		,19
		,3
		,36
		,9
		)
	AND PS_SUPPKEY NOT IN (
		SELECT S_SUPPKEY
		FROM tpch_supplier
		WHERE S_COMMENT LIKE '%%Customer%%Complaints%%'
		)
GROUP BY P_BRAND
	,P_TYPE
	,P_SIZE
)dt""",
"""select  /*Q17*/count_big(*) from (
SELECT SUM(L_EXTENDEDPRICE) / 7.0 AS AVG_YEARLY
FROM tpch_lineitem
	,tpch_part
WHERE P_PARTKEY = L_PARTKEY
	AND P_BRAND = 'Brand#23'
	AND P_CONTAINER = 'MED BOX'
	AND L_QUANTITY < (
		SELECT 0.2 * AVG(L_QUANTITY)
		FROM tpch_lineitem
		WHERE L_PARTKEY = P_PARTKEY
		))dt""",
"""select  /*Q18*/count_big(*) from (
SELECT TOP 100 C_NAME
	,C_CUSTKEY
	,O_ORDERKEY
	,O_ORDERDATE
	,O_TOTALPRICE
	,SUM(L_QUANTITY) as sum_q
FROM tpch_customer
	,tpch_orders
	,tpch_lineitem
WHERE O_ORDERKEY IN (
		SELECT L_ORDERKEY
		FROM tpch_lineitem
		GROUP BY L_ORDERKEY
		HAVING SUM(L_QUANTITY) > 300
		)
	AND C_CUSTKEY = O_CUSTKEY
	AND O_ORDERKEY = L_ORDERKEY
GROUP BY C_NAME
	,C_CUSTKEY
	,O_ORDERKEY
	,O_ORDERDATE
	,O_TOTALPRICE
)dt""",
"""select  /*Q19*/count_big(*) from (
SELECT SUM(L_EXTENDEDPRICE * (1 - L_DISCOUNT)) AS REVENUE
FROM tpch_lineitem
	,tpch_part
WHERE (
		P_PARTKEY = L_PARTKEY
		AND P_BRAND = 'Brand#12'
		AND P_CONTAINER IN (
			'SM CASE'
			,'SM BOX'
			,'SM PACK'
			,'SM PKG'
			)
		AND L_QUANTITY >= 1
		AND L_QUANTITY <= 1 + 10
		AND P_SIZE BETWEEN 1
			AND 5
		AND L_SHIPMODE IN (
			'AIR'
			,'AIR REG'
			)
		AND L_SHIPINSTRUCT = 'DELIVER IN PERSON'
		)
	OR (
		P_PARTKEY = L_PARTKEY
		AND P_BRAND = 'Brand#23'
		AND P_CONTAINER IN (
			'MED BAG'
			,'MED BOX'
			,'MED PKG'
			,'MED PACK'
			)
		AND L_QUANTITY >= 10
		AND L_QUANTITY <= 10 + 10
		AND P_SIZE BETWEEN 1
			AND 10
		AND L_SHIPMODE IN (
			'AIR'
			,'AIR REG'
			)
		AND L_SHIPINSTRUCT = 'DELIVER IN PERSON'
		)
	OR (
		P_PARTKEY = L_PARTKEY
		AND P_BRAND = 'Brand#34'
		AND P_CONTAINER IN (
			'LG CASE'
			,'LG BOX'
			,'LG PACK'
			,'LG PKG'
			)
		AND L_QUANTITY >= 20
		AND L_QUANTITY <= 20 + 10
		AND P_SIZE BETWEEN 1
			AND 15
		AND L_SHIPMODE IN (
			'AIR'
			,'AIR REG'
			)
		AND L_SHIPINSTRUCT = 'DELIVER IN PERSON'
		))dt""",
"""select  /*Q20*/count_big(*) from (
SELECT S_NAME
	,S_ADDRESS
FROM tpch_supplier
	,tpch_nation
WHERE S_SUPPKEY IN (
		SELECT PS_SUPPKEY
		FROM tpch_partsupp
		WHERE PS_PARTKEY IN (
				SELECT P_PARTKEY
				FROM tpch_part
				WHERE P_NAME LIKE 'forest%%'
				)
			AND PS_AVAILQTY > (
				SELECT 0.5 * sum(L_QUANTITY)
				FROM tpch_lineitem
				WHERE L_PARTKEY = PS_PARTKEY
					AND L_SUPPKEY = PS_SUPPKEY
					AND L_SHIPDATE >= '1994-01-01'
					AND L_SHIPDATE < dateadd(yy, 1, '1994-01-01')
				)
		)
	AND S_NATIONKEY = N_NATIONKEY
	AND N_NAME = 'CANADA'
)dt""",
"""select  /*Q21*/count_big(*) from (
SELECT TOP 100 S_NAME
	,COUNT(*) AS NUMWAIT
FROM tpch_supplier
	,tpch_lineitem L1
	,tpch_orders
	,tpch_nation
WHERE S_SUPPKEY = L1.L_SUPPKEY
	AND O_ORDERKEY = L1.L_ORDERKEY
	AND O_ORDERSTATUS = 'F'
	AND L1.L_RECEIPTDATE > L1.L_COMMITDATE
	AND EXISTS (
		SELECT *
		FROM tpch_lineitem L2
		WHERE L2.L_ORDERKEY = L1.L_ORDERKEY
			AND L2.L_SUPPKEY <> L1.L_SUPPKEY
		)
	AND NOT EXISTS (
		SELECT *
		FROM tpch_lineitem L3
		WHERE L3.L_ORDERKEY = L1.L_ORDERKEY
			AND L3.L_SUPPKEY <> L1.L_SUPPKEY
			AND L3.L_RECEIPTDATE > L3.L_COMMITDATE
		)
	AND S_NATIONKEY = N_NATIONKEY
	AND N_NAME = 'SAUDI ARABIA'
GROUP BY S_NAME
)dt""",
"""select  /*Q22*/count_big(*) from (
SELECT CNTRYCODE
	,COUNT(*) AS NUMCUST
	,SUM(C_ACCTBAL) AS TOTACCTBAL
FROM (
	SELECT SUBSTRING(C_PHONE, 1, 2) AS CNTRYCODE
		,C_ACCTBAL
	FROM tpch_customer
	WHERE SUBSTRING(C_PHONE, 1, 2) IN (
			'13'
			,'31'
			,'23'
			,'29'
			,'30'
			,'18'
			,'17'
			)
		AND C_ACCTBAL > (
			SELECT AVG(C_ACCTBAL)
			FROM tpch_customer
			WHERE C_ACCTBAL > 0.00
				AND SUBSTRING(C_PHONE, 1, 2) IN (
					'13'
					,'31'
					,'23'
					,'29'
					,'30'
					,'18'
					,'17'
					)
			)
		AND NOT EXISTS (
			SELECT *
			FROM tpch_orders
			WHERE O_CUSTKEY = C_CUSTKEY
			)
	) AS CUSTSALE
GROUP BY CNTRYCODE
)dt"""]
