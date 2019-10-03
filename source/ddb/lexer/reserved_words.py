# This builds the BYTECODE definitions for ddb
import timeit


SECTION_BLOCK_START=1000
SECTION_BLOCK_INCREMENT=1000
WORD_INCREMENT =2

# All  MYSQL 8 reserverd/keywords are here for fure use, change element 3=1 to activte

words=[
 ['R_ACCESSIBLE'                   ,'ACCESSIBLE',0,]
,['R_ADD'                          ,'ADD',0,]
,['R_ALL'                          ,'ALL',0,]
,['R_ALTER'                        ,'ALTER',0,]
,['R_ANALYZE'                      ,'ANALYZE',0,]
,['R_AND'                          ,'AND',1,]
,['R_ARRAY'                        ,'ARRAY',0,]
,['R_ASC'                          ,'ASC',1,]
,['R_ASENSITIVE'                   ,'ASENSITIVE',0,]
,['R_AS'                           ,'AS',1,]
,['R_BEFORE'                       ,'BEFORE',1,]
,['R_BETWEEN'                      ,'BETWEEN',1,]
,['R_BIGINT'                       ,'BIGINT',0,]
,['R_BINARY'                       ,'BINARY',0,]
,['R_BLOB'                         ,'BLOB',0,]
,['R_BOTH'                         ,'BOTH',0,]
,['R_BY'                           ,'BY',1,]
,['R_CALL'                         ,'CALL',0,]
,['R_CASCADE'                      ,'CASCADE',0,]
,['R_CASE'                         ,'CASE',0,]
,['R_CHANGE'                       ,'CHANGE',0,]
,['R_CHARACTER'                    ,'CHARACTER',0,]
,['R_CHAR'                         ,'CHAR',0,]
,['R_CHECK'                        ,'CHECK',0,]
,['R_COLLATE'                      ,'COLLATE',0,]
,['R_COLUMN'                       ,'COLUMN',0,]
,['R_CONDITION'                    ,'CONDITION',0,]
,['R_CONSTRAINT'                   ,'CONSTRAINT',0,]
,['R_CONTINUE'                     ,'CONTINUE',0,]
,['R_CONVERT'                      ,'CONVERT',0,]
,['R_CREATE'                       ,'CREATE',1,]
,['R_CROSS'                        ,'CROSS',0,]
,['R_CUBE'                         ,'CUBE',0,]
,['R_CUME_DIST'                    ,'CUME_DIST',0,]
,['R_CURRENT_DATE'                 ,'CURRENT_DATE',0,]
,['R_CURRENT_TIME'                 ,'CURRENT_TIME',0,]
,['R_CURRENT_TIMESTAMP'            ,'CURRENT_TIMESTAMP',0,]
,['R_CURRENT_USER'                 ,'CURRENT_USER',0,]
,['R_CURSOR'                       ,'CURSOR',0,]
,['R_DATABASE'                     ,'DATABASE',1,]
,['R_DATABASES'                    ,'DATABASES',1,]
,['R_DAY_HOUR'                     ,'DAY_HOUR',0,]
,['R_DAY_MICROSECOND'              ,'DAY_MICROSECOND',0,]
,['R_DAY_MINUTE'                   ,'DAY_MINUTE',0,]
,['R_DAY_SECOND'                   ,'DAY_SECOND',0,]
,['R_DECIMAL'                      ,'DECIMAL',0,]
,['R_DECLARE'                      ,'DECLARE',0,]
,['R_DEC'                          ,'DEC',0,]
,['R_DEFAULT'                      ,'DEFAULT',0,]
,['R_DELAYED'                      ,'DELAYED',0,]
,['R_DELETE'                       ,'DELETE',0,]
,['R_DENSE_RANK'                   ,'DENSE_RANK',0,]
,['R_DESC'                         ,'DESC',1,]
,['R_DESCRIBE'                     ,'DESCRIBE',0,]
,['R_DETERMINISTIC'                ,'DETERMINISTIC',0,]
,['R_DISTINCT'                     ,'DISTINCT',1,]
,['R_DISTINCTROW'                  ,'DISTINCTROW',0,]
,['R_DIV'                          ,'DIV',0,]
,['R_DOUBLE'                       ,'DOUBLE',0,]
,['R_DROP'                         ,'DROP',1,]
,['R_DUAL'                         ,'DUAL',0,]
,['R_EACH'                         ,'EACH',0,]
,['R_ELSEIF'                       ,'ELSEIF',0,]
,['R_ELSE'                         ,'ELSE',0,]
,['R_EMPTY'                        ,'EMPTY',0,]
,['R_ENCLOSED'                     ,'ENCLOSED',0,]
,['R_ESCAPED'                      ,'ESCAPED',0,]
,['R_EXCEPT'                       ,'EXCEPT',0,]
,['R_EXISTS'                       ,'EXISTS',1,]
,['R_EXIT'                         ,'EXIT',0,]
,['R_EXPLAIN'                      ,'EXPLAIN',0,]
,['R_FALSE'                        ,'FALSE',1,]
,['R_FETCH'                        ,'FETCH',0,]
,['R_FIRST_VALUE'                  ,'FIRST_VALUE',0,]
,['R_FLOAT4'                       ,'FLOAT4',0,]
,['R_FLOAT8'                       ,'FLOAT8',0,]
,['R_FLOAT'                        ,'FLOAT',0,]
,['R_FORCE'                        ,'FORCE',0,]
,['R_FOREIGN'                      ,'FOREIGN',0,]
,['R_FOR'                          ,'FOR',0,]
,['R_FROM'                         ,'FROM',1,]
,['R_FULLTEXT'                     ,'FULLTEXT',0,]
,['R_FUNCTION'                     ,'FUNCTION',0,]
,['R_GENERATED'                    ,'GENERATED',0,]
,['R_GET'                          ,'GET',0,]
,['R_GRANT'                        ,'GRANT',0,]
,['R_GROUPING'                     ,'GROUPING',0,]
,['R_GROUP'                        ,'GROUP',1,]
,['R_GROUPS'                       ,'GROUPS',1,]
,['R_HAVING'                       ,'HAVING',1,]
,['R_HIGH_PRIORITY'                ,'HIGH_PRIORITY',0,]
,['R_HOUR_MICROSECOND'             ,'HOUR_MICROSECOND',0,]
,['R_HOUR_MINUTE'                  ,'HOUR_MINUTE',0,]
,['R_HOUR_SECOND'                  ,'HOUR_SECOND',0,]
,['R_IF'                           ,'IF',0,]
,['R_IGNORE'                       ,'IGNORE',0,]
,['R_INDEX'                        ,'INDEX',0,]
,['R_INFILE'                       ,'INFILE',0,]
,['R_INNER'                        ,'INNER',0,]
,['R_INOUT'                        ,'INOUT',0,]
,['R_IN'                           ,'IN',1,]
,['R_INSENSITIVE'                  ,'INSENSITIVE',0,]
,['R_INSERT'                       ,'INSERT',1,]
,['R_INT1'                         ,'INT1',0,]
,['R_INT2'                         ,'INT2',0,]
,['R_INT3'                         ,'INT3',0,]
,['R_INT4'                         ,'INT4',0,]
,['R_INT8'                         ,'INT8',0,]
,['R_INTEGER'                      ,'INTEGER',0,]
,['R_INTERVAL'                     ,'INTERVAL',0,]
,['R_INTO'                         ,'INTO',1,]
,['R_INT'                          ,'INT',0,]
,['R_IO_AFTER_GTIDS'               ,'IO_AFTER_GTIDS',0,]
,['R_IO_BEFORE_GTIDS'              ,'IO_BEFORE_GTIDS',0,]
,['R_IS'                           ,'IS',1,]
,['R_ITERATE'                      ,'ITERATE',0,]
,['R_JOIN'                         ,'JOIN',1,]
,['R_JSON_TABLE'                   ,'JSON_TABLE',0,]
,['R_KEY'                          ,'KEY',0,]
,['R_KEYS'                         ,'KEYS',0,]
,['R_KILL'                         ,'KILL',0,]
,['R_LAG'                          ,'LAG',0,]
,['R_LAST_VALUE'                   ,'LAST_VALUE',0,]
,['R_LATERAL'                      ,'LATERAL',0,]
,['R_LEADING'                      ,'LEADING',0,]
,['R_LEAD'                         ,'LEAD',0,]
,['R_LEAVE'                        ,'LEAVE',0,]
,['R_LEFT'                         ,'LEFT',1,]
,['R_LIKE'                         ,'LIKE',1,]
,['R_LIMIT'                        ,'LIMIT',1,]
,['R_LINEAR'                       ,'LINEAR',0,]
,['R_LINES'                        ,'LINES',0,]
,['R_LOAD'                         ,'LOAD',0,]
,['R_LOCALTIME'                    ,'LOCALTIME',0,]
,['R_LOCALTIMESTAMP'               ,'LOCALTIMESTAMP',0,]
,['R_LOCK'                         ,'LOCK',0,]
,['R_LONGBLOB'                     ,'LONGBLOB',0,]
,['R_LONG'                         ,'LONG',0,]
,['R_LONGTEXT'                     ,'LONGTEXT',0,]
,['R_LOOP'                         ,'LOOP',0,]
,['R_LOW_PRIORITY'                 ,'LOW_PRIORITY',0,]
,['R_MASTER_BIND'                  ,'MASTER_BIND',0,]
,['R_MASTER_SSL_VERIFY_SERVER_CERT','MASTER_SSL_VERIFY_SERVER_CERT',0,]
,['R_MATCH'                        ,'MATCH',0,]
,['R_MAXVALUE'                     ,'MAXVALUE',0,]
,['R_MEDIUMBLOB'                   ,'MEDIUMBLOB',0,]
,['R_MEDIUMINT'                    ,'MEDIUMINT',0,]
,['R_MEDIUMTEXT'                   ,'MEDIUMTEXT',0,]
,['R_MEMBER'                       ,'MEMBER',0,]
,['R_MIDDLEINT'                    ,'MIDDLEINT',0,]
,['R_MINUTE_MICROSECOND'           ,'MINUTE_MICROSECOND',0,]
,['R_MINUTE_SECOND'                ,'MINUTE_SECOND',0,]
,['R_MODIFIES'                     ,'MODIFIES',0,]
,['R_MOD'                          ,'MOD',1,]
,['R_NATURAL'                      ,'NATURAL',0,]
,['R_NOT'                          ,'NOT',1,]
,['R_NO_WRITE_TO_BINLOG'           ,'NO_WRITE_TO_BINLOG',0,]
,['R_NTH_VALUE'                    ,'NTH_VALUE',0,]
,['R_NTILE'                        ,'NTILE',0,]
,['R_NULL'                         ,'NULL',1,]
,['R_NUMERIC'                      ,'NUMERIC',0,]
,['R_OF'                           ,'OF',0,]
,['R_ON'                           ,'ON',1,]
,['R_OPTIMIZE'                     ,'OPTIMIZE',0,]
,['R_OPTIMIZER_COSTS'              ,'OPTIMIZER_COSTS',0,]
,['R_OPTIONALLY'                   ,'OPTIONALLY',0,]
,['R_OPTION'                       ,'OPTION',0,]
,['R_ORDER'                        ,'ORDER',1,]
,['R_OR'                           ,'OR',1,]
,['R_OUTER'                        ,'OUTER',0,]
,['R_OUTFILE'                      ,'OUTFILE',0,]
,['R_OUT'                          ,'OUT',0,]
,['R_OVER'                         ,'OVER',0,]
,['R_PARTITION'                    ,'PARTITION',0,]
,['R_PERCENT_RANK'                 ,'PERCENT_RANK',0,]
,['R_PRECISION'                    ,'PRECISION',0,]
,['R_PRIMARY'                      ,'PRIMARY',0,]
,['R_PROCEDURE'                    ,'PROCEDURE',0,]
,['R_PURGE'                        ,'PURGE',0,]
,['R_RANGE'                        ,'RANGE',0,]
,['R_RANK'                         ,'RANK',0,]
,['R_READ'                         ,'READ',0,]
,['R_READS'                        ,'READS',0,]
,['R_READ_WRITE'                   ,'READ_WRITE',0,]
,['R_REAL'                         ,'REAL',0,]
,['R_RECURSIVE'                    ,'RECURSIVE',0,]
,['R_REFERENCES'                   ,'REFERENCES',0,]
,['R_REGEXP'                       ,'REGEXP',0,]
,['R_RELEASE'                      ,'RELEASE',0,]
,['R_RENAME'                       ,'RENAME',0,]
,['R_REPEAT'                       ,'REPEAT',0,]
,['R_REPLACE'                      ,'REPLACE',0,]
,['R_REQUIRE'                      ,'REQUIRE',0,]
,['R_RESIGNAL'                     ,'RESIGNAL',0,]
,['R_RESTRICT'                     ,'RESTRICT',0,]
,['R_RETURN'                       ,'RETURN',0,]
,['R_REVOKE'                       ,'REVOKE',0,]
,['R_RIGHT'                        ,'RIGHT',1,]
,['R_RLIKE'                        ,'RLIKE',0,]
,['R_ROW_NUMBER'                   ,'ROW_NUMBER',0,]
,['R_ROW'                          ,'ROW',0,]
,['R_ROWS'                         ,'ROWS',0,]
,['R_SCHEMA'                       ,'SCHEMA',0,]
,['R_SCHEMAS'                      ,'SCHEMAS',0,]
,['R_SECOND_MICROSECOND'           ,'SECOND_MICROSECOND',0,]
,['R_SELECT'                       ,'SELECT',1,]
,['R_SENSITIVE'                    ,'SENSITIVE',0,]
,['R_SEPARATOR'                    ,'SEPARATOR',0,]
,['R_SET'                          ,'SET',1,]
,['R_SHOW'                         ,'SHOW',1,]
,['R_SIGNAL'                       ,'SIGNAL',0,]
,['R_SMALLINT'                     ,'SMALLINT',0,]
,['R_SPATIAL'                      ,'SPATIAL',0,]
,['R_SPECIFIC'                     ,'SPECIFIC',0,]
,['R_SQL_BIG_RESULT'               ,'SQL_BIG_RESULT',0,]
,['R_SQL_CALC_FOUND_ROWS'          ,'SQL_CALC_FOUND_ROWS',0,]
,['R_SQLEXCEPTION'                 ,'SQLEXCEPTION',0,]
,['R_SQL'                          ,'SQL',0,]
,['R_SQL_SMALL_RESULT'             ,'SQL_SMALL_RESULT',0,]
,['R_SQLSTATE'                     ,'SQLSTATE',0,]
,['R_SQLWARNING'                   ,'SQLWARNING',0,]
,['R_SSL'                          ,'SSL',0,]
,['R_STARTING'                     ,'STARTING',0,]
,['R_STORED'                       ,'STORED',0,]
,['R_STRAIGHT_JOIN'                ,'STRAIGHT_JOIN',0,]
,['R_SYSTEM'                       ,'SYSTEM',0,]
,['R_TABLE'                        ,'TABLE',1,]
,['R_TERMINATED'                   ,'TERMINATED',0,]
,['R_THEN'                         ,'THEN',0,]
,['R_TINYBLOB'                     ,'TINYBLOB',0,]
,['R_TINYINT'                      ,'TINYINT',0,]
,['R_TINYTEXT'                     ,'TINYTEXT',0,]
,['R_TO'                           ,'TO',0,]
,['R_TRAILING'                     ,'TRAILING',0,]
,['R_TRIGGER'                      ,'TRIGGER',0,]
,['R_TRUE'                         ,'TRUE',1,]
,['R_UNDO'                         ,'UNDO',0,]
,['R_UNION'                        ,'UNION',1,]
,['R_UNIQUE'                       ,'UNIQUE',1,]
,['R_UNLOCK'                       ,'UNLOCK',0,]
,['R_UNSIGNED'                     ,'UNSIGNED',0,]
,['R_UPDATE'                       ,'UPDATE',1,]
,['R_USAGE'                        ,'USAGE',0,]
,['R_USE'                          ,'USE',0,]
,['R_USING'                        ,'USING',0,]
,['R_UTC_DATE'                     ,'UTC_DATE',0,]
,['R_UTC_TIME'                     ,'UTC_TIME',0,]
,['R_UTC_TIMESTAMP'                ,'UTC_TIMESTAMP',0,]
,['R_VALUES'                       ,'VALUES',1,]
,['R_VARBINARY'                    ,'VARBINARY',0,]
,['R_VARCHARACTER'                 ,'VARCHARACTER',0,]
,['R_VARCHAR'                      ,'VARCHAR',0,]
,['R_VARYING'                      ,'VARYING',0,]
,['R_VIRTUAL'                      ,'VIRTUAL',0,]
,['R_WHEN'                         ,'WHEN',0,]
,['R_WHERE'                        ,'WHERE',1,]
,['R_WHILE'                        ,'WHILE',0,]
,['R_WINDOW'                       ,'WINDOW',0,]
,['R_WITH'                         ,'WITH',0,]
,['R_WRITE'                        ,'WRITE',0,]
,['R_XOR'                          ,'XOR',1,]
,['R_YEAR_MONTH'                   ,'YEAR_MONTH',0,]
,['R_ZEROFILL'                     ,'ZEROFILL',0,]
,['K_ACCOUNT'                      ,'ACCOUNT',0,]
,['K_ACTION'                       ,'ACTION',0,]
,['K_ACTIVE'                       ,'ACTIVE',0,]
,['K_ADMIN'                        ,'ADMIN',0,]
,['K_AFTER'                        ,'AFTER',0,]
,['K_AGAINST'                      ,'AGAINST',0,]
,['K_AGGREGATE'                    ,'AGGREGATE',0,]
,['K_ALGORITHM'                    ,'ALGORITHM',0,]
,['K_ALWAYS'                       ,'ALWAYS',0,]
,['K_ANALYSE'                      ,'ANALYSE',0,]
,['K_ANY'                          ,'ANY',0,]
,['K_ASCII'                        ,'ASCII',0,]
,['K_AT'                           ,'AT',0,]
,['K_AUTOEXTEND_SIZE'              ,'AUTOEXTEND_SIZE',0,]
,['K_AUTO_INCREMENT'               ,'AUTO_INCREMENT',0,]
,['K_AVG'                          ,'AVG',0,]
,['K_AVG_ROW_LENGTH'               ,'AVG_ROW_LENGTH',0,]
,['K_BACKUP'                       ,'BACKUP',0,]
,['K_BEGIN'                        ,'BEGIN',0,]
,['K_BINLOG'                       ,'BINLOG',0,]
,['K_BIT'                          ,'BIT',0,]
,['K_BLOCK'                        ,'BLOCK',0,]
,['K_BOOL'                         ,'BOOL',0,]
,['K_BOOLEAN'                      ,'BOOLEAN',0,]
,['K_BTREE'                        ,'BTREE',0,]
,['K_BUCKETS'                      ,'BUCKETS',0,]
,['K_BYTE'                         ,'BYTE',0,]
,['K_CACHE'                        ,'CACHE',0,]
,['K_CASCADED'                     ,'CASCADED',0,]
,['K_CATALOG_NAME'                 ,'CATALOG_NAME',0,]
,['K_CHAIN'                        ,'CHAIN',0,]
,['K_CHANGED'                      ,'CHANGED',0,]
,['K_CHANNEL'                      ,'CHANNEL',0,]
,['K_CHARSET'                      ,'CHARSET',0,]
,['K_CHECKSUM'                     ,'CHECKSUM',0,]
,['K_CIPHER'                       ,'CIPHER',0,]
,['K_CLASS_ORIGIN'                 ,'CLASS_ORIGIN',0,]
,['K_CLIENT'                       ,'CLIENT',0,]
,['K_CLONE'                        ,'CLONE',0,]
,['K_CLOSE'                        ,'CLOSE',0,]
,['K_COALESCE'                     ,'COALESCE',0,]
,['K_CODE'                         ,'CODE',0,]
,['K_COLLATION'                    ,'COLLATION',0,]
,['K_COLUMN_FORMAT'                ,'COLUMN_FORMAT',0,]
,['K_COLUMN_NAME'                  ,'COLUMN_NAME',0,]
,['K_COLUMNS'                      ,'COLUMNS',0,]
,['K_COMMENT'                      ,'COMMENT',0,]
,['K_COMMIT'                       ,'COMMIT',0,]
,['K_COMMITTED'                    ,'COMMITTED',0,]
,['K_COMPACT'                      ,'COMPACT',0,]
,['K_COMPLETION'                   ,'COMPLETION',0,]
,['K_COMPONENT'                    ,'COMPONENT',0,]
,['K_COMPRESSED'                   ,'COMPRESSED',0,]
,['K_COMPRESSION'                  ,'COMPRESSION',0,]
,['K_CONCURRENT'                   ,'CONCURRENT',0,]
,['K_CONNECTION'                   ,'CONNECTION',0,]
,['K_CONSISTENT'                   ,'CONSISTENT',0,]
,['K_CONSTRAINT_CATALOG'           ,'CONSTRAINT_CATALOG',0,]
,['K_CONSTRAINT_NAME'              ,'CONSTRAINT_NAME',0,]
,['K_CONSTRAINT_SCHEMA'            ,'CONSTRAINT_SCHEMA',0,]
,['K_CONTAINS'                     ,'CONTAINS',0,]
,['K_CONTEXT'                      ,'CONTEXT',0,]
,['K_CPU'                          ,'CPU',0,]
,['K_CURRENT'                      ,'CURRENT',0,]
,['K_CURSOR_NAME'                  ,'CURSOR_NAME',0,]
,['K_DATA'                         ,'DATA',0,]
,['K_DATAFILE'                     ,'DATAFILE',0,]
,['K_DATE'                         ,'DATE',1,]
,['K_DATETIME'                     ,'DATETIME',1,]
,['K_DAY'                          ,'DAY',0,]
,['K_DEALLOCATE'                   ,'DEALLOCATE',0,]
,['K_DEFAULT_AUTH'                 ,'DEFAULT_AUTH',0,]
,['K_DEFINER'                      ,'DEFINER',0,]
,['K_DEFINITION'                   ,'DEFINITION',0,]
,['K_DELAY_KEY_WRITE'              ,'DELAY_KEY_WRITE',0,]
,['K_DESCRIPTION'                  ,'DESCRIPTION',0,]
,['K_DES_KEY_FILE'                 ,'DES_KEY_FILE',0,]
,['K_DIAGNOSTICS'                  ,'DIAGNOSTICS',0,]
,['K_DIRECTORY'                    ,'DIRECTORY',0,]
,['K_DISABLE'                      ,'DISABLE',0,]
,['K_DISCARD'                      ,'DISCARD',0,]
,['K_DISK'                         ,'DISK',0,]
,['K_DO'                           ,'DO',0,]
,['K_DUMPFILE'                     ,'DUMPFILE',0,]
,['K_DUPLICATE'                    ,'DUPLICATE',0,]
,['K_DYNAMIC'                      ,'DYNAMIC',0,]
,['K_ENABLE'                       ,'ENABLE',0,]
,['K_ENCRYPTION'                   ,'ENCRYPTION',0,]
,['K_END'                          ,'END',0,]
,['K_ENDS'                         ,'ENDS',0,]
,['K_ENFORCED'                     ,'ENFORCED',0,]
,['K_ENGINE'                       ,'ENGINE',0,]
,['K_ENGINES'                      ,'ENGINES',0,]
,['K_ENUM'                         ,'ENUM',0,]
,['K_ERROR'                        ,'ERROR',0,]
,['K_ERRORS'                       ,'ERRORS',0,]
,['K_ESCAPE'                       ,'ESCAPE',0,]
,['K_EVENT'                        ,'EVENT',0,]
,['K_EVENTS'                       ,'EVENTS',0,]
,['K_EVERY'                        ,'EVERY',0,]
,['K_EXCHANGE'                     ,'EXCHANGE',0,]
,['K_EXCLUDE'                      ,'EXCLUDE',0,]
,['K_EXECUTE'                      ,'EXECUTE',0,]
,['K_EXPANSION'                    ,'EXPANSION',0,]
,['K_EXPIRE'                       ,'EXPIRE',0,]
,['K_EXPORT'                       ,'EXPORT',0,]
,['K_EXTENDED'                     ,'EXTENDED',0,]
,['K_EXTENT_SIZE'                  ,'EXTENT_SIZE',0,]
,['K_FAST'                         ,'FAST',0,]
,['K_FAULTS'                       ,'FAULTS',0,]
,['K_FIELDS'                       ,'FIELDS',0,]
,['K_FILE'                         ,'FILE',0,]
,['K_FILE_BLOCK_SIZE'              ,'FILE_BLOCK_SIZE',0,]
,['K_FILTER'                       ,'FILTER',0,]
,['K_FIRST'                        ,'FIRST',0,]
,['K_FIXED'                        ,'FIXED',0,]
,['K_FLUSH'                        ,'FLUSH',0,]
,['K_FOLLOWING'                    ,'FOLLOWING',0,]
,['K_FOLLOWS'                      ,'FOLLOWS',0,]
,['K_FORMAT'                       ,'FORMAT',0,]
,['K_FOUND'                        ,'FOUND',0,]
,['K_FULL'                         ,'FULL',1,]
,['K_GENERAL'                      ,'GENERAL',0,]
,['K_GEOMCOLLECTION'               ,'GEOMCOLLECTION',0,]
,['K_GEOMETRY'                     ,'GEOMETRY',0,]
,['K_GEOMETRYCOLLECTION'           ,'GEOMETRYCOLLECTION',0,]
,['K_GET_FORMAT'                   ,'GET_FORMAT',0,]
,['K_GET_MASTER_PUBLIC_KEY'        ,'GET_MASTER_PUBLIC_KEY',0,]
,['K_GLOBAL'                       ,'GLOBAL',0,]
,['K_GRANTS'                       ,'GRANTS',0,]
,['K_GROUP_REPLICATION'            ,'GROUP_REPLICATION',0,]
,['K_HANDLER'                      ,'HANDLER',0,]
,['K_HASH'                         ,'HASH',0,]
,['K_HELP'                         ,'HELP',0,]
,['K_HISTOGRAM'                    ,'HISTOGRAM',0,]
,['K_HISTORY'                      ,'HISTORY',0,]
,['K_HOST'                         ,'HOST',0,]
,['K_HOSTS'                        ,'HOSTS',0,]
,['K_HOUR'                         ,'HOUR',0,]
,['K_IDENTIFIED'                   ,'IDENTIFIED',0,]
,['K_IGNORE_SERVER_IDS'            ,'IGNORE_SERVER_IDS',0,]
,['K_IMPORT'                       ,'IMPORT',0,]
,['K_INACTIVE'                     ,'INACTIVE',0,]
,['K_INDEXES'                      ,'INDEXES',0,]
,['K_INITIAL_SIZE'                 ,'INITIAL_SIZE',0,]
,['K_INSERT_METHOD'                ,'INSERT_METHOD',0,]
,['K_INSTALL'                      ,'INSTALL',0,]
,['K_INSTANCE'                     ,'INSTANCE',0,]
,['K_INVISIBLE'                    ,'INVISIBLE',0,]
,['K_INVOKER'                      ,'INVOKER',0,]
,['K_IO'                           ,'IO',0,]
,['K_IO_THREAD'                    ,'IO_THREAD',0,]
,['K_IPC'                          ,'IPC',0,]
,['K_ISOLATION'                    ,'ISOLATION',0,]
,['K_ISSUER'                       ,'ISSUER',0,]
,['K_JSON'                         ,'JSON',0,]
,['K_KEY_BLOCK_SIZE'               ,'KEY_BLOCK_SIZE',0,]
,['K_LANGUAGE'                     ,'LANGUAGE',0,]
,['K_LAST'                         ,'LAST',0,]
,['K_LEAVES'                       ,'LEAVES',0,]
,['K_LESS'                         ,'LESS',0,]
,['K_LEVEL'                        ,'LEVEL',0,]
,['K_LINESTRING'                   ,'LINESTRING',0,]
,['K_LIST'                         ,'LIST',0,]
,['K_LOCAL'                        ,'LOCAL',0,]
,['K_LOCKED'                       ,'LOCKED',0,]
,['K_LOCKS'                        ,'LOCKS',0,]
,['K_LOGFILE'                      ,'LOGFILE',0,]
,['K_LOGS'                         ,'LOGS',0,]
,['K_MASTER'                       ,'MASTER',0,]
,['K_MASTER_AUTO_POSITION'         ,'MASTER_AUTO_POSITION',0,]
,['K_MASTER_COMPRESSION_ALGORITHMS','MASTER_COMPRESSION_ALGORITHMS',0,]
,['K_MASTER_CONNECT_RETRY'         ,'MASTER_CONNECT_RETRY',0,]
,['K_MASTER_DELAY'                 ,'MASTER_DELAY',0,]
,['K_MASTER_HEARTBEAT_PERIOD'      ,'MASTER_HEARTBEAT_PERIOD',0,]
,['K_MASTER_HOST'                  ,'MASTER_HOST',0,]
,['K_MASTER_LOG_FILE'              ,'MASTER_LOG_FILE',0,]
,['K_MASTER_LOG_POS'               ,'MASTER_LOG_POS',0,]
,['K_MASTER_PASSWORD'              ,'MASTER_PASSWORD',0,]
,['K_MASTER_PORT'                  ,'MASTER_PORT',0,]
,['K_MASTER_PUBLIC_KEY_PATH'       ,'MASTER_PUBLIC_KEY_PATH',0,]
,['K_MASTER_RETRY_COUNT'           ,'MASTER_RETRY_COUNT',0,]
,['K_MASTER_SERVER_ID'             ,'MASTER_SERVER_ID',0,]
,['K_MASTER_SSL'                   ,'MASTER_SSL',0,]
,['K_MASTER_SSL_CA'                ,'MASTER_SSL_CA',0,]
,['K_MASTER_SSL_CAPATH'            ,'MASTER_SSL_CAPATH',0,]
,['K_MASTER_SSL_CERT'              ,'MASTER_SSL_CERT',0,]
,['K_MASTER_SSL_CIPHER'            ,'MASTER_SSL_CIPHER',0,]
,['K_MASTER_SSL_CRL'               ,'MASTER_SSL_CRL',0,]
,['K_MASTER_SSL_CRLPATH'           ,'MASTER_SSL_CRLPATH',0,]
,['K_MASTER_SSL_KEY'               ,'MASTER_SSL_KEY',0,]
,['K_MASTER_TLS_CIPHERSUITES'      ,'MASTER_TLS_CIPHERSUITES',0,]
,['K_MASTER_TLS_VERSION'           ,'MASTER_TLS_VERSION',0,]
,['K_MASTER_USER'                  ,'MASTER_USER',0,]
,['K_MASTER_ZSTD_COMPRESSION_LEVEL','MASTER_ZSTD_COMPRESSION_LEVEL',0,]
,['K_MAX_CONNECTIONS_PER_HOUR'     ,'MAX_CONNECTIONS_PER_HOUR',0,]
,['K_MAX_QUERIES_PER_HOUR'         ,'MAX_QUERIES_PER_HOUR',0,]
,['K_MAX_ROWS'                     ,'MAX_ROWS',0,]
,['K_MAX_SIZE'                     ,'MAX_SIZE',0,]
,['K_MAX_UPDATES_PER_HOUR'         ,'MAX_UPDATES_PER_HOUR',0,]
,['K_MAX_USER_CONNECTIONS'         ,'MAX_USER_CONNECTIONS',0,]
,['K_MEDIUM'                       ,'MEDIUM',0,]
,['K_MEMORY'                       ,'MEMORY',0,]
,['K_MERGE'                        ,'MERGE',0,]
,['K_MESSAGE_TEXT'                 ,'MESSAGE_TEXT',0,]
,['K_MICROSECOND'                  ,'MICROSECOND',0,]
,['K_MIGRATE'                      ,'MIGRATE',0,]
,['K_MIN_ROWS'                     ,'MIN_ROWS',0,]
,['K_MINUTE'                       ,'MINUTE',0,]
,['K_MODE'                         ,'MODE',0,]
,['K_MODIFY'                       ,'MODIFY',0,]
,['K_MONTH'                        ,'MONTH',0,]
,['K_MULTILINESTRING'              ,'MULTILINESTRING',0,]
,['K_MULTIPOINT'                   ,'MULTIPOINT',0,]
,['K_MULTIPOLYGON'                 ,'MULTIPOLYGON',0,]
,['K_MUTEX'                        ,'MUTEX',0,]
,['K_MYSQL_ERRNO'                  ,'MYSQL_ERRNO',0,]
,['K_NAME'                         ,'NAME',0,]
,['K_NAMES'                        ,'NAMES',0,]
,['K_NATIONAL'                     ,'NATIONAL',0,]
,['K_NCHAR'                        ,'NCHAR',0,]
,['K_NDB'                          ,'NDB',0,]
,['K_NDBCLUSTER'                   ,'NDBCLUSTER',0,]
,['K_NESTED'                       ,'NESTED',0,]
,['K_NETWORK_NAMESPACE'            ,'NETWORK_NAMESPACE',0,]
,['K_NEVER'                        ,'NEVER',0,]
,['K_NEW'                          ,'NEW',0,]
,['K_NEXT'                         ,'NEXT',0,]
,['K_NO'                           ,'NO',0,]
,['K_NODEGROUP'                    ,'NODEGROUP',0,]
,['K_NONE'                         ,'NONE',0,]
,['K_NO_WAIT'                      ,'NO_WAIT',0,]
,['K_NOWAIT'                       ,'NOWAIT',0,]
,['K_NULLS'                        ,'NULLS',0,]
,['K_NUMBER'                       ,'NUMBER',0,]
,['K_NVARCHAR'                     ,'NVARCHAR',0,]
,['K_OFFSET'                       ,'OFFSET',0,]
,['K_OJ'                           ,'OJ',0,]
,['K_OLD'                          ,'OLD',0,]
,['K_ONE'                          ,'ONE',0,]
,['K_ONLY'                         ,'ONLY',0,]
,['K_OPEN'                         ,'OPEN',0,]
,['K_OPTIONAL'                     ,'OPTIONAL',0,]
,['K_OPTIONS'                      ,'OPTIONS',0,]
,['K_ORDINALITY'                   ,'ORDINALITY',0,]
,['K_ORGANIZATION'                 ,'ORGANIZATION',0,]
,['K_OTHERS'                       ,'OTHERS',0,]
,['K_OWNER'                        ,'OWNER',0,]
,['K_PACK_KEYS'                    ,'PACK_KEYS',0,]
,['K_PAGE'                         ,'PAGE',0,]
,['K_PARSER'                       ,'PARSER',0,]
,['K_PARTIAL'                      ,'PARTIAL',0,]
,['K_PARTITIONING'                 ,'PARTITIONING',0,]
,['K_PARTITIONS'                   ,'PARTITIONS',0,]
,['K_PASSWORD'                     ,'PASSWORD',0,]
,['K_PATH'                         ,'PATH',0,]
,['K_PERSIST'                      ,'PERSIST',0,]
,['K_PERSIST_ONLY'                 ,'PERSIST_ONLY',0,]
,['K_PHASE'                        ,'PHASE',0,]
,['K_PLUGIN'                       ,'PLUGIN',0,]
,['K_PLUGIN_DIR'                   ,'PLUGIN_DIR',0,]
,['K_PLUGINS'                      ,'PLUGINS',0,]
,['K_POINT'                        ,'POINT',0,]
,['K_POLYGON'                      ,'POLYGON',0,]
,['K_PORT'                         ,'PORT',0,]
,['K_PRECEDES'                     ,'PRECEDES',0,]
,['K_PRECEDING'                    ,'PRECEDING',0,]
,['K_PREPARE'                      ,'PREPARE',0,]
,['K_PRESERVE'                     ,'PRESERVE',0,]
,['K_PREV'                         ,'PREV',0,]
,['K_PRIVILEGE_CHECKS_USER'        ,'PRIVILEGE_CHECKS_USER',0,]
,['K_PRIVILEGES'                   ,'PRIVILEGES',0,]
,['K_PROCESS'                      ,'PROCESS',0,]
,['K_PROCESSLIST'                  ,'PROCESSLIST',0,]
,['K_PROFILE'                      ,'PROFILE',0,]
,['K_PROFILES'                     ,'PROFILES',0,]
,['K_PROXY'                        ,'PROXY',0,]
,['K_QUARTER'                      ,'QUARTER',0,]
,['K_QUERY'                        ,'QUERY',0,]
,['K_QUICK'                        ,'QUICK',0,]
,['K_RANDOM'                       ,'RANDOM',0,]
,['K_READ_ONLY'                    ,'READ_ONLY',0,]
,['K_REBUILD'                      ,'REBUILD',0,]
,['K_RECOVER'                      ,'RECOVER',0,]
,['K_REDO_BUFFER_SIZE'             ,'REDO_BUFFER_SIZE',0,]
,['K_REDOFILE'                     ,'REDOFILE',0,]
,['K_REDUNDANT'                    ,'REDUNDANT',0,]
,['K_REFERENCE'                    ,'REFERENCE',0,]
,['K_RELAY'                        ,'RELAY',0,]
,['K_RELAYLOG'                     ,'RELAYLOG',0,]
,['K_RELAY_LOG_FILE'               ,'RELAY_LOG_FILE',0,]
,['K_RELAY_LOG_POS'                ,'RELAY_LOG_POS',0,]
,['K_RELAY_THREAD'                 ,'RELAY_THREAD',0,]
,['K_RELOAD'                       ,'RELOAD',0,]
,['K_REMOTE'                       ,'REMOTE',0,]
,['K_REMOVE'                       ,'REMOVE',0,]
,['K_REORGANIZE'                   ,'REORGANIZE',0,]
,['K_REPAIR'                       ,'REPAIR',0,]
,['K_REPEATABLE'                   ,'REPEATABLE',0,]
,['K_REPLICATE_DO_DB'              ,'REPLICATE_DO_DB',0,]
,['K_REPLICATE_DO_TABLE'           ,'REPLICATE_DO_TABLE',0,]
,['K_REPLICATE_IGNORE_DB'          ,'REPLICATE_IGNORE_DB',0,]
,['K_REPLICATE_IGNORE_TABLE'       ,'REPLICATE_IGNORE_TABLE',0,]
,['K_REPLICATE_REWRITE_DB'         ,'REPLICATE_REWRITE_DB',0,]
,['K_REPLICATE_WILD_DO_TABLE'      ,'REPLICATE_WILD_DO_TABLE',0,]
,['K_REPLICATE_WILD_IGNORE_TABLE'  ,'REPLICATE_WILD_IGNORE_TABLE',0,]
,['K_REPLICATION'                  ,'REPLICATION',0,]
,['K_REQUIRE_ROW_FORMAT'           ,'REQUIRE_ROW_FORMAT',0,]
,['K_RESET'                        ,'RESET',0,]
,['K_RESOURCE'                     ,'RESOURCE',0,]
,['K_RESPECT'                      ,'RESPECT',0,]
,['K_RESTART'                      ,'RESTART',0,]
,['K_RESTORE'                      ,'RESTORE',0,]
,['K_RESUME'                       ,'RESUME',0,]
,['K_RETAIN'                       ,'RETAIN',0,]
,['K_RETURNED_SQLSTATE'            ,'RETURNED_SQLSTATE',0,]
,['K_RETURNS'                      ,'RETURNS',0,]
,['K_REUSE'                        ,'REUSE',0,]
,['K_REVERSE'                      ,'REVERSE',0,]
,['K_ROLE'                         ,'ROLE',0,]
,['K_ROLLBACK'                     ,'ROLLBACK',0,]
,['K_ROLLUP'                       ,'ROLLUP',0,]
,['K_ROTATE'                       ,'ROTATE',0,]
,['K_ROUTINE'                      ,'ROUTINE',0,]
,['K_ROW_COUNT'                    ,'ROW_COUNT',0,]
,['K_ROW_FORMAT'                   ,'ROW_FORMAT',0,]
,['K_RTREE'                        ,'RTREE',0,]
,['K_SAVEPOINT'                    ,'SAVEPOINT',0,]
,['K_SCHEDULE'                     ,'SCHEDULE',0,]
,['K_SCHEMA_NAME'                  ,'SCHEMA_NAME',0,]
,['K_SECOND'                       ,'SECOND',0,]
,['K_SECONDARY'                    ,'SECONDARY',0,]
,['K_SECONDARY_ENGINE'             ,'SECONDARY_ENGINE',0,]
,['K_SECONDARY_LOAD'               ,'SECONDARY_LOAD',0,]
,['K_SECONDARY_UNLOAD'             ,'SECONDARY_UNLOAD',0,]
,['K_SECURITY'                     ,'SECURITY',0,]
,['K_SERIAL'                       ,'SERIAL',0,]
,['K_SERIALIZABLE'                 ,'SERIALIZABLE',0,]
,['K_SERVER'                       ,'SERVER',0,]
,['K_SESSION'                      ,'SESSION',0,]
,['K_SHARE'                        ,'SHARE',0,]
,['K_SHUTDOWN'                     ,'SHUTDOWN',0,]
,['K_SIGNED'                       ,'SIGNED',0,]
,['K_SIMPLE'                       ,'SIMPLE',0,]
,['K_SKIP'                         ,'SKIP',0,]
,['K_SLAVE'                        ,'SLAVE',0,]
,['K_SLOW'                         ,'SLOW',0,]
,['K_SNAPSHOT'                     ,'SNAPSHOT',0,]
,['K_SOCKET'                       ,'SOCKET',0,]
,['K_SOME'                         ,'SOME',0,]
,['K_SONAME'                       ,'SONAME',0,]
,['K_SOUNDS'                       ,'SOUNDS',0,]
,['K_SOURCE'                       ,'SOURCE',0,]
,['K_SQL_AFTER_GTIDS'              ,'SQL_AFTER_GTIDS',0,]
,['K_SQL_AFTER_MTS_GAPS'           ,'SQL_AFTER_MTS_GAPS',0,]
,['K_SQL_BEFORE_GTIDS'             ,'SQL_BEFORE_GTIDS',0,]
,['K_SQL_BUFFER_RESULT'            ,'SQL_BUFFER_RESULT',0,]
,['K_SQL_CACHE'                    ,'SQL_CACHE',0,]
,['K_SQL_NO_CACHE'                 ,'SQL_NO_CACHE',0,]
,['K_SQL_THREAD'                   ,'SQL_THREAD',0,]
,['K_SQL_TSI_DAY'                  ,'SQL_TSI_DAY',0,]
,['K_SQL_TSI_HOUR'                 ,'SQL_TSI_HOUR',0,]
,['K_SQL_TSI_MINUTE'               ,'SQL_TSI_MINUTE',0,]
,['K_SQL_TSI_MONTH'                ,'SQL_TSI_MONTH',0,]
,['K_SQL_TSI_QUARTER'              ,'SQL_TSI_QUARTER',0,]
,['K_SQL_TSI_SECOND'               ,'SQL_TSI_SECOND',0,]
,['K_SQL_TSI_WEEK'                 ,'SQL_TSI_WEEK',0,]
,['K_SQL_TSI_YEAR'                 ,'SQL_TSI_YEAR',0,]
,['K_SRID'                         ,'SRID',0,]
,['K_STACKED'                      ,'STACKED',0,]
,['K_START'                        ,'START',0,]
,['K_STARTS'                       ,'STARTS',0,]
,['K_STATS_AUTO_RECALC'            ,'STATS_AUTO_RECALC',0,]
,['K_STATS_PERSISTENT'             ,'STATS_PERSISTENT',0,]
,['K_STATS_SAMPLE_PAGES'           ,'STATS_SAMPLE_PAGES',0,]
,['K_STATUS'                       ,'STATUS',0,]
,['K_STOP'                         ,'STOP',0,]
,['K_STORAGE'                      ,'STORAGE',0,]
,['K_STRING'                       ,'STRING',0,]
,['K_SUBCLASS_ORIGIN'              ,'SUBCLASS_ORIGIN',0,]
,['K_SUBJECT'                      ,'SUBJECT',0,]
,['K_SUBPARTITION'                 ,'SUBPARTITION',0,]
,['K_SUBPARTITIONS'                ,'SUBPARTITIONS',0,]
,['K_SUPER'                        ,'SUPER',0,]
,['K_SUSPEND'                      ,'SUSPEND',0,]
,['K_SWAPS'                        ,'SWAPS',0,]
,['K_SWITCHES'                     ,'SWITCHES',0,]
,['K_TABLE_CHECKSUM'               ,'TABLE_CHECKSUM',0,]
,['K_TABLE_NAME'                   ,'TABLE_NAME',0,]
,['K_TABLES'                       ,'TABLES',0,]
,['K_TABLESPACE'                   ,'TABLESPACE',0,]
,['K_TEMPORARY'                    ,'TEMPORARY',0,]
,['K_TEMPTABLE'                    ,'TEMPTABLE',0,]
,['K_TEXT'                         ,'TEXT',0,]
,['K_THAN'                         ,'THAN',0,]
,['K_THREAD_PRIORITY'              ,'THREAD_PRIORITY',0,]
,['K_TIES'                         ,'TIES',0,]
,['K_TIME'                         ,'TIME',0,]
,['K_TIMESTAMP'                    ,'TIMESTAMP',0,]
,['K_TIMESTAMPADD'                 ,'TIMESTAMPADD',0,]
,['K_TIMESTAMPDIFF'                ,'TIMESTAMPDIFF',0,]
,['K_TRANSACTION'                  ,'TRANSACTION',0,]
,['K_TRIGGERS'                     ,'TRIGGERS',0,]
,['K_TRUNCATE'                     ,'TRUNCATE',0,]
,['K_TYPE'                         ,'TYPE',0,]
,['K_TYPES'                        ,'TYPES',0,]
,['K_UNBOUNDED'                    ,'UNBOUNDED',0,]
,['K_UNCOMMITTED'                  ,'UNCOMMITTED',0,]
,['K_UNDEFINED'                    ,'UNDEFINED',0,]
,['K_UNDO_BUFFER_SIZE'             ,'UNDO_BUFFER_SIZE',0,]
,['K_UNDOFILE'                     ,'UNDOFILE',0,]
,['K_UNICODE'                      ,'UNICODE',0,]
,['K_UNINSTALL'                    ,'UNINSTALL',0,]
,['K_UNKNOWN'                      ,'UNKNOWN',0,]
,['K_UNTIL'                        ,'UNTIL',0,]
,['K_UPGRADE'                      ,'UPGRADE',0,]
,['K_USE_FRM'                      ,'USE_FRM',0,]
,['K_USER'                         ,'USER',0,]
,['K_USER_RESOURCES'               ,'USER_RESOURCES',0,]
,['K_VALIDATION'                   ,'VALIDATION',0,]
,['K_VALUE'                        ,'VALUE',0,]
,['K_VARIABLES'                    ,'VARIABLES',0,]
,['K_VCPU'                         ,'VCPU',0,]
,['K_VIEW'                         ,'VIEW',0,]
,['K_VISIBLE'                      ,'VISIBLE',0,]
,['K_WAIT'                         ,'WAIT',0,]
,['K_WARNINGS'                     ,'WARNINGS',0,]
,['K_WEEK'                         ,'WEEK',0,]
,['K_WEIGHT_STRING'                ,'WEIGHT_STRING',0,]
,['K_WITHOUT'                      ,'WITHOUT',0,]
,['K_WORK'                         ,'WORK',0,]
,['K_WRAPPER'                      ,'WRAPPER',0,]
,['K_X509'                         ,'X509',0,]
,['K_XA'                           ,'XA',0,]
,['K_XID'                          ,'XID',0,]
,['K_XML'                          ,'XML',0,]
,['K_YEAR'                         ,'YEAR',0,]

,['D_NEW_LINE'                     ,'\n',1,]
,['D_TAB'                          ,'\t',1,]
,['D_SPACE'                        ,' ',1,]
,['D_COMMA'                        ,',',1,]
,['D_PERIOD'                       ,'.',1,]
,['D_DOLLAR'                       ,'$',1,]
,['D_UNDERSCORE'                   ,'_',1,]


,['N_ZERO'                         ,'0',1,]
,['N_ONE'                          ,'1',1,]
,['N_TWO'                          ,'2',1,]
,['N_THREE'                        ,'3',1,]
,['N_FOUR'                         ,'4',1,]
,['N_FIVE'                         ,'5',1,]
,['N_SIX'                          ,'6',1,]
,['N_SEVEN'                        ,'7',1,]
,['N_EIGHT'                        ,'8',1,]
,['N_NINE'                         ,'9',1,]

,['A_a'                            ,'a',1,]
,['A_b'                            ,'b',1,]
,['A_c'                            ,'c',1,]
,['A_d'                            ,'d',1,]
,['A_e'                            ,'e',1,]
,['A_f'                            ,'f',1,]
,['A_g'                            ,'g',1,]
,['A_h'                            ,'h',1,]
,['A_i'                            ,'i',1,]
,['A_j'                            ,'j',1,]
,['A_k'                            ,'k',1,]
,['A_l'                            ,'l',1,]
,['A_m'                            ,'m',1,]
,['A_n'                            ,'n',1,]
,['A_o'                            ,'o',1,]
,['A_p'                            ,'p',1,]
,['A_q'                            ,'q',1,]
,['A_r'                            ,'r',1,]
,['A_s'                            ,'s',1,]
,['A_t'                            ,'t',1,]
,['A_u'                            ,'u',1,]
,['A_v'                            ,'v',1,]
,['A_w'                            ,'w',1,]
,['A_x'                            ,'x',1,]
,['A_y'                            ,'y',1,]
,['A_z'                            ,'z',1,]
,['A_A'                            ,'A',1,]
,['A_B'                            ,'B',1,]
,['A_C'                            ,'C',1,]
,['A_D'                            ,'D',1,]
,['A_E'                            ,'E',1,]
,['A_F'                            ,'F',1,]
,['A_G'                            ,'G',1,]
,['A_H'                            ,'H',1,]
,['A_I'                            ,'I',1,]
,['A_J'                            ,'J',1,]
,['A_K'                            ,'K',1,]
,['A_L'                            ,'L',1,]
,['A_M'                            ,'M',1,]
,['A_N'                            ,'N',1,]
,['A_O'                            ,'O',1,]
,['A_P'                            ,'P',1,]
,['A_Q'                            ,'Q',1,]
,['A_R'                            ,'R',1,]
,['A_S'                            ,'S',1,]
,['A_T'                            ,'T',1,]
,['A_U'                            ,'U',1,]
,['A_V'                            ,'V',1,]
,['A_W'                            ,'W',1,]
,['A_X'                            ,'X',1,]
,['A_Y'                            ,'Y',1,]
,['A_Z'                            ,'Z',1,]

,['B_DOUBLE_QUOTE'                 ,'"',1,]
,['B_SINGLE_QUOTE'                 ,'\'',1,]
,['B_BACK_TIC'                     ,'`',1,]
,['B_LEFT_COMMENT'                 ,'/*',1,]
,['B_RIGHT_COMMENT'                ,'*/',1,]
,['B_COMMENT_SINGLE'               ,'--',1,]
,['B_LEFT_PAREN'                   ,'(',1,]
,['B_RIGHT_PAREN'                  ,')',1,]


,['O_NULL_SAFE_EQUALS'             ,'<=>',1,]
,['O_PLUS_EQUALS'                  ,'+=',1,]
,['O_MINUS_EQUALS'                 ,'-=',1,]
,['O_MULTIPLY_EQUALS'              ,'*=',1,]
,['O_DIVIDE_EQUALS'                ,'/=',1,]
,['O_MODULUS_EQUALS'               ,'%=',1,]
,['O_GREATER_THAN_EQUALS'          ,'>=',1,]
,['O_LESS_THAN_EQUALS'             ,'<=',1,]
,['O_EQUALS'                       ,'==',1,]
,['O_NOT_EQUALS'                   ,'!=',1,]
,['O_NOT_EQUALS'                   ,'<>',1,]
,['O_OR_EQUALS'                    ,'|=',1,]
,['O_AND_EQUALS'                   ,'&=',1,]
,['O_XOR_EQUALS'                   ,'^=',1,]
,['O_SET'                          ,'=:',1,]

,['O_SHORT_CIRCUIT_OR'             ,'||',1,]
,['O_SHORT_CIRCUIT_AND'            ,'&&',1,]
,['O_BITWISE_LEFT'                 ,'<<',1,]
,['O_BITWISE_RIGHT'                ,'>>',1,]
,['O_BITWISE_INVERSION'            ,'~',1,]

,['O_PLUS'                         ,'+',1,]
,['O_MINUS'                        ,'-',1,]
,['O_MULTIPLY'                     ,'*',1,]
,['O_DIVIDE'                       ,'/',1,]
,['O_MODULUS'                      ,'%',1,]
,['O_GREATER_THAN'                 ,'>',1,]
,['O_LESS_THAN'                    ,'<',1,]
,['O_ASIGN'                        ,'=',1,]
,['O_NEGATE'                       ,'!',1,]
,['O_OR'                           ,'|',1,]
,['O_AND'                          ,'&',1,]
,['O_XOR'                          ,'^',1,]

]



print """import timeit

### ----                                     ----
### ddb BYTECODE LANGUAGE DEFINITIONS
### ----                                     ----
### Automagically generated, dont mess with this.
### ----  or you will be eaten by unicorns   ----
### ----                                     ----

# each word is given an integer value based on section, sections increment based on SECTION BLOCK_VALUE

# T=text
# R=Reserved word
# K=Key word
# B=Block    such as comment, text or code
# O=Operator

# comparisons are ordered to be done in greatest length order, to prevent uneven length but similar values
# this also doubles as a speed enhancement




"""



###
###  Template out constant values
###


order="BRKONAD"
section_index=SECTION_BLOCK_START
    
index=0
for section in order:

    index=section_index
    for item in words:
        if item[2]==1:
            if item[0][0]==section:
                item.append(index)
                index+=1
    section_index+=SECTION_BLOCK_INCREMENT



print("")
print("#")
print("# Integer Values")
print("#")
print("")
    
for section in order:
    print("")
    if section=="O":
        print("# OPERATOR")
    if section=="B":
        print("# BLOCK")
    if section=="R":
        print("# RESERVED WORD")
    if section=="K":
        print("# KEYWORD")
    if section=="T":
        print("# TEXT")
    if section=="A":
        print("# Alpha")
    if section=="N":
        print("# Numeric")
    if section=="D":
        print("# Delimiter")
    print("")

    for item in words:
        if item[2]==1:
            if item[0][0]==section:
                print item[0][2:]+'='+str(item[3])

###
###  Template out constant strings
###

    
print("")
print("#")
print("# String Values")
print("#")
print("")

index=0
for section in order:
    print("")
    if section=="O":
        print("# OPERATOR")
    if section=="B":
        print("# BLOCK")
    if section=="R":
        print("# RESERVED WORD")
    if section=="K":
        print("# KEYWORD")
    if section=="T":
        print("# TEXT")
    if section=="A":
        print("# Alpha")
    if section=="N":
        print("# Numeric")
    if section=="D":
        print("# Delimiter")
    print("")    

    for item in words:
        if item[2]==1:
            if item[0][0]==section:
                print item[0][2:]+'_STR='+repr(item[1])
    

print("")
print("#")
print("# Code")
print("#")
print("")


###
###  Template identifyer for python 2/3
###

for version in range(2,4):

    print """
def get_intermediate_code_"""+str(version)+"""(text):
    if text==None: return 0
    text=text.upper()
    text_length=len(text)
    text_hash=hash(text)
    if   text=='': return 0 

    """

    max_len=0
    lengths={}
    for item in words:
        word_length=len(item[1])
        if word_length>max_len: 
            max_len=word_length
            lengths[max_len]=max_len

    if_type="if  "

    for length in range(max_len,0,-1):

        found_word=None
        for item in words:

            word_length=len(item[1])
            if item[2]!=1 or word_length!=length:    
                continue
            found_word=True
        if found_word==None: continue

        print "    "+if_type+" text_length=="+str(length)+":"
        
        if_type="elif"
        sub_if_type="if  "


        for item in words:
            word_length=len(item[1])
            if item[0][0]=='N' or  item[0][0]=='A': continue
            if word_length!=length:    
                continue

            if item[2]==1:
                if version==2:
                    print "        "+sub_if_type+" text_hash=="+str(hash(item[1]) )+": return "+str(item[3] )
                else:
                    print "        "+sub_if_type+" text=="+repr (item[1]) + ": return "+str(item[3] )
                sub_if_type="elif"
    print "    return 0"
        
print """
def add_fragment(fragment,fragment_length,bulk=None,depth=0):
    new_fragments=[]
    if bulk:
        if fragment!="":
            new_fragments.append([fragment,0,depth])
    else:
        if fragment!="":
            right_fragment=""
            right_fragment_length=0
    
            while fragment_length>0:
                found=0
                for length in range(fragment_length,0,-1):
                    code=get_intermediate_code_2(fragment[:length])
                    if code!=0:
                        found=True
                        if code==SPACE or code==TAB or code==NEW_LINE:
                            pass
                        else:
                            new_fragments.append([fragment[:length],code,depth])
                        fragment_length-=length
                        if fragment_length>0:
                            fragment=fragment[length:]
                        break;
                
                # if we looped through all length combiniations and found nothing, add the remainder and shrink the stack
                if found==0:
                    new_fragments.append([fragment[0],0,depth])
                    fragment_length-=1
                    if fragment_length>0:
                        fragment=fragment[1:]
    return new_fragments
   

def get_BYTECODE(data,depth=0):
    #print data
    fragments=[]
    fragment=""
    fragment_length=0
 
    in_block=None
    in_alpha=None
    block_depth=0

    # main loop for tokenizing
    for c in data:
        if in_block:
            in_alpha=None
            # is it the other side of the block
            if c==LEFT_PAREN_STR:      
                block_depth+=1
                fragment+=c
                fragment_length+=1
                continue

            if c==in_block:
                
                if in_block==RIGHT_PAREN_STR:
                    #print block_depth
                    block_depth-=1
                    if block_depth!=0:
                        fragment+=c
                        fragment_length+=1
                        continue
                    pass
                    sub_code=get_BYTECODE(fragment,depth+1)
                    fragments+=sub_code
                else:
                    fragments+=add_fragment(fragment,fragment_length,True,depth)
                fragment=""
                fragment_length=0
                in_block=None
                #block_depth=0
            # no, add the contents
            else:
                fragment+=c
                fragment_length+=1
        else:
            # self closing
            if   c==DOUBLE_QUOTE_STR:    in_block=DOUBLE_QUOTE_STR
            elif c==SINGLE_QUOTE_STR:    in_block=SINGLE_QUOTE_STR
            elif c==BACK_TIC_STR:        in_block=BACK_TIC_STR
            
            # matched pair
            elif c==LEFT_COMMENT_STR:    in_block=RIGHT_COMMENT_STR
            elif c==COMMENT_SINGLE_STR:  in_block=NEW_LINE_STR
            elif c==LEFT_PAREN_STR:      
                in_block=RIGHT_PAREN_STR
                
                block_depth+=1
                
                
    
            if in_block:
                fragments+=add_fragment(fragment,fragment_length,None,depth)
                fragment=""
                fragment_length=0
                continue
            
    
            #not a block, or anything else
            else:
                # is this the start of an "WORD"
                if in_alpha==None:
                    if ( c>=A_STR and c<=Z_STR ) or ( c>=a_STR and c<=z_STR ) or ( c>=ZERO_STR and c<=NINE_STR ) or c== UNDERSCORE_STR or c==DOLLAR_STR:
                        fragments+=add_fragment(fragment,fragment_length,None,depth)
                        fragment=c
                        fragment_length=1
                        in_alpha=True

                    # not in a word, none word zone stuff..
                    else:
                        fragment+=c
                        fragment_length+=1

                # Are we in a "WORD"
                else:
                    # If we just LEFT ... add the existing word, and start a new one
                    if not ( c>=A_STR and c<=Z_STR ) and  not ( c>=a_STR and c<=z_STR ) and not ( c>=ZERO_STR and c<=NINE_STR ) and c!=UNDERSCORE_STR and  c!=DOLLAR_STR:
                        fragments+=add_fragment(fragment,fragment_length,True,depth)
                        fragment=c
                        fragment_length=1
                        in_alpha=None

                    # IF SO append
                    else:
                        fragment+=c
                        fragment_length+=1

    # END Loop                
    
    # if anything is still left in the pipeline, cleanup
    
    fragments+=add_fragment(fragment,fragment_length,in_alpha,depth)
    fragment=""
    fragment_length=0


    # err if block mismatch
    if in_block:
        err_msg="Missing {0}".format(in_block)
        raise Exception(err_msg)
    
    # reduce groups that are single elements
    
    
    #while len(fragments)==1:
        #print fragments
        #eif isinstance(fragments,dict):
        #    fragments=fragments['sub']
    #    print fragments
    #    return fragments
    
    return [{"sub":fragments}]
   

def print_code(codes,root=True):
    
    if isinstance(codes,list):
        for code in codes:
            if isinstance(code,dict):
                print_code(code['sub'],None)
            elif isinstance(code,list):
                for i in range(code[2]):
                    print " " , 
                print(code)
    

def test(debug=None):
    codes=get_BYTECODE("SELECT * FROM (PIZ (((o ber )) && == ZAZ) )(hh.'hh')  (f) 'db blah 432%^$#@'.\\"rfdsf table\\" where  && || | >= == &&& === this=that and that not 5")
    if debug: print_code(codes) 


#print(timeit.timeit(test, number=10))

test(True)

"""