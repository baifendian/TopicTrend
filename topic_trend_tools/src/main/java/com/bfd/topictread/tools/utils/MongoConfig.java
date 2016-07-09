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
import java.util.List;

import com.mongodb.ReadPreference;

/**
 * mongodb配置类
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class MongoConfig {
    private String host;

    private int port = 27017;

    private List<String> hosts = new ArrayList<String>();

    private int socketTimeout = 1000;

    private int connectTimeout = 1000;

    private String dbName;

    private boolean slaveOk = false;

    private boolean isReSet = false;

    private ReadPreference readPreference = ReadPreference.primaryPreferred();

    private int w = 0;

    private int wtimeout = 0;

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public int getSocketTimeout() {
        return socketTimeout;
    }

    public void setSocketTimeout(int socketTimeout) {
        this.socketTimeout = socketTimeout;
    }

    public int getConnectTimeout() {
        return connectTimeout;
    }

    public void setConnectTimeout(int connectTimeout) {
        this.connectTimeout = connectTimeout;
    }

    public String getDbName() {
        return dbName;
    }

    public void setDbName(String dbName) {
        this.dbName = dbName;
    }

    public List<String> getHosts() {
        return hosts;
    }

    public void setHosts(List<String> hosts) {
        this.hosts = hosts;
    }

    public boolean isReSet() {
        return isReSet;
    }

    public void setReSet(boolean isReSet) {
        this.isReSet = isReSet;
    }

    public ReadPreference getReadPreference() {
        return readPreference;
    }

    public void setReadPreference(ReadPreference readPreference) {
        this.readPreference = readPreference;
    }

    public int getW() {
        return w;
    }

    public void setW(int w) {
        this.w = w;
    }

    public int getWtimeout() {
        return wtimeout;
    }

    public void setWtimeout(int wtimeout) {
        this.wtimeout = wtimeout;
    }

    public void setSlaveOk(boolean slaveOk) {
        this.slaveOk = slaveOk;
    }

    public boolean isSlaveOk() {
        return slaveOk;
    }
}
