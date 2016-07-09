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

import java.util.ArrayList;
import java.util.List;

import com.bfd.topictread.tools.model.EventInfo;
import com.bfd.topictread.tools.utils.MongoWrapper;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

/**
 * 事件表Dao
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class EventDao {
    /** 事件表 */
    private static final String COLLECTION_EVENT_NAME = "event";

    /** Mongo client */
    private final MongoWrapper mongoWrapper;

    public EventDao(String connectString) {
        mongoWrapper = new MongoWrapper(connectString);
    }

    /**
     * 获取所有事件
     * <p>
     * 
     * @return
     */
    public List<EventInfo> obtainAllEvent() {
        List<EventInfo> eventInfos = new ArrayList<EventInfo>();
        List<DBObject> results = mongoWrapper.find(COLLECTION_EVENT_NAME, new BasicDBObject());
        for (DBObject dbObject : results) {
            EventInfo eventInfo = new EventInfo();
            eventInfo.setId(dbObject.get("_id").toString());
            eventInfos.add(eventInfo);
        }
        return eventInfos;
    }
}
