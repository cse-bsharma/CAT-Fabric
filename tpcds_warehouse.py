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
                i_item_id )ab""",
"""with /*q11*/customer_total_return as
(select sr_customer_sk as ctr_customer_sk
,sr_store_sk as ctr_store_sk
,sum(sr_return_amt) as ctr_total_return
from tpcds.store_returns
,tpcds.date_dim
where sr_returned_date_sk = d_date_sk
and d_year =2002
group by sr_customer_sk
,sr_store_sk)
 select count_big(*) from (select c_customer_id
from customer_total_return ctr1
,tpcds.store
,tpcds.customer
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from customer_total_return ctr2
where ctr1.ctr_store_sk = ctr2.ctr_store_sk)
and s_store_sk = ctr1.ctr_store_sk
and s_state = 'TN'
and ctr1.ctr_customer_sk = c_customer_sk) ds""",
"""with /*Q12*/wscs as
 (select sold_date_sk
        ,sales_price
  from (select ws_sold_date_sk sold_date_sk
              ,ws_ext_sales_price sales_price
        from tpcds.web_sales 
        union all
        select cs_sold_date_sk sold_date_sk
              ,cs_ext_sales_price sales_price
        from tpcds.catalog_sales) as x),
 wswscs as 
 (select d_week_seq,
        sum(case when (d_day_name='Sunday') then sales_price else null end) sun_sales,
        sum(case when (d_day_name='Monday') then sales_price else null end) mon_sales,
        sum(case when (d_day_name='Tuesday') then sales_price else  null end) tue_sales,
        sum(case when (d_day_name='Wednesday') then sales_price else null end) wed_sales,
        sum(case when (d_day_name='Thursday') then sales_price else null end) thu_sales,
        sum(case when (d_day_name='Friday') then sales_price else null end) fri_sales,
        sum(case when (d_day_name='Saturday') then sales_price else null end) sat_sales
 from wscs
     ,tpcds.date_dim
 where d_date_sk = sold_date_sk
 group by d_week_seq)
 select count_big(*) from(
 select d_week_seq1
       ,round(sun_sales1/sun_sales2,2) a
       ,round(mon_sales1/mon_sales2,2) b
       ,round(tue_sales1/tue_sales2,2) c
       ,round(wed_sales1/wed_sales2,2) d
       ,round(thu_sales1/thu_sales2,2) e
       ,round(fri_sales1/fri_sales2,2) f
       ,round(sat_sales1/sat_sales2,2) g
 from
 (select wswscs.d_week_seq d_week_seq1
        ,sun_sales sun_sales1
        ,mon_sales mon_sales1
        ,tue_sales tue_sales1
        ,wed_sales wed_sales1
        ,thu_sales thu_sales1
        ,fri_sales fri_sales1
        ,sat_sales sat_sales1
  from wswscs,tpcds.date_dim 
  where date_dim.d_week_seq = wswscs.d_week_seq and
        d_year = 2001) y,
 (select wswscs.d_week_seq d_week_seq2
        ,sun_sales sun_sales2
        ,mon_sales mon_sales2
        ,tue_sales tue_sales2
        ,wed_sales wed_sales2
        ,thu_sales thu_sales2
        ,fri_sales fri_sales2
        ,sat_sales sat_sales2
  from wswscs
      ,tpcds.date_dim 
  where date_dim.d_week_seq = wswscs.d_week_seq and
        d_year = 2001+1) z
 where d_week_seq1=d_week_seq2-53)dt""",
"""select /*Q13*/count_big(*) from(
select dt.d_year 
       ,item.i_brand_id brand_id 
       ,item.i_brand brand
       ,sum(ss_ext_sales_price) sum_agg
 from  tpcds.date_dim dt 
      ,tpcds.store_sales
      ,tpcds.item
 where dt.d_date_sk = store_sales.ss_sold_date_sk
   and store_sales.ss_item_sk = item.i_item_sk
   and item.i_manufact_id = 436
   and dt.d_moy=12
 group by dt.d_year
      ,item.i_brand
      ,item.i_brand_id)ab""",
"""select /*Q14*/ case when (select count(*) 
                  from tpcds.store_sales 
                  where ss_quantity between 1 and 20) > 24114
            then (select avg(ss_ext_tax) 
                  from tpcds.store_sales 
                  where ss_quantity between 1 and 20) 
            else (select avg(ss_net_profit)
                  from tpcds.store_sales
                  where ss_quantity between 1 and 20) end bucket1 ,
       case when (select count(*)
                  from tpcds.store_sales
                  where ss_quantity between 21 and 40) > 21602
            then (select avg(ss_ext_tax)
                  from tpcds.store_sales
                  where ss_quantity between 21 and 40) 
            else (select avg(ss_net_profit)
                  from tpcds.store_sales
                  where ss_quantity between 21 and 40) end bucket2,
       case when (select count(*)
                  from tpcds.store_sales
                  where ss_quantity between 41 and 60) > 391592
            then (select avg(ss_ext_tax)
                  from tpcds.store_sales
                  where ss_quantity between 41 and 60)
            else (select avg(ss_net_profit)
                  from tpcds.store_sales
                  where ss_quantity between 41 and 60) end bucket3,
       case when (select count(*)
                  from tpcds.store_sales
                  where ss_quantity between 61 and 80) > 60278
            then (select avg(ss_ext_tax)
                  from tpcds.store_sales
                  where ss_quantity between 61 and 80)
            else (select avg(ss_net_profit)
                  from tpcds.store_sales
                  where ss_quantity between 61 and 80) end bucket4,
       case when (select count(*)
                  from tpcds.store_sales
                  where ss_quantity between 81 and 100) > 384990
            then (select avg(ss_ext_tax)
                  from tpcds.store_sales
                  where ss_quantity between 81 and 100)
            else (select avg(ss_net_profit)
                  from tpcds.store_sales
                  where ss_quantity between 81 and 100) end bucket5
from tpcds.reason
where r_reason_sk = 1""",
"""select /*Q15*/count_big(*) from(
select  i_product_name
             ,i_brand
             ,i_class
             ,avg(cast(inv_quantity_on_hand as bigint)) qoh
       from tpcds.inventory
           ,tpcds.date_dim
           ,tpcds.item
       where inv_date_sk=d_date_sk
              and inv_item_sk=i_item_sk
       group by rollup(i_product_name
                       ,i_brand
                       ,i_class))ab""",
"""select /*Q16*/count_big(*) from(
select s_store_name
      ,sum(ss_net_profit) dt
 from tpcds.store_sales
     ,tpcds.date_dim
     ,tpcds.store,
     (select ca_zip
     from (
      select substring(ca_zip,1,5) ca_zip
      from tpcds.customer_address
      where substring(ca_zip,1,5) in (
                          '33501','58105','69405','16885','37627','12247',
                          '19511','20613','40303','48493','74597',
                          '72427','14685','24369','50585','79241',
                          '86473','94023','39005','82687','69051',
                          '18325','10409','10981','44107','12577',
                          '48981','62923','95585','80477','19801',
                          '76057','65019','92855','65939','80799',
                          '85645','33355','96399','11249','72545',
                          '59891','25077','20713','40059','30463',
                          '29421','63451','21757','32755','88801',
                          '61823','66871','75299','75651','72719',
                          '40753','21065','16373','81025','44615',
                          '50807','59963','45873','57467','77327',
                          '74323','37675','16087','72919','18489',
                          '85643','70137','19783','13611','31375',
                          '32539','13819','11733','50955','31329',
                          '72561','10575','41711','34831','46717',
                          '69393','57677','66277','17877','88905',
                          '18943','71585','43257','21175','78291',
                          '41275','83867','10561','32289','52681',
                          '27261','84623','21117','68521','15179',
                          '11241','45111','52201','61147','52055',
                          '34323','37769','59599','42699','12111',
                          '73745','10421','13963','68557','24211',
                          '41893','68093','44345','19667','62739',
                          '18785','59039','22121','34249','19149',
                          '33995','13677','13141','68573','94683',
                          '80485','64017','51535','19625','91897',
                          '25973','92029','28727','87637','94781',
                          '16471','75497','13767','58829','39453',
                          '94353','21993','34611','67181','96437',
                          '49045','86061','54559','70051','19753',
                          '24837','18849','24485','43005','16511',
                          '39735','60569','23269','57957','21963',
                          '14967','73873','25617','39699','84799',
                          '77137','27145','51991','18289','29915',
                          '21751','31479','85189','33975','73611',
                          '51275','66201','38715','48671','30407',
                          '37051','26961','61267','69777','69957',
                          '34493','18535','56125','53579','33385',
                          '61757','19229','35491','24547','20173',
                          '98267','47865','73307','55371','28647',
                          '51871','91353','21861','67429','17613',
                          '56527','85785','86851','56457','46243',
                          '47957','31943','98481','50159','39923',
                          '80667','73131','11567','59643','86867',
                          '83145','77685','21761','39799','12051',
                          '73943','66127','80515','17923','30807',
                          '42389','49397','89243','58799','35709',
                          '81069','14389','53505','52035','60159',
                          '74673','95859','79467','57639','19709',
                          '26359','17453','93131','47085','59147',
                          '10359','80317','18069','32307','26437',
                          '45109','64795','94309','88195','84943',
                          '36339','97839','49151','69675','32553',
                          '82587','82351','29515','57349','17799',
                          '32389','49021','58745','42937','25735',
                          '31913','99295','81315','35823','71517',
                          '95307','11441','57585','24291','18867',
                          '56075','38383','78937','65719','88559',
                          '51497','22645','93311','18075','57103',
                          '84821','86867','19125','48139','57707',
                          '67581','68671','38211','96419','56335',
                          '38013','62605','61725','22081','32177',
                          '69911','61515','48359','45983','28133',
                          '91021','35265','76715','86577','86313',
                          '45389','77887','62037','62493','68951',
                          '89269','74457','83149','99983','18527',
                          '34027','45705','26433','48631','21267',
                          '24465','40099','61059','66947','38867',
                          '28987','90565','91543','92721','71325',
                          '77377','34385','45691','57693','80675',
                          '71999','51591','68589','18035','37603',
                          '91089','59731','23229','10507','62407',
                          '80545','24323','21827','54647','85461',
                          '85929','14911','11589','17123','54361',
                          '84101','10321','14407','13161','60953',
                          '69143','74023','22231','58557','41821',
                          '91129','45571','30769','12633','67251',
                          '10511','95539','92061','53487')
     intersect
      select ca_zip
      from (select substring(ca_zip,1,5) ca_zip,count(*) cnt
            from tpcds.customer_address, tpcds.customer
            where ca_address_sk = c_current_addr_sk and
                  c_preferred_cust_flag='Y'
            group by ca_zip
            having count(*) > 10)a1)a2) v1
 where ss_store_sk = s_store_sk
  and ss_sold_date_sk = d_date_sk
  and d_qoy = 1 and d_year = 1998
  and (substring(s_zip,1,2) = substring(v1.ca_zip,1,2))
 group by s_store_name)ab""",
"""select /*Q17*/count_big(*) from(
select i_item_id
      ,i_item_desc 
      ,i_class 
      ,i_current_price
      ,sum(ss_ext_sales_price) as itemrevenue 
      ,sum(ss_ext_sales_price)*100/sum(sum(ss_ext_sales_price)) over
          (partition by i_class) as revenueratio
from	
	tpcds.store_sales
    	,tpcds.item 
    	,tpcds.date_dim
where 
	ss_item_sk = i_item_sk 
  	and ss_sold_date_sk = d_date_sk
group by 
	i_item_id
        ,i_item_desc 
        ,i_class
        ,i_current_price)ab""",
"""select /*q18*/count_big(*) from (
select top 100 dt.d_year
 	,item.i_brand_id brand_id
 	,item.i_brand brand
 	,sum(ss_ext_sales_price) ext_price
 from tpcds.date_dim dt
     ,tpcds.store_sales
     ,tpcds.item
 where dt.d_date_sk = store_sales.ss_sold_date_sk
    and store_sales.ss_item_sk = item.i_item_sk
    and item.i_manager_id = 1
    and dt.d_moy=12
    and dt.d_year=1998
 group by dt.d_year
 	,item.i_brand
 	,item.i_brand_id)ab"""]