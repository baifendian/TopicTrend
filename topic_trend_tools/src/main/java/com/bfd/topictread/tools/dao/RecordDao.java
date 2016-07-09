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

package com.bfd.topictread.tools.dao;

import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import com.bfd.topictread.tools.utils.MongoWrapper;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

/**
 * 记录表Dao
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class RecordDao {
    /** 记录表 */
    private static final String COLLECTION_RECORD_NAME = "record";

    /** Mongo client */
    private final MongoWrapper mongoWrapper;

    public RecordDao(String connectString) {
        mongoWrapper = new MongoWrapper(connectString);
    }

    /**
     * 插入影响力数据
     * <p>
     */
    public void insertInfluence(String date, Map<String, Double> influenceMap) {

        Set<Entry<String, Double>> entries = influenceMap.entrySet();
        for (Entry<String, Double> entry : entries) {
            BasicDBObject query = new BasicDBObject();
            query.put("date", date);
            query.put("event_id", entry.getKey());

            DBObject udata = new BasicDBObject();
            udata.put("influence", entry.getValue().intValue());

            DBObject data = new BasicDBObject();
            data.put("$set", udata);
            mongoWrapper.update(COLLECTION_RECORD_NAME, query, data);
        }

    }
}
