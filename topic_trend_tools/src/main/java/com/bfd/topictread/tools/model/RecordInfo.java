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
 * 记录信息类
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class RecordInfo {
    /** 记录id */
    private String id;

    /** 事件id */
    private String event_id;

    /** 日期 */
    private String date;

    /** 影响力 */
    private int influence;

    /**
     * getter method
     * 
     * @see RecordInfo#id
     * @return the id
     */
    public String getId() {
        return id;
    }

    /**
     * setter method
     * 
     * @see RecordInfo#id
     * @param id
     *            the id to set
     */
    public void setId(String id) {
        this.id = id;
    }

    /**
     * getter method
     * 
     * @see RecordInfo#event_id
     * @return the event_id
     */
    public String getEvent_id() {
        return event_id;
    }

    /**
     * setter method
     * 
     * @see RecordInfo#event_id
     * @param event_id
     *            the event_id to set
     */
    public void setEvent_id(String event_id) {
        this.event_id = event_id;
    }

    /**
     * getter method
     * 
     * @see RecordInfo#date
     * @return the date
     */
    public String getDate() {
        return date;
    }

    /**
     * setter method
     * 
     * @see RecordInfo#date
     * @param date
     *            the date to set
     */
    public void setDate(String date) {
        this.date = date;
    }

    /**
     * getter method
     * 
     * @see RecordInfo#influence
     * @return the influence
     */
    public int getInfluence() {
        return influence;
    }

    /**
     * setter method
     * 
     * @see RecordInfo#influence
     * @param influence
     *            the influence to set
     */
    public void setInfluence(int influence) {
        this.influence = influence;
    }

}
