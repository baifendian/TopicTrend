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

package com.bfd.topictread.tools.model;

/**
 * 微信数据聚集
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class WeixinAgg {
    /** 事件id */
    private String eventId;

    /** 阅读数 */
    private Long totalRead;

    /** 总记录数 */
    private Long total;

    /**
     * getter method
     * 
     * @see WeixinAgg#eventId
     * @return the eventId
     */
    public String getEventId() {
        return eventId;
    }

    /**
     * setter method
     * 
     * @see WeixinAgg#eventId
     * @param eventId
     *            the eventId to set
     */
    public void setEventId(String eventId) {
        this.eventId = eventId;
    }

    /**
     * getter method
     * 
     * @see WeixinAgg#totalRead
     * @return the totalRead
     */
    public Long getTotalRead() {
        return totalRead;
    }

    /**
     * setter method
     * 
     * @see WeixinAgg#totalRead
     * @param totalRead
     *            the totalRead to set
     */
    public void setTotalRead(Long totalRead) {
        this.totalRead = totalRead;
    }

    /**
     * getter method
     * 
     * @see WeixinAgg#total
     * @return the total
     */
    public Long getTotal() {
        return total;
    }

    /**
     * setter method
     * 
     * @see WeixinAgg#total
     * @param total
     *            the total to set
     */
    public void setTotal(Long total) {
        this.total = total;
    }

}
