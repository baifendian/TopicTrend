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
 * 事件信息类
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class EventInfo {
    /** 事件id */
    private String id;

    /** 事件分类 */
    private int cate;

    @Override
    public String toString() {
        return "EventInfo [id=" + id + ", cate=" + cate + "]";
    }

    /**
     * getter method
     * 
     * @see EventInfo#id
     * @return the id
     */
    public String getId() {
        return id;
    }

    /**
     * setter method
     * 
     * @see EventInfo#id
     * @param id
     *            the id to set
     */
    public void setId(String id) {
        this.id = id;
    }

    /**
     * getter method
     * 
     * @see EventInfo#cate
     * @return the cate
     */
    public int getCate() {
        return cate;
    }

    /**
     * setter method
     * 
     * @see EventInfo#cate
     * @param cate
     *            the cate to set
     */
    public void setCate(int cate) {
        this.cate = cate;
    }

}
