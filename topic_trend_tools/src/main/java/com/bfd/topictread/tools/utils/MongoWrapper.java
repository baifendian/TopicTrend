/**
 * Copyright (C) 2015 Baifendian Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.bfd.topictread.tools.utils;

import static java.util.Arrays.asList;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.mongodb.AggregationOutput;
import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.ReadPreference;
import com.mongodb.WriteConcern;

/**
 * 对MongoClient的封装。<br />
 * 建议对一个MongoDB实例在全局维护一个MongoWrapper对象来提高性能，<br />
 * 因为 MongoPool.getMongoClient(config);是同步的。
 * 
 * @author dsfan
 */
public class MongoWrapper {

    private final MongoClient client;

    private final DB db;

    private MongoConfig config;

    public MongoWrapper(String url) {
        parseUrl(url);
        client = MongoPool.getMongoClient(config);
        db = client.getDB(config.getDbName());
        Logger mongoLogger = Logger.getLogger("org.mongodb.driver");
        mongoLogger.setLevel(Level.OFF);
    }

    public String getHost() {
        return config.getHost();
    }

    public int getPort() {
        return config.getPort();
    }

    public String getDbName() {
        return config.getDbName();
    }

    /**
     * 安全插入
     * 
     * @param collName
     *            collection 名称
     * @param obj
     *            对象
     * @throws Exception
     */
    public void insertSafe(String collName, DBObject obj) throws Exception {
        DBCollection coll = db.getCollection(collName);
        // WriterConcern.SAFE 模式，即w=1；这种配置意味着客户端在插入数据或更新数据的时候，要求 mongodb
        // 必须将所更新的数据写入磁盘并返回更新成功的信息给程序。
        // 如果碰上应用程序访问压力大，mongodb 就会反应迟钝，并可能会假死。
        // 针对此情况，需要评估数据的一致性需求，做出合适调整。
        coll.insert(obj, WriteConcern.SAFE);
    }

    /**
     * 批量插入
     * 
     * @param collName
     * @param objList
     *            插入对象的列表
     * @throws Exception
     */
    public void insertSafe(String collName, List<DBObject> objList) throws Exception {
        DBCollection coll = db.getCollection(collName);
        coll.insert(objList, WriteConcern.SAFE);
    }

    /**
     * 查找
     * 
     * @param collName
     * @param query
     * @param orderBy
     * @return
     */
    public DBObject findOne(String collName, DBObject query) {
        DBCollection coll = db.getCollection(collName);
        return coll.findOne(query);
    }

    /**
     * 查找
     * 
     * @param collName
     * @param query
     * @return
     */
    public List<DBObject> find(String collName, DBObject query) {
        DBCollection coll = db.getCollection(collName);
        List<DBObject> dbObjects = new ArrayList<DBObject>();
        DBCursor dbCursor = coll.find(query);
        if (dbCursor != null) {
            while (dbCursor.hasNext()) {
                dbObjects.add(dbCursor.next());
            }
            dbCursor.close();
        }
        return dbObjects;
    }

    /**
     * 更新
     * 
     * @param collName
     * @param query
     * @param object
     */
    public void update(String collName, DBObject query, DBObject object) {
        DBCollection coll = db.getCollection(collName);
        coll.update(query, object);
    }

    /**
     * 聚集操作sum
     * <p>
     * 
     * @param collName
     * @param groupField
     * @param sumField
     * @param matchMap
     * @return 聚集结果
     */
    public List<DBObject> aggregateSum(String collName, String groupField, List<String> sumFields, Map<String, Object> matchMap) {
        DBCollection coll = db.getCollection(collName);
        AggregationOutput output = null;
        BasicDBObject dbObject = new BasicDBObject("_id", "$" + groupField);
        dbObject.append("total", new BasicDBObject("$sum", 1));
        if (sumFields != null) {
            int i = 1;
            for (String field : sumFields) {
                dbObject.append("total" + i++, new BasicDBObject("$sum", "$" + field));
            }
        }

        BasicDBObject group = new BasicDBObject("$group", dbObject);

        if (matchMap != null) {
            Set<Entry<String, Object>> entrySet = matchMap.entrySet();
            BasicDBObject basicDBObject = null;
            for (Entry<String, Object> entry : entrySet) {
                if (basicDBObject == null) {
                    basicDBObject = new BasicDBObject(entry.getKey(), entry.getValue());
                } else {
                    basicDBObject.append(entry.getKey(), entry.getValue());
                }
            }
            BasicDBObject match = new BasicDBObject("$match", basicDBObject);
            output = coll.aggregate(asList(match, group));
        } else {
            output = coll.aggregate(asList(group));
        }
        Iterable<DBObject> iterable = output.results();
        List<DBObject> dbObjects = new ArrayList<DBObject>();
        for (DBObject object : iterable) {
            dbObjects.add(object);
        }
        return dbObjects;
    }

    /**
     * 解析连接字符串
     * 
     * @param url
     */
    private void parseUrl(String url) {
        config = new MongoConfig();

        int index1 = url.indexOf(":");
        int index2 = url.lastIndexOf("/");
        int index3 = url.indexOf("?");

        if (index1 == -1 || index2 == -1) {
            throw new IllegalArgumentException("MongoDB连接字符串格式不正确！");
        }

        String part1 = url.substring(index1 + 3, index2);
        String part2 = url.substring(index2 + 1);

        if (index3 != -1) {
            part2 = url.substring(index2 + 1, index3);
        }

        if ((part1 != null && part1.trim().length() > 0) && (part2 != null && part2.trim().length() > 0)) {
            config.setDbName(part2);

            if (part1.contains(",")) {
                config.setReSet(true);
                String[] hostsInfo = part1.split(",");
                for (String hostAndPort : hostsInfo) {
                    String[] hostInfo = hostAndPort.split(":");
                    if (hostInfo.length == 2) {
                        config.getHosts().add(hostAndPort);
                    } else if (hostInfo.length == 1) {
                        config.setHost(hostAndPort + ":" + 27017);
                    } else {
                        throw new IllegalArgumentException("MongoDB连接字符串格式不正确！");
                    }
                }
            } else {
                String[] hostInfo = part1.split(":");
                if (hostInfo.length == 2) {
                    config.setHost(hostInfo[0]);
                    try {
                        config.setPort(Integer.parseInt(hostInfo[1]));
                    } catch (Exception e) {
                        throw new IllegalArgumentException("MongoDB连接字符串格式不正确：port格式不对！");
                    }
                } else if (hostInfo.length == 1) {
                    config.setHost(hostInfo[0]);
                } else {
                    throw new IllegalArgumentException("MongoDB连接字符串格式不正确！");
                }
            }

        } else {
            throw new IllegalArgumentException("MongoDB连接字符串格式不正确！");
        }

        if (index3 != -1) {
            // ?connectTimeout=1000&socketTimeout=1000&preference=secondary
            String paramsString = url.substring(index3 + 1);
            String[] pairs = paramsString.split("&");
            HashMap<String, String> params = new HashMap<String, String>();
            for (String str : pairs) {
                String[] tmp = str.split("=");
                if (tmp.length == 2) {
                    params.put(tmp[0], tmp[1]);
                }
            }

            if (params.size() > 0) {
                String connectTimeout = params.get("connectTimeout");
                String socketTimeout = params.get("socketTimeout");
                String preference = params.get("preference");
                String w = params.get("w");
                String wtimeout = params.get("wtimeout");
                String slaveOk = params.get("slaveOk");

                if (connectTimeout != null) {
                    config.setConnectTimeout(Integer.parseInt(connectTimeout));
                }

                if (socketTimeout != null) {
                    config.setSocketTimeout(Integer.parseInt(socketTimeout));
                }

                if (slaveOk != null && slaveOk.equals("true")) {
                    config.setSlaveOk(true);
                }

                if (w != null) {
                    config.setW(Integer.valueOf(w));
                }

                if (wtimeout != null) {
                    config.setWtimeout(Integer.valueOf(wtimeout));
                }

                if (preference != null) {
                    if (preference.equalsIgnoreCase("primaryPreferred")) {
                        config.setReadPreference(ReadPreference.primaryPreferred());
                    } else if (preference.equalsIgnoreCase("secondary")) {
                        config.setReadPreference(ReadPreference.secondary());
                    } else if (preference.equalsIgnoreCase("secondaryPreferred")) {
                        config.setReadPreference(ReadPreference.secondaryPreferred());
                    } else if (preference.equalsIgnoreCase("nearest")) {
                        config.setReadPreference(ReadPreference.nearest());
                    }
                }
            }
        }
    }
}
