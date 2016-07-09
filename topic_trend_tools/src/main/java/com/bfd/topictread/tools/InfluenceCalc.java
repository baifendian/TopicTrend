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

package com.bfd.topictread.tools;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import com.bfd.topictread.tools.common.PropertiesConfiguration;
import com.bfd.topictread.tools.model.InfluenceModel;
import com.bfd.topictread.tools.model.NewsAgg;
import com.bfd.topictread.tools.model.WeiboAgg;
import com.bfd.topictread.tools.model.WeixinAgg;

/**
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class InfluenceCalc {

    /**
     * 计算影响力
     * <p>
     * 
     * @param weiboAggs
     * @param weixinAggs
     * @param newsAggs
     * @return Map<String, Double>
     */
    public static Map<String, Double> calcInfluence(List<WeiboAgg> weiboAggs, List<WeixinAgg> weixinAggs, List<NewsAgg> newsAggs) {
        Map<String, InfluenceModel> influencemModelMap = new HashMap<String, InfluenceModel>();
        calcWeiboInfluence(weiboAggs, influencemModelMap);
        calcWeixinInfluence(weixinAggs, influencemModelMap);
        calcNewsInfluence(newsAggs, influencemModelMap);
        return calcTotalInfluence(influencemModelMap);
    }

    /**
     * 计算微博影响力
     * <p>
     * 
     * @param weiboAggs
     * @param influencemModelMap
     */
    private static void calcWeiboInfluence(List<WeiboAgg> weiboAggs, Map<String, InfluenceModel> influencemModelMap) {
        double a = PropertiesConfiguration.getValue("weibo.count.factor", 0.5);
        double b = PropertiesConfiguration.getValue("weibo.comment.factor", 0.3);
        double c = PropertiesConfiguration.getValue("weibo.like.factor", 0.05);
        double d = PropertiesConfiguration.getValue("weibo.transmit.factor", 0.15);
        for (WeiboAgg weiboAgg : weiboAggs) {
            double influence = 0.0;
            influence += weiboAgg.getTotal() * a;
            influence += weiboAgg.getTotalComment() * b;
            influence += weiboAgg.getTotalLike() * c;
            influence += weiboAgg.getTotalTransmit() * d;
            String eventId = weiboAgg.getEventId();
            if (influencemModelMap.containsKey(eventId)) {
                InfluenceModel model = influencemModelMap.get(eventId);
                model.setWeiboInfluence(influence);
            } else {
                InfluenceModel model = new InfluenceModel();
                model.setWeiboInfluence(influence);
                influencemModelMap.put(eventId, model);
            }
        }
    }

    /**
     * 计算微信影响力
     * <p>
     * 
     * @param weixinAggs
     * @param influencemModelMap
     */
    private static void calcWeixinInfluence(List<WeixinAgg> weixinAggs, Map<String, InfluenceModel> influencemModelMap) {
        double a = PropertiesConfiguration.getValue("weixin.count.factor", 0.5);
        double b = PropertiesConfiguration.getValue("weixin.read.factor", 0.5);
        for (WeixinAgg weixinAgg : weixinAggs) {
            double influence = 0.0;
            influence += weixinAgg.getTotal() * a;
            influence += weixinAgg.getTotalRead() * b;
            String eventId = weixinAgg.getEventId();
            if (influencemModelMap.containsKey(eventId)) {
                InfluenceModel model = influencemModelMap.get(eventId);
                model.setWeixinInfluence(influence);
            } else {
                InfluenceModel model = new InfluenceModel();
                model.setWeixinInfluence(influence);
                influencemModelMap.put(eventId, model);
            }
        }

    }

    /**
     * 计算新闻影响力
     * <p>
     * 
     * @param newsAggs
     * @param influencemModelMap
     */
    private static void calcNewsInfluence(List<NewsAgg> newsAggs, Map<String, InfluenceModel> influencemModelMap) {
        double a = PropertiesConfiguration.getValue("news.count.factor", 1.0);
        for (NewsAgg newsAgg : newsAggs) {
            double influence = 0.0;
            influence += newsAgg.getTotal() * a;
            String eventId = newsAgg.getEventId();
            if (influencemModelMap.containsKey(eventId)) {
                InfluenceModel model = influencemModelMap.get(eventId);
                model.setNewsInfluence(influence);
            } else {
                InfluenceModel model = new InfluenceModel();
                model.setNewsInfluence(influence);
                influencemModelMap.put(eventId, model);
            }
        }

    }

    /**
     * 计算总的影响力
     * <p>
     * 
     * @param influencemModelMap
     */
    private static Map<String, Double> calcTotalInfluence(Map<String, InfluenceModel> influencemModelMap) {
        Set<Entry<String, InfluenceModel>> entries = influencemModelMap.entrySet();
        Map<String, Double> influenceMap = new HashMap<String, Double>();
        for (Entry<String, InfluenceModel> entry : entries) {
            InfluenceModel model = entry.getValue();
            double a = PropertiesConfiguration.getValue("weibo.factor", 0.4);
            double b = PropertiesConfiguration.getValue("weixin.factor", 0.3);
            double c = PropertiesConfiguration.getValue("news.factor", 0.3);
            double influence = 0.0;
            influence += model.getWeiboInfluence() * a;
            influence += model.getWeixinInfluence() * b;
            influence += model.getNewsInfluence() * c;
            influenceMap.put(entry.getKey(), influence);
        }
        return influenceMap;
    }

}
