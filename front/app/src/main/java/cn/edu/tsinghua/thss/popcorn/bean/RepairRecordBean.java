package cn.edu.tsinghua.thss.popcorn.bean;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * Created by 兜哥 on 2016/6/7.
 */
public class RepairRecordBean {
    public String status;
    public ArrayList<Info> data;
    public class Info implements Serializable{
        public int id;
        public String title;
        public String device_name;
        public String device_brief;
        public String creator;
        public String create_time;
        public String description;
        public String image;
        public String memo;
        public String editor;
        public String edit_datetime;
        public Boolean is_audit;
        public String note;
     }
}
