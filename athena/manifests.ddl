CREATE EXTERNAL TABLE `quilt_manifests_{bucket}`(
  `logical_key` string COMMENT 'from deserializer', 
  `physical_keys` array<string> COMMENT 'from deserializer', 
  `size` string COMMENT 'from deserializer', 
  `hash` struct<type:string,value:string> COMMENT 'from deserializer', 
  `meta` string COMMENT 'from deserializer', 
  `user_meta` string COMMENT 'from deserializer', 
  `message` string COMMENT 'from deserializer', 
  `version` string COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
WITH SERDEPROPERTIES ( 
  'ignore.malformed.json'='true') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://{bucket}/.quilt/packages'
TBLPROPERTIES (
  'has_encrypted_data'='false', 
  'transient_lastDdlTime'='1605312102')
