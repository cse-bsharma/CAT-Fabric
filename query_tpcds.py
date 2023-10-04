sql_queries = [
    """SELECT /*fabric1*/Count(*) 
FROM   tpcds.store_sales, 
       tpcds.household_demographics, 
       tpcds.time_dim, 
       tpcds.store 
WHERE  ss_sold_time_sk = time_dim.t_time_sk 
       AND ss_hdemo_sk = household_demographics.hd_demo_sk 
       AND ss_store_sk = s_store_sk 
       AND time_dim.t_hour = 15 
       AND time_dim.t_minute >= 30 
       AND household_demographics.hd_dep_count = 7 
       AND store.s_store_name = 'ese' ;""",
    """select /*fabric2*/ count_big(*) from
(
SELECT 
         i_item_id , 
         i_item_desc , 
         i_current_price 
FROM     tpcds.item, 
         tpcds.inventory, 
         tpcds.date_dim, 
         tpcds.catalog_sales 
WHERE    i_current_price BETWEEN 20 AND      20 + 30 
AND      inv_item_sk = i_item_sk 
AND      d_date_sk=inv_date_sk 
AND      d_date BETWEEN '1999-03-06' AND      
                  DATEADD(DAY,90,'1999-03-06') 
AND      i_manufact_id IN (843,815,850,840) 
AND      inv_quantity_on_hand BETWEEN 100 AND      500 
AND      cs_item_sk = i_item_sk 
GROUP BY i_item_id, 
         i_item_desc, 
         i_current_price 
)ab""",
    """select /*fabric3 */count_big(*) from (
SELECT 
         i_item_id , 
         i_item_desc , 
         i_category , 
         i_class , 
         i_current_price , 
         Sum(cs_ext_sales_price)                                                              AS itemrevenue ,
         Sum(cs_ext_sales_price)*100/Sum(Sum(cs_ext_sales_price)) OVER (partition BY i_class) AS revenueratio
FROM     tpcds.catalog_sales , 
         tpcds.item , 
         tpcds.date_dim 
WHERE    cs_item_sk = i_item_sk 
AND      i_category IN ('Children', 
                        'Women', 
                        'Electronics') 
AND      cs_sold_date_sk = d_date_sk 
AND      d_date BETWEEN '2001-02-03'  AND     
                  DATEADD(DAY,30,'2001-02-03')
GROUP BY i_item_id , 
         i_item_desc , 
         i_category , 
         i_class , 
         i_current_price  )ab""",
    """select /*fabric4 */count_big(*) from (SELECT i_item_id, 
               Avg(cs_quantity)    agg1, 
               Avg(cs_list_price)  agg2, 
               Avg(cs_coupon_amt)  agg3, 
               Avg(cs_sales_price) agg4 
FROM   tpcds.catalog_sales, 
       tpcds.customer_demographics, 
       tpcds.date_dim, 
       tpcds.item, 
       tpcds.promotion 
WHERE  cs_sold_date_sk = d_date_sk 
       AND cs_item_sk = i_item_sk 
       AND cs_bill_cdemo_sk = cd_demo_sk 
       AND cs_promo_sk = p_promo_sk 
       AND cd_gender = 'F' 
       AND cd_marital_status = 'W' 
       AND cd_education_status = 'Secondary' 
       AND ( p_channel_email = 'N' 
              OR p_channel_event = 'N' ) 
       AND d_year = 2000 
GROUP  BY i_item_id )ab""",
    """select /*fabric5 */count_big(*) from
(
SELECT 
         i_item_id , 
         i_item_desc , 
         i_current_price 
FROM     tpcds.item, 
         tpcds.inventory, 
         tpcds.date_dim, 
         tpcds.catalog_sales 
WHERE    i_current_price BETWEEN 20 AND      20 + 30 
AND      inv_item_sk = i_item_sk 
AND      d_date_sk=inv_date_sk 
AND      d_date BETWEEN '1999-03-06' AND      
                  DATEADD(DAY,90,'1999-03-06') 
AND      i_manufact_id IN (843,815,850,840) 
AND      inv_quantity_on_hand BETWEEN 100 AND      500 
AND      cs_item_sk = i_item_sk 
GROUP BY i_item_id, 
         i_item_desc, 
         i_current_price 
)ab""",
"""select /*fabric6 */ count(*) from (
SELECT i_item_id, 
               Avg(cs_quantity)    agg1, 
               Avg(cs_list_price)  agg2, 
               Avg(cs_coupon_amt)  agg3, 
               Avg(cs_sales_price) agg4 
FROM   tpcds.catalog_sales, 
       tpcds.customer_demographics, 
       tpcds.date_dim, 
       tpcds.item, 
       tpcds.promotion 
WHERE  cs_sold_date_sk = d_date_sk 
       AND cs_item_sk = i_item_sk 
       AND cs_bill_cdemo_sk = cd_demo_sk 
       AND cs_promo_sk = p_promo_sk 
       AND cd_gender = 'F' 
       AND cd_marital_status = 'W' 
       AND cd_education_status = 'Secondary' 
       AND ( p_channel_email = 'N' 
              OR p_channel_event = 'N' ) 
       AND d_year = 2000 
GROUP  BY i_item_id 
)ab""",
"""select /*fabric7 */ count(*) from (
SELECT i_item_id, 
               s_state, 
               Grouping(s_state)   g_state, 
               Avg(ss_quantity)    agg1, 
               Avg(ss_list_price)  agg2, 
               Avg(ss_coupon_amt)  agg3, 
               Avg(ss_sales_price) agg4 
FROM   tpcds.store_sales, 
       tpcds.customer_demographics, 
       tpcds.date_dim, 
       tpcds.store, 
       tpcds.item 
WHERE  ss_sold_date_sk = d_date_sk 
       AND ss_item_sk = i_item_sk 
       AND ss_store_sk = s_store_sk 
       AND ss_cdemo_sk = cd_demo_sk 
       AND cd_gender = 'M' 
       AND cd_marital_status = 'D' 
       AND cd_education_status = 'College' 
       AND d_year = 2000 
       AND s_state IN ( 'TN', 'TN', 'TN', 'TN', 
                        'TN', 'TN' ) 
GROUP  BY rollup ( i_item_id, s_state ) 
)ab""",
"""select /*fabric8 */ count(*) from (
SELECT i_item_id, 
               i_item_desc, 
               s_store_id, 
               s_store_name, 
               Avg(ss_quantity)        AS store_sales_quantity, 
               Avg(sr_return_quantity) AS store_returns_quantity, 
               Avg(cs_quantity)        AS catalog_sales_quantity 
FROM   tpcds.store_sales, 
       tpcds.store_returns, 
       tpcds.catalog_sales, 
       tpcds.date_dim d1, 
       tpcds.date_dim d2, 
       tpcds.date_dim d3, 
       tpcds.store, 
       tpcds.item 
WHERE  d1.d_moy = 4 
       AND d1.d_year = 1998 
       AND d1.d_date_sk = ss_sold_date_sk 
       AND i_item_sk = ss_item_sk 
       AND s_store_sk = ss_store_sk 
       AND ss_customer_sk = sr_customer_sk 
       AND ss_item_sk = sr_item_sk 
       AND ss_ticket_number = sr_ticket_number 
       AND sr_returned_date_sk = d2.d_date_sk 
       AND d2.d_moy BETWEEN 4 AND 4 + 3 
       AND d2.d_year = 1998 
       AND sr_customer_sk = cs_bill_customer_sk 
       AND sr_item_sk = cs_item_sk 
       AND cs_sold_date_sk = d3.d_date_sk 
       AND d3.d_year IN ( 1998, 1998 + 1, 1998 + 2 ) 
GROUP  BY i_item_id, 
          i_item_desc, 
          s_store_id, 
          s_store_name 
)ab""",
"""
SELECT /*fabric9 */ Count(*) 
FROM   (SELECT DISTINCT c_last_name, 
                        c_first_name, 
                        d_date 
        FROM   tpcds.store_sales, 
               tpcds.date_dim, 
               tpcds.customer 
        WHERE  store_sales.ss_sold_date_sk = date_dim.d_date_sk 
               AND store_sales.ss_customer_sk = customer.c_customer_sk 
               AND d_month_seq BETWEEN 1188 AND 1188 + 11 
        INTERSECT 
        SELECT DISTINCT c_last_name, 
                        c_first_name, 
                        d_date 
        FROM   tpcds.catalog_sales, 
               tpcds.date_dim, 
               tpcds.customer 
        WHERE  catalog_sales.cs_sold_date_sk = date_dim.d_date_sk 
               AND catalog_sales.cs_bill_customer_sk = customer.c_customer_sk 
               AND d_month_seq BETWEEN 1188 AND 1188 + 11 
        INTERSECT 
        SELECT DISTINCT c_last_name, 
                        c_first_name, 
                        d_date 
        FROM   tpcds.web_sales, 
               tpcds.date_dim, 
               tpcds.customer 
        WHERE  web_sales.ws_sold_date_sk = date_dim.d_date_sk 
               AND web_sales.ws_bill_customer_sk = customer.c_customer_sk 
               AND d_month_seq BETWEEN 1188 AND 1188 + 11) hot_cust """,
"""select /*fabric10*/ count(*) from (
SELECT
                w_state , 
                i_item_id , 
                Sum( 
                CASE 
                                WHEN ( 
                                                               Cast(d_date AS DATE) < Cast ('2002-06-01' AS DATE)) THEN cs_sales_price - COALESCE(cr_refunded_cash,0) 
                                ELSE 0 
                END) AS sales_before , 
                Sum( 
                CASE 
                                WHEN ( 
                                                                Cast(d_date AS DATE) >= Cast ('2002-06-01' AS DATE)) THEN cs_sales_price - COALESCE(cr_refunded_cash,0) 
                                ELSE 0 
                END) AS sales_after 
FROM            tpcds.catalog_sales 
LEFT OUTER JOIN tpcds.catalog_returns 
ON              ( 
                                cs_order_number = cr_order_number 
                AND             cs_item_sk = cr_item_sk) , 
                tpcds.warehouse , 
                tpcds.item , 
                tpcds.date_dim 
WHERE           i_current_price BETWEEN 0.99 AND             1.49 
AND             i_item_sk = cs_item_sk 
AND             cs_warehouse_sk = w_warehouse_sk 
AND             cs_sold_date_sk = d_date_sk 
AND             d_date BETWEEN DATEADD(DAY,-30,'2002-06-01')  AND             
                                DATEADD (DAY,30,'2002-06-01')
GROUP BY        w_state, 
                i_item_id )ab"""
]