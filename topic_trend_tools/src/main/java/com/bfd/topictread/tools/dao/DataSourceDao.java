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
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.bfd.topictread.tools.model.NewsAgg;
import com.bfd.topictread.tools.model.WeiboAgg;
import com.bfd.topictread.tools.model.WeixinAgg;
import com.bfd.topictread.tools.utils.MongoWrapper;
import com.mongodb.DBObject;

/**
 * 源数据Dao
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class DataSourceDao {
    /** 微信 */
    private static final String COLLECTION_WEIXIN_NAME = "weixin";

    /** 微博 */
    private static final String COLLECTION_WEIBO_NAME = "weibo";

    /** 新闻 */
    private static final String COLLECTION_NEWS_NAME = "news";

    /** Mongo client */
    private final MongoWrapper mongoWrapper;

    public DataSourceDao(String connectString) {
        mongoWrapper = new MongoWrapper(connectString);
    }

    /**
     * 获取所有微博信息的数据
     * <p>
     * 
     * @return
     */
    public List<WeiboAgg> obtainWeiboAggByDay(String date) {
        List<WeiboAgg> weiboAggs = new ArrayList<WeiboAgg>();
        List<String> sumFields = Arrays.asList("comment", "like", "transmit");
        Map<String, Object> matchMap = new HashMap<String, Object>();
        matchMap.put("date", date);
        List<DBObject> results = mongoWrapper.aggregateSum(COLLECTION_WEIBO_NAME, "event_id", sumFields, matchMap);
        for (DBObject dbObject : results) {
            if (dbObject.get("_id") != null) {
                WeiboAgg agg = new WeiboAgg();
                agg.setEventId(dbObject.get("_id").toString());
                agg.setTotal(Long.valueOf(dbObject.get("total").toString()));
                agg.setTotalComment(Long.valueOf(dbObject.get("total1").toString()));
                agg.setTotalLike(Long.valueOf(dbObject.get("total2").toString()));
                agg.setTotalTransmit(Long.valueOf(dbObject.get("total3").toString()));
                weiboAggs.add(agg);
            }
        }
        return weiboAggs;
    }

    /**
     * 获取所有微信信息的数据
     * <p>
     * 
     * @return
     */
    public List<WeixinAgg> obtainWeixinAggByDay(String date) {
        List<WeixinAgg> weixinAggs = new ArrayList<WeixinAgg>();
        List<String> sumFields = Arrays.asList("read");
        Map<String, Object> matchMap = new HashMap<String, Object>();
        matchMap.put("date", date);
        List<DBObject> results = mongoWrapper.aggregateSum(COLLECTION_WEIXIN_NAME, "event_id", sumFields, matchMap);
        for (DBObject dbObject : results) {
            if (dbObject.get("_id") != null) {
                WeixinAgg agg = new WeixinAgg();
                agg.setEventId(dbObject.get("_id").toString());
                agg.setTotal(Long.valueOf(dbObject.get("total").toString()));
                agg.setTotalRead(Long.valueOf(dbObject.get("total1").toString()));
                weixinAggs.add(agg);
            }
        }
        return weixinAggs;
    }

    /**
     * 获取所有新闻信息的数据
     * <p>
     * 
     * @return
     */
    public List<NewsAgg> obtainNewsAggByDay(String date) {
        List<NewsAgg> newsAggs = new ArrayList<NewsAgg>();
        Map<String, Object> matchMap = new HashMap<String, Object>();
        matchMap.put("date", date);
        List<DBObject> results = mongoWrapper.aggregateSum(COLLECTION_NEWS_NAME, "event_id", null, matchMap);
        for (DBObject dbObject : results) {
            if (dbObject.get("_id") != null) {
                NewsAgg agg = new NewsAgg();
                agg.setEventId(dbObject.get("_id").toString());
                agg.setTotal(Long.valueOf(dbObject.get("total").toString()));
                newsAggs.add(agg);
            }
        }
        return newsAggs;
    }

}
