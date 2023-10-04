SELECT 
	d.name as 'database_name'
	, s.login_name
	, r.session_id
	, r.start_time
	, r.status
	, r.total_elapsed_time
	, r.command
	--, t.text 
	,CASE   --uses statement start and end offset to figure out what statement is running
	WHEN r.[statement_start_offset] > 0 THEN  
	--The start of the active command is not at the beginning of the full command text 
	CASE r.[statement_end_offset]  
		WHEN -1 THEN  
			--The end of the full command is also the end of the active statement 
			SUBSTRING(t.TEXT, (r.[statement_start_offset]/2) + 1, 2147483647) 
		ELSE   
			--The end of the active statement is not at the end of the full command 
			SUBSTRING(t.TEXT, (r.[statement_start_offset]/2) + 1, (r.[statement_end_offset] - r.[statement_start_offset])/2)   
	END  
	ELSE  
	--1st part of full command is running 
	CASE r.[statement_end_offset]  
		WHEN -1 THEN  
			--The end of the full command is also the end of the active statement 
			RTRIM(LTRIM(t.[text]))  
		ELSE  
			--The end of the active statement is not at the end of the full command 
			LEFT(t.TEXT, (r.[statement_end_offset]/2) +1)  
	END  
	END 
	AS [executing_statement] 
	,t.[text] AS [parent_batch] 
	, s.program_name
	--, r.user_id
	--, r.blocking_session_id
	--, r.wait_type
	--, r.wait_time
	--, r.last_wait_type
	--, r.reads
	--, r.writes
	--, r.logical_reads
	, r.query_hash
	, r.query_plan_hash
	, r.dist_statement_id
	, r.label
	--, s.host_name
	, s.client_interface_name
	--,r.statement_start_offset
	--,r.statement_end_offset
	,r.sql_handle
	,c.client_net_address
	,c.connection_id
FROM sys.dm_exec_requests r 
CROSS APPLY sys.[dm_exec_sql_text](r.[sql_handle]) t  
JOIN sys.dm_exec_sessions s
	ON r.session_id = s.session_id
JOIN sys.dm_exec_connections c
	ON s.session_id = c.session_id
JOIN sys.databases d
	ON d.database_id = r.database_id
WHERE r.dist_statement_id != '00000000-0000-0000-0000-000000000000' 
AND r.session_id <> @@SPID 
AND s.program_name <> 'QueryStore'

kill 59;

select * from sys.dm_exec_requests_history;

select count_big(*) from tpch.customer

select min(O_ORDERDATE), max(O_ORDERDATE) from tpch.orders;


select count_big(*) from tpch.customer   ;
select count_big(*) from tpch.lineitem   ;
select count_big(*) from tpch.nation	   ;
select count_big(*) from tpch.orders	   ;
select count_big(*) from tpch.part	   ;
select count_big(*) from tpch.partsupp   ;
select count_big(*) from tpch.region	   ;
select count_big(*) from tpch.supplier   ;

drop table TPCH.CUSTOMER   ;
drop table TPCH.LINEITEM   ;
drop table TPCH.NATION	   ;
drop table TPCH.ORDERS	   ;
drop table TPCH.PART	   ;
drop table TPCH.PARTSUPP   ;
drop table TPCH.REGION	   ;
drop table TPCH.SUPPLIER ;


drop table tpch.customer;


select a.name from sys.tables a inner join sys.schemas b on a.schema_id=b.schema_id where a.type_desc='USER_TABLE' and b.name='tpch' ;


drop table  dbo.call_center              ;
drop table  dbo.catalog_page			  ;
drop table  dbo.catalog_returns		  ;
drop table  dbo.catalog_sales			  ;
drop table  dbo.customer				  ;
drop table  dbo.customer_address		  ;
drop table  dbo.customer_demographics	  ;
drop table  dbo.date_dim				  ;
drop table  dbo.household_demographics	  ;
drop table  dbo.income_band			  ;
drop table  dbo.inventory				  ;
drop table  dbo.item					  ;
drop table  dbo.promotion				  ;
drop table  dbo.reason					  ;
drop table  dbo.ship_mode				  ;
drop table  dbo.store					  ;
drop table  dbo.store_returns			  ;
drop table  dbo.store_sales			  ;
drop table  dbo.time_dim				  ;
drop table  dbo.warehouse				  ;
drop table  dbo.web_page				  ;
drop table  dbo.web_returns			  ;
drop table  dbo.web_sales				  ;
drop table  dbo.web_site;


kill 55 ;
kill 53 ;
kill 151;
kill 152;
kill 157;
kill 168;
kill 170;
kill 176;
kill 178;
kill 179;
kill 216;
kill 217;
kill 219;
kill 221;
kill 222;
kill 223;
kill 224;
kill 225;
kill 226;
kill 227;
kill 229;
kill 230;
kill 231;
kill 234;
kill 236;
kill 238;
kill 239;
kill 242;
kill 245;
kill 246;
kill 251;
kill 255;
kill 256;
kill 257;
kill 258;
kill 259;
kill 260;
kill 261;
kill 263;
kill 264;
kill 265;
kill 267;
kill 268;
kill 269;
kill 270;
kill 271;
kill 272;
kill 274;
kill 275;
kill 276;
kill 277;
kill 278;
kill 279;
kill 280;
kill 281;
kill 282;
kill 283;
kill 284;
kill 285;
kill 286;
kill 287;
kill 282;


sys.sys_manifest_file_catalog_table


select count_big(*) from  dbo.call_center              ;
select count_big(*) from  dbo.catalog_page			  ;
select count_big(*) from  dbo.catalog_returns		  ;
select count_big(*) from  dbo.catalog_sales			  ;
select count_big(*) from  dbo.customer				  ;
select count_big(*) from  dbo.customer_address		  ;
select count_big(*) from  dbo.customer_demographics	  ;
select count_big(*) from  dbo.date_dim				  ;
select count_big(*) from  dbo.household_demographics	  ;
select count_big(*) from  dbo.income_band			  ;
select count_big(*) from  dbo.inventory				  ;
select count_big(*) from  dbo.item					  ;
select count_big(*) from  dbo.promotion				  ;
select count_big(*) from  dbo.reason					  ;
select count_big(*) from  dbo.ship_mode				  ;
select count_big(*) from  dbo.store					  ;
select count_big(*) from  dbo.store_returns			  ;
select count_big(*) from  dbo.store_sales			  ;
select count_big(*) from  dbo.time_dim				  ;
select count_big(*) from  dbo.warehouse				  ;
select count_big(*) from  dbo.web_page				  ;
select count_big(*) from  dbo.web_returns			  ;
select count_big(*) from  dbo.web_sales				  ;
select count_big(*) from  dbo.web_site;



select * from tpcdsstage.catalog_sales where cs_sold_date_sk not like '%[0-9]%'

INSERT INTO	dbo.catalog_sales	select * from	tpcdsstage.catalog_sales	;
INSERT INTO	dbo.store_returns	select * from	tpcdsstage.store_returns	;
INSERT INTO	dbo.store_sales	select * from	tpcdsstage.store_sales	;
INSERT INTO	dbo.time_dim	select * from	tpcdsstage.time_dim	;
INSERT INTO	dbo.warehouse	select * from	tpcdsstage.warehouse	;
INSERT INTO	dbo.web_page	select * from	tpcdsstage.web_page	;
INSERT INTO	dbo.web_returns	select * from	tpcdsstage.web_returns	;
INSERT INTO	dbo.web_sales	select * from	tpcdsstage.web_sales	;
INSERT INTO	dbo.web_site        	select * from	tpcdsstage.web_site	;


INSERT INTO	lakehouse.dbo_call_center           	select * from	dbo.call_center            	;
INSERT INTO	lakehouse.dbo_catalog_page	select * from	dbo.catalog_page	;
INSERT INTO	lakehouse.dbo_catalog_returns	select * from	dbo.catalog_returns	;
INSERT INTO	lakehouse.dbo_catalog_sales	select * from	dbo.catalog_sales	;
INSERT INTO	lakehouse.dbo_customer	select * from	dbo.customer	;
INSERT INTO	lakehouse.dbo_customer_address	select * from	dbo.customer_address	;
INSERT INTO	lakehouse.dbo_customer_demographics	select * from	dbo.customer_demographics	;
INSERT INTO	lakehouse.dbo_date_dim	select * from	dbo.date_dim	;
INSERT INTO	lakehouse.dbo_household_demographics	select * from	dbo.household_demographics	;
INSERT INTO	lakehouse.dbo_income_band	select * from	dbo.income_band	;
INSERT INTO	lakehouse.dbo_inventory	select * from	dbo.inventory	;
INSERT INTO	lakehouse.dbo_item	select * from	dbo.item	;
INSERT INTO	lakehouse.dbo_promotion	select * from	dbo.promotion	;
INSERT INTO	lakehouse.dbo_reason	select * from	dbo.reason	;
INSERT INTO	lakehouse.dbo_ship_mode	select * from	dbo.ship_mode	;
INSERT INTO	lakehouse.dbo_store	select * from	dbo.store	;
INSERT INTO	lakehouse.dbo_time_dim	select * from	dbo.time_dim	;
INSERT INTO	lakehouse.dbo_warehouse	select * from	dbo.warehouse	;
INSERT INTO	lakehouse.dbo_web_page	select * from	dbo.web_page	;
INSERT INTO	lakehouse.dbo_web_sales	select * from	dbo.web_sales	;
INSERT INTO	lakehouse.dbo_web_site        	select * from	dbo.web_site	;

