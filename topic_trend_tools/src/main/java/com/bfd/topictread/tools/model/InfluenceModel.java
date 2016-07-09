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
 * <p>
 * 
 * @author : dsfan
 * @date : 2016-7-9
 */
public class InfluenceModel {
    /** 微博影响力 */
    private double weiboInfluence;

    /** 微信影响力 */
    private double weixinInfluence;

    /** 新闻影响力 */
    private double newsInfluence;

    /**
     * getter method
     * 
     * @see InfluenceModel#weiboInfluence
     * @return the weiboInfluence
     */
    public double getWeiboInfluence() {
        return weiboInfluence;
    }

    /**
     * setter method
     * 
     * @see InfluenceModel#weiboInfluence
     * @param weiboInfluence
     *            the weiboInfluence to set
     */
    public void setWeiboInfluence(double weiboInfluence) {
        this.weiboInfluence = weiboInfluence;
    }

    /**
     * getter method
     * 
     * @see InfluenceModel#weixinInfluence
     * @return the weixinInfluence
     */
    public double getWeixinInfluence() {
        return weixinInfluence;
    }

    /**
     * setter method
     * 
     * @see InfluenceModel#weixinInfluence
     * @param weixinInfluence
     *            the weixinInfluence to set
     */
    public void setWeixinInfluence(double weixinInfluence) {
        this.weixinInfluence = weixinInfluence;
    }

    /**
     * getter method
     * 
     * @see InfluenceModel#newsInfluence
     * @return the newsInfluence
     */
    public double getNewsInfluence() {
        return newsInfluence;
    }

    /**
     * setter method
     * 
     * @see InfluenceModel#newsInfluence
     * @param newsInfluence
     *            the newsInfluence to set
     */
    public void setNewsInfluence(double newsInfluence) {
        this.newsInfluence = newsInfluence;
    }

}
