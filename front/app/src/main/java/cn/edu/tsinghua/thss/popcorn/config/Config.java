package cn.edu.tsinghua.thss.popcorn.config;

/**
 * Created by LY on 2015/6/4.
 */
public class Config {

    public static String ACCESS_TOKEN = "hello_world";

    public static String LOCAL_IP = "http://192.168.1.102";//"http://192.168.1.103";
    public static String REPAIR_TASK_LIST_URL =  Config.LOCAL_IP + "/app/maintain/list/2/";
    public static String MAINTAIN_TASK_LIST_URL = Config.LOCAL_IP + "/app/maintain/list/1/";

    public static String SCORE_RANK_URL = LOCAL_IP + "/app/score/rank/";
    public static String VERSION_SERVER_URL = LOCAL_IP + "/app/version/";

    public static String WILL_WINGS_ORG_WEBSITE = "http://www.willwings.com";
    public static String DEBUG_USERNAME = "";
    public static int MAX_NETWORK_TIME = 5000;

    public static int MAIN_UPDATE_DELAY = 0;
    public static int REPAIR_UPDATE_DELAY = 0;
    public static int RECORD_UPDATE_DELAY = 0;

    public static int MAIN_UPDATE_INTERVAL = 1000;
    public static int REPAIR_UPDATE_INTERVAL = 1000*60*2;
    public static int RECORD_UPDATE_INTERVAL = 1000*60*2;
}
