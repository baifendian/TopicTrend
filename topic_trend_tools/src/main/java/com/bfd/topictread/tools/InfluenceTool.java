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

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;
import java.util.Map;

import com.bfd.topictread.tools.common.PropertiesConfiguration;
import com.bfd.topictread.tools.dao.DataSourceDao;
import com.bfd.topictread.tools.dao.RecordDao;
import com.bfd.topictread.tools.model.NewsAgg;
import com.bfd.topictread.tools.model.WeiboAgg;
import com.bfd.topictread.tools.model.WeixinAgg;

/**
 * 事件影响力分析工具
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class InfluenceTool {
    /** 配置文件路径 */
    private static final String CONFIG_PATH = "classpath:config.properties";

    /**
     * main
     * <p>
     * 
     * @param args
     */
    public static void main(String[] args) {
        // 加载配置文件
        PropertiesConfiguration.load(new String[] { CONFIG_PATH });

        // mongodb连接字符串
        String mongoConStr = PropertiesConfiguration.getValue("mongodb.constr", "");

        // 获取日期（默认计算昨天的数据）
        String dateString;
        if (args != null && args.length > 0) {
            dateString = args[0];
        } else {
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
            Calendar calendar = Calendar.getInstance();
            calendar.add(Calendar.DAY_OF_MONTH, -1); // 昨天
            dateString = simpleDateFormat.format(calendar.getTime());
        }

        // dateString = "2016-07-08";

        System.out.println("***********开始计算事件的影响力");
        System.out.println("***********日期：dateString");

        // 获取事件相关源数据（一天）
        DataSourceDao sourceDao = new DataSourceDao(mongoConStr);
        List<WeiboAgg> weiboAggs = sourceDao.obtainWeiboAggByDay(dateString);
        List<WeixinAgg> weixinAggs = sourceDao.obtainWeixinAggByDay(dateString);
        List<NewsAgg> newsAggs = sourceDao.obtainNewsAggByDay(dateString);

        // 计算事件影响力
        Map<String, Double> influenceMap = InfluenceCalc.calcInfluence(weiboAggs, weixinAggs, newsAggs);
        System.out.println("***********计算完毕!");
        System.out.println("***********事件总数：" + influenceMap.size());
        // System.out.println(influenceMap);

        // 存储事件影响力
        System.out.println("***********开始存储事件的影响力");
        RecordDao recordDao = new RecordDao(mongoConStr);
        recordDao.insertInfluence(dateString, influenceMap);
        System.out.println("***********存储完成，已存入mongodb中！");
    }
}
