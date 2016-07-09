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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientOptions;
import com.mongodb.ReadPreference;
import com.mongodb.ServerAddress;
import com.mongodb.WriteConcern;

/**
 * Mongdb连接池
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class MongoPool {
    // 一个host:port只创建一个MongoClient
    private volatile static Map<String, MongoClient> pools = new HashMap<String, MongoClient>();

    private static Object syncObject = new Object();

    private MongoPool() {
    }

    public static MongoClient getMongoClient(MongoConfig config) {
        synchronized (syncObject) {
            String key = "";
            if (config.isReSet()) {
                for (String host : config.getHosts()) {
                    key = key + host + "_";
                }
                key = key.substring(0, key.lastIndexOf("_"));
                if (!pools.containsKey(key)) {
                    pools.put(key, createReSetInstance(config));
                } else if (pools.get(key) == null) {
                    pools.put(key, createReSetInstance(config));
                }
            } else {
                key = config.getHost() + ":" + config.getPort();
                if (!pools.containsKey(key)) {
                    pools.put(key, createInstance(config));
                } else if (pools.get(key) == null) {
                    pools.put(key, createInstance(config));
                }
            }
            return pools.get(key);
        }
    }

    private static MongoClient createInstance(MongoConfig config) {
        MongoClient client = null;

        // MongoClientOptions源码：https://github.com/mongodb/mongo-java-driver/blob/master/src/main/com/mongodb/MongoClientOptions.java

        MongoClientOptions.Builder builder = new MongoClientOptions.Builder();
        builder.connectTimeout(config.getConnectTimeout());
        builder.socketTimeout(config.getSocketTimeout());
        builder.connectionsPerHost(100);

        if (config.isSlaveOk())
            builder.readPreference(ReadPreference.secondary());

        MongoClientOptions options = builder.build();
        client = new MongoClient(new ServerAddress(config.getHost(), config.getPort()), options);

        // mongodb-java-driver 的连接池，目前从观察到的情况是应用一开启便根据 connectionsPerHost
        // 变量的设置，建立全部连接，然后提供给程序使用，并且一旦其中某个连接到数据库的访问失败，
        // 则会清空整个连接池到这台数据库的连接，并重新建立连接。
        // 而 mongodb 对中断连接的垃圾清理工作则是懒惰的被动清理方式，
        // 如果驱动程序端配置的连接数过大，一旦发生重连，则会导致 mongo
        // 服务器端堆积大量的垃圾连接以及对应数据，导致主机资源耗尽。
        // 建议： mongodb 驱动的连接池大小的设置一般应该控制 100 左右。

        return client;
    }

    private static MongoClient createReSetInstance(MongoConfig config) {
        MongoClient client = null;

        MongoClientOptions.Builder builder = new MongoClientOptions.Builder();
        builder.connectTimeout(config.getConnectTimeout());
        builder.socketTimeout(config.getSocketTimeout());
        builder.connectionsPerHost(100);
        builder.writeConcern(new WriteConcern(config.getW(), config.getWtimeout()));
        builder.readPreference(config.getReadPreference());
        MongoClientOptions options = builder.build();

        List<ServerAddress> addresses = new ArrayList<ServerAddress>();
        for (String host : config.getHosts()) {
            String[] ipAndport = host.split(":");
            ServerAddress address = new ServerAddress(ipAndport[0], Integer.valueOf(ipAndport[1]));
            addresses.add(address);
        }
        client = new MongoClient(addresses, options);
        return client;
    }
}
