#Define the SQL queries you want to execute
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
    """select /*fabric2 */count_big(*) from (SELECT
         Count(DISTINCT cs_order_number) AS order_count,
         Sum(cs_ext_ship_cost)           AS total_shipping_cost ,
         Sum(cs_net_profit)              AS total_net_profit
FROM     tpcds.catalog_sales cs1 ,
         tpcds.date_dim ,
         tpcds.customer_address ,
         tpcds.call_center
WHERE    d_date BETWEEN '2002-3-01' AND      
                  DATEADD(DAY,60,'2002-3-01')
AND      cs1.cs_ship_date_sk = d_date_sk
AND      cs1.cs_ship_addr_sk = ca_address_sk
AND      ca_state = 'IA'
AND      cs1.cs_call_center_sk = cc_call_center_sk
AND      cc_county IN ('Williamson County',
                       'Williamson County',
                       'Williamson County',
                       'Williamson County',
                       'Williamson County' )
AND      EXISTS
         (
                SELECT *
                FROM   tpcds.catalog_sales cs2
                WHERE  cs1.cs_order_number = cs2.cs_order_number
                AND    cs1.cs_warehouse_sk <> cs2.cs_warehouse_sk)
AND      NOT EXISTS
         (
                SELECT *
                FROM   tpcds.catalog_returns cr1
                WHERE  cs1.cs_order_number = cr1.cr_order_number))ab""",
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
    """select /*fabric5 */count_big(*) from (
SELECT Avg(ss_quantity) as avg_ss_quantity, 
       Avg(ss_ext_sales_price) avg_ext_sales_price, 
       Avg(ss_ext_wholesale_cost) avg_ext_wholesale_cost, 
       Sum(ss_ext_wholesale_cost)  sum_ss_ext_wholesale_cost
FROM   tpcds.store_sales, 
       tpcds.store, 
       tpcds.customer_demographics, 
       tpcds.household_demographics, 
       tpcds.customer_address, 
       tpcds.date_dim 
WHERE  s_store_sk = ss_store_sk 
       AND ss_sold_date_sk = d_date_sk 
       AND d_year = 2001 
       AND ( ( ss_hdemo_sk = hd_demo_sk 
               AND cd_demo_sk = ss_cdemo_sk 
               AND cd_marital_status = 'U' 
               AND cd_education_status = 'Advanced Degree' 
               AND ss_sales_price BETWEEN 100.00 AND 150.00 
               AND hd_dep_count = 3 ) 
              OR ( ss_hdemo_sk = hd_demo_sk 
                   AND cd_demo_sk = ss_cdemo_sk 
                   AND cd_marital_status = 'M' 
                   AND cd_education_status = 'Primary' 
                   AND ss_sales_price BETWEEN 50.00 AND 100.00 
                   AND hd_dep_count = 1 ) 
              OR ( ss_hdemo_sk = hd_demo_sk 
                   AND cd_demo_sk = ss_cdemo_sk 
                   AND cd_marital_status = 'D' 
                   AND cd_education_status = 'Secondary' 
                   AND ss_sales_price BETWEEN 150.00 AND 200.00 
                   AND hd_dep_count = 1 ) ) 
       AND ( ( ss_addr_sk = ca_address_sk 
               AND ca_country = 'United States' 
               AND ca_state IN ( 'AZ', 'NE', 'IA' ) 
               AND ss_net_profit BETWEEN 100 AND 200 ) 
              OR ( ss_addr_sk = ca_address_sk 
                   AND ca_country = 'United States' 
                   AND ca_state IN ( 'MS', 'CA', 'NV' ) 
                   AND ss_net_profit BETWEEN 150 AND 300 ) 
              OR ( ss_addr_sk = ca_address_sk 
                   AND ca_country = 'United States' 
                   AND ca_state IN ( 'GA', 'TX', 'NJ' ) 
                   AND ss_net_profit BETWEEN 50 AND 250 )))abc"""
]