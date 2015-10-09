package cn.edu.tsinghua.thss.popcorn.config;

import android.os.Environment;

/**
 * Created by LY on 2015/6/4.
 */
public class Config {

    public static String ACCESS_TOKEN = "hello_world";

    public static String LOCAL_IP = "http://192.168.1.102";
    public static String REPORT_URL =  LOCAL_IP + "/app/maintain/add/";
    public static String ROUTE_GET_URL = LOCAL_IP + "/app/route";
    public static String FORM_GET_URL = LOCAL_IP + "/app/form";

    public static String ATTENDANCE_POST_URL = LOCAL_IP + "/app/check/";
    public static String ATTENDANCE_GET_URL = LOCAL_IP + "/app/checkinfo/";

    public static String SCORE_RANK_URL = LOCAL_IP + "/app/score/rank/";
    public static String VERSION_SERVER_URL = LOCAL_IP + "/app/version/";
    public static String GET_ALL_DEVICE_BRIEF_URL = LOCAL_IP + "/app/device/brief/";
    public static String GET_DEVICE_INFO_URL = LOCAL_IP + "/app/device/info/";
    public static String GET_USER_INFO_URL = LOCAL_IP + "/app/userinfo/";
    public static String GET_BONUS_URL = LOCAL_IP + "/app/egg/";
    public static String GET_BONUS_TIME_URL = LOCAL_IP + "/app/egg/time";
    public static String GET_BONUS_INFO_URL = LOCAL_IP + "/app/egg/info";
    public static String LOGIN_URL = LOCAL_IP +"/app/login/";
    public static String SUBMIT_METER_URL = LOCAL_IP + "/app/meter/";
    public static String SUBMIT_USER_INFO_URL = LOCAL_IP + "/app/userinfo/submit/";
    public static String SUBMIT_REPORT_IMAGE_URL = LOCAL_IP + "/app/maintain/image/";
    public static String SUBMIT_AVATAR_URL = LOCAL_IP + "/app/avatar/";

    public static String REPAIR_TASK_LIST_URL =  LOCAL_IP + "/app/maintain/list/2/";
    public static String REPAIR_TASK_SUBMIT_URL = LOCAL_IP + "/app/maintain/submit/";
    public static String REPAIR_TASK_UPDATE_URL = LOCAL_IP + "/app/maintain/update/";
    public static String REPAIR_TASK_CONFIRM_URL = LOCAL_IP + "/app/maintain/confirm/";
    public static String MAINTAIN_TASK_LIST_URL = LOCAL_IP + "/app/maintain/list/1/";
    public static String MAINTAIN_TASK_SUBMIT_URL = LOCAL_IP + "/app/maintain/submit/";
    public static String MAINTAIN_TASK_UPDATE_URL = LOCAL_IP + "/app/maintain/update/";
    public static String MAINTAIN_TASK_CONFIRM_URL = LOCAL_IP + "/app/maintain/confirm/";
    public static String TASK_LIST_URL = LOCAL_IP + "/app/task/list/";
    public static String TASK_SUBMIT_URL = LOCAL_IP + "/app/task/submit/";
    public static String TASK_UPDATE_URL = LOCAL_IP + "/app/task/update/";
    public static String TASK_CONFIRM_URL = LOCAL_IP + "/app/task/confirm/";

    public static String WILL_WINGS_ORG_WEBSITE = "http://www.willwings.com";
    public static String AVATAR_FILE_DIR = Environment.getExternalStorageDirectory().getPath() + "/willwings/avatar/";
    public static String REPORT_FILE_PATH = Environment.getExternalStorageDirectory().getPath() + "/willwings/photos/report.jpg";
    public static String DEBUG_USERNAME = "";
    public static int MAX_NETWORK_TIME = 5000;

    public static int MAIN_UPDATE_DELAY = 0;
    public static int REPAIR_UPDATE_DELAY = 0;
    public static int RECORD_UPDATE_DELAY = 0;

    public static int MAIN_UPDATE_INTERVAL = 1000;
    public static int REPAIR_UPDATE_INTERVAL = 1000*60*2;
}
