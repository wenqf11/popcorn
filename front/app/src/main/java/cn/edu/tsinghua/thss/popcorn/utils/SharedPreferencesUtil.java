package cn.edu.tsinghua.thss.popcorn.utils;

import android.content.Context;
import android.content.SharedPreferences;

/**
 * Created by 兜哥 on 2016/7/8.
 */
public class SharedPreferencesUtil {
    private static SharedPreferences sp;
    public static SharedPreferences getSharedPreferences(Context context){
        if(sp==null){
            sp=context.getSharedPreferences("config",Context.MODE_PRIVATE);
        }
        return sp;
    }
    public static boolean getBoolean(Context context,String key,Boolean value){
        SharedPreferences sp = getSharedPreferences(context);
        return  sp.getBoolean(key,value);
    }
    public static void putBoolean(Context context,String key,Boolean value){
        SharedPreferences sp = getSharedPreferences(context);
        sp.edit().putBoolean(key,value).commit();
    }
    public static String getString(Context context,String key,String value){
        SharedPreferences sp = getSharedPreferences(context);
        return  sp.getString(key,value);
    }
    public static void putString(Context context,String key,String value){
        SharedPreferences sp = getSharedPreferences(context);
        sp.edit().putString(key,value).commit();
    }
    public static int getInt(Context context,String key,int value){
        SharedPreferences sp = getSharedPreferences(context);
        return  sp.getInt(key,value);
    }
    public static void putInt(Context context,String key,int value){
        SharedPreferences sp = getSharedPreferences(context);
        sp.edit().putInt(key,value).commit();
    }
    /**
     * 移除
     */
    public static void remove(Context context,String sky){
        SharedPreferences sp=getSharedPreferences(context);
        sp.edit().remove(sky).commit();
    }
}
