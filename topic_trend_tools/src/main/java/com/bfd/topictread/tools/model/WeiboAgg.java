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
 * 微博数据聚集
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class WeiboAgg {
    /** 事件id */
    private String eventId;

    /** 评论数 */
    private Long totalComment;

    /** 点赞数 */
    private Long totalLike;

    /** 转发数 */
    private Long totalTransmit;

    /** 总记录数 */
    private Long total;

    @Override
    public String toString() {
        return "WeiboAgg [eventId=" + eventId + ", totalComment=" + totalComment + ", totalLike=" + totalLike + ", totalTransmit=" + totalTransmit + ", total=" + total + "]";
    }

    /**
     * getter method
     * 
     * @see WeiboAgg#eventId
     * @return the eventId
     */
    public String getEventId() {
        return eventId;
    }

    /**
     * setter method
     * 
     * @see WeiboAgg#eventId
     * @param eventId
     *            the eventId to set
     */
    public void setEventId(String eventId) {
        this.eventId = eventId;
    }

    /**
     * getter method
     * 
     * @see WeiboAgg#totalComment
     * @return the totalComment
     */
    public Long getTotalComment() {
        return totalComment;
    }

    /**
     * setter method
     * 
     * @see WeiboAgg#totalComment
     * @param totalComment
     *            the totalComment to set
     */
    public void setTotalComment(Long totalComment) {
        this.totalComment = totalComment;
    }

    /**
     * getter method
     * 
     * @see WeiboAgg#totalLike
     * @return the totalLike
     */
    public Long getTotalLike() {
        return totalLike;
    }

    /**
     * setter method
     * 
     * @see WeiboAgg#totalLike
     * @param totalLike
     *            the totalLike to set
     */
    public void setTotalLike(Long totalLike) {
        this.totalLike = totalLike;
    }

    /**
     * getter method
     * 
     * @see WeiboAgg#totalTransmit
     * @return the totalTransmit
     */
    public Long getTotalTransmit() {
        return totalTransmit;
    }

    /**
     * setter method
     * 
     * @see WeiboAgg#totalTransmit
     * @param totalTransmit
     *            the totalTransmit to set
     */
    public void setTotalTransmit(Long totalTransmit) {
        this.totalTransmit = totalTransmit;
    }

    /**
     * getter method
     * 
     * @see WeiboAgg#total
     * @return the total
     */
    public Long getTotal() {
        return total;
    }

    /**
     * setter method
     * 
     * @see WeiboAgg#total
     * @param total
     *            the total to set
     */
    public void setTotal(Long total) {
        this.total = total;
    }

}
